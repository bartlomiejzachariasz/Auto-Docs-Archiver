from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from src.processor import Processor
from ..connect import Connector

import datetime

from src.ocr import Reader

app = Flask(__name__)
cors = CORS(app)
reader = Reader()
connector = Connector("localhost", 27017)
connector.connect("test_db")
processor = Processor(connector)


@app.route("/health_check", methods=["GET"])
@cross_origin()
def health_check():
    resp = jsonify(datetime.datetime.now())
    resp.status_code = 201
    return resp


@app.route("/upload", methods=["POST"])
def upload_image():
    file = request.files['file']
    extracted_text = reader.read(file)
    resp = jsonify(processor.process_data(data_input=extracted_text))
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run()
