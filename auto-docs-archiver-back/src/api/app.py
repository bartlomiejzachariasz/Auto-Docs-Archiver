import json
import logging
import io
import boto3

from bson import ObjectId
from flask import Flask, jsonify, request, make_response, abort, Response, send_file
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

from src.api.auth import Authenticator
from src.utils.basic_processor import BasicProcessor
from src.utils.classifier import Classifier
from src.resources.config import DB_CONFIG
from src.utils.decorators import auth_required
from src.legacy.processor import Processor
from src.utils.xes_generator import XesGenerator
from src.utils.connect import Connector

import datetime

from src.utils.ocr import Reader

app = Flask(__name__)
jwt = JWTManager(app)
app.config.from_json('../resources/config.json')
cors = CORS(app)
reader = Reader()
connector = Connector(DB_CONFIG["host"], DB_CONFIG["port"])
connector.connect(DB_CONFIG["db_name"])
processor = Processor(connector)
basic_processor = BasicProcessor()
authenticator = Authenticator(db_connector=connector)
classifier = Classifier()
xes_generator = XesGenerator()
traces = []


@app.route("/health_check", methods=["GET"])
@cross_origin()
def health_check():
    resp = jsonify(datetime.datetime.now())
    resp.status_code = 201
    return resp


@app.route("/generate", methods=["GET"])
@auth_required
def generate():
    return xes_generator.generate(traces)


@app.route("/auth/signin", methods=["POST"])
def sign_in():
    try:
        credentials = json.loads(request.data.decode('utf-8'))
        token = authenticator.authenticate_user(credentials['username'], credentials['password'])
        return make_response(jsonify({'token': token, 'username': credentials['username']}))
    except Exception as error:
        logging.error(f'Error: {error}')
        abort(403)


@app.route("/documents", methods=["GET"])
@auth_required
def get_all_documents():
    try:
        user = authenticator.get_authenticated_user()
        user_id = connector.find_by_column("users", "username", user["username"], single=True, exclude=["filename"])
        documents = connector.find_by_column("documents", "user_id", str(user_id['_id']))

        response = [{
            "id": str(document['_id']),
            "date": "test_string",
            "category": document['category']
        } for document in documents]

        return make_response(jsonify(response))
    except Exception as e:
        logging.error(e)


@app.route("/documents/<doc_id>", methods=["DELETE"])
@auth_required
def delete_document(doc_id):
    try:
        user = authenticator.get_authenticated_user()
        user_id = connector.find_by_column("users", "username", user["username"], single=True, exclude=["filename"])

        document = connector.find_by_column("documents", "_id", ObjectId(doc_id), single=True)

        if document["user_id"] != str(user_id["_id"]):
            return Response(status=403)

        connector.delete("documents", "_id", ObjectId(doc_id))

        return Response(status=204)
    except Exception as e:
        logging.error(e)


@app.route("/documents/<doc_id>", methods=["GET"])
@auth_required
def get_document(doc_id):
    try:
        user = authenticator.get_authenticated_user()
        document = connector.find_by_column("documents", "_id", ObjectId(doc_id), single=True)
        if document["user_id"] != str(user["_id"]):
            abort(403)
        else:
            file = download_from_s3(document["filename"])

            with open(file, 'rb') as f:
                return send_file(
                    io.BytesIO(f.read()),
                    attachment_filename=file,
                    mimetype='image/jpeg')
    except Exception as error:
        logging.error(error)
        abort(403)


@app.route("/documents", methods=["POST"])
@auth_required
def upload_document():
    try:
        user = authenticator.get_authenticated_user()
        file = request.files['file']
        file.save(file.filename)
        extracted_text = reader.read(file)
        processed_text = basic_processor.process_data(extracted_text)
        category = classifier.classify(processed_text['data'])

        user_id = connector.find_by_column("users", "username", user["username"], single=True)

        _id = connector.save("documents", {
            "category": category,
            "date": "test_date",
            "user_id": str(user_id["_id"])
        })
        upload_to_s3(file.filename, str(_id))
        return Response(status=201)
    except Exception as error:
        logging.error(error)
        abort(403)


def download_from_s3(filename):
    s3 = boto3.resource('s3')

    output = filename
    s3.Bucket('autoarchiverfiles').download_file(filename, output)

    return output


def upload_to_s3(file, filename):
    s3_client = boto3.client('s3')
    try:
        with open(file, 'rb') as f:
            s3_client.upload_fileobj(f, 'autoarchiverfiles', filename)
    except Exception:
        abort(500)


if __name__ == "__main__":
    app.run()
