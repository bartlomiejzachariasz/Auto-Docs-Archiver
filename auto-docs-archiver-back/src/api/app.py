import json
import logging
import boto3

from bson import ObjectId
from flask import Flask, jsonify, request, make_response, abort, Response, send_file
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

from src.api.auth import Authenticator
from src.errors.errors import UserNotFound
from src.utils.basic_processor import BasicProcessor
from src.utils.classifier import Classifier
from src.resources.config import DB_CONFIG, AWS_CONFIG
from src.utils.decorators import auth_required
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
basic_processor = BasicProcessor()
authenticator = Authenticator(db_connector=connector)
classifier = Classifier()
traces = []


@app.route("/health_check", methods=["GET"])
@cross_origin()
def health_check():
    resp = jsonify(datetime.datetime.now())
    resp.status_code = 201
    return resp


@app.route("/auth/signin", methods=["POST"])
def sign_in():
    try:
        credentials = json.loads(request.data.decode('utf-8'))
        token = authenticator.authenticate_user(credentials['username'], credentials['password'])
        return make_response(jsonify({'token': token, 'username': credentials['username']}))
    except Exception as error:
        logging.error(f'Error: {error}')
        abort(403)


@app.route("/auth/register", methods=["POST"])
def register():
    try:
        credentials = json.loads(request.data.decode('utf-8'))
        user = connector.find_by_column("users", "username", credentials['username'], single=True)
        if user is not None:
            abort(409)
        connector.save("users", credentials)
        return Response(status=201)
    except Exception as error:
        logging.error(f'Error: {error}')
        abort(500)


@app.route("/documents", methods=["GET"])
@auth_required
def get_all_documents():
    try:
        user = authenticator.get_authenticated_user()
        user_id = connector.find_by_column("users", "username", user["username"], single=True, exclude=["filename"])
        documents = connector.find_by_column("documents", "user_id", str(user_id['_id']))

        response = [{
            "id": str(document['_id']),
            "date": str(document['date']),
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
        if str(document["user_id"]) != str(user["_id"]):
            abort(403)
        else:
            file_path = get_image_url(str(document["_id"]))

            response = {
                "id": doc_id,
                "date": str(document["date"]),
                "category": document["category"],
                "file_path": file_path
            }

            return make_response(jsonify(response))
    except Exception as error:
        logging.error(error)
        abort(403)


@app.route("/documents/<doc_id>", methods=["PUT"])
@auth_required
def update_id(doc_id):
    try:
        credentials = json.loads(request.data.decode('utf-8'))
        user = authenticator.get_authenticated_user()
        document = connector.find_by_column("documents", "_id", ObjectId(doc_id), single=True)
        if str(document["user_id"]) != str(user["_id"]):
            abort(403)
        else:
            connector.update("documents", "_id", ObjectId(doc_id), "date", credentials["date"])
            return Response(status=201)
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
            "date": processed_text['date'] if processed_text['date'] is not None else 'unknown',
            "user_id": str(user_id["_id"])
        })

        upload_to_s3(file.filename, str(_id))
        return str(_id)

    except Exception as error:
        logging.error(error)
        abort(500)


def download_from_s3(filename):
    s3 = boto3.resource('s3')

    output = filename
    s3.Bucket(AWS_CONFIG["bucket_name"]).download_file(filename, output)

    return output


def upload_to_s3(file, filename):
    s3_client = boto3.client('s3')
    try:
        with open(file, 'rb') as f:
            s3_client.upload_fileobj(f, AWS_CONFIG["bucket_name"], f'{filename}.jpg')
    except Exception:
        abort(500)


def get_image_url(file_id):
    s3_client = boto3.client('s3')
    location = s3_client.get_bucket_location(Bucket=AWS_CONFIG["bucket_name"])['LocationConstraint']
    return f'https://s3-{location}.amazonaws.com/{AWS_CONFIG["bucket_name"]}/{file_id}.jpg'


if __name__ == "__main__":
    app.run()
