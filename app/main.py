import os
from flask import Flask, jsonify
from pymongo import MongoClient
app = Flask(__name__)

uri = os.environ.get('MONGO_URI')

client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

db = client['weathercritic']
collection = db['forecasts']

@app.route('/forecasts')
def index():
  results = collection.find({})
  return jsonify(list(results))