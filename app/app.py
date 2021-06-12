from bson import json_util, ObjectId
from flask import Flask, request
from datetime import datetime

from app.helpers import mongo_client

API_VERSION = '1.0'

app = Flask(__name__)
db = mongo_client()


@app.route('/')
def root():
    response = {'apiVersion': API_VERSION, 'appName': 'Topbox Backend Take Home Test'}
    return json_util.dumps(response)


@app.route('/clients')
def clients():
    return json_util.dumps(db.clients.find({}))


@app.route('/clients/<client_id>')
def clients_by_id(client_id):
    client_object_id = ObjectId(client_id)
    return json_util.dumps(db.clients.find_one({'_id': client_object_id}))


@app.route('/engagements')
def engagements():
    return json_util.dumps(db.engagements.find({}))


@app.route('/engagements/<engagement_id>')
def engagements_by_id(engagement_id):
    engagement_object_id = ObjectId(engagement_id)
    return json_util.dumps(db.engagements.find_one({'_id': engagement_object_id}))


@app.route('/interactions')
def interactions():
    return json_util.dumps(db.interactions.find({}))


@app.route('/interactions/<engagement_id>')
def interactions_by_engagement_id_and_interaction_date(engagement_id):
    """
        Query interactions by engagement id and with an optional start and end datetime
        query params: startDate, endDate
        http://localhost:5000/interactions/<engagement_id>?startDate=2020-06-01T12:12:12&endDate=2020-07-01T12:12:12
    """

    engagement_object_id = ObjectId(engagement_id)
    query = [{'engagementId': engagement_object_id}]

    if not request.args.get('startDate') is None:
        start_date = datetime.strptime(request.args.get('startDate'), '%Y-%m-%dT%H:%M:%S')
        query.append({'interactionDate': {'$gte': start_date}})
    if not request.args.get('endDate') is None:
        end_date = datetime.strptime(request.args.get('endDate'), '%Y-%m-%dT%H:%M:%S')
        query.append({'interactionDate': {'$lte': end_date}})

    return json_util.dumps(db.interactions.find({'$and': query}))


@app.route('/interactions/<interaction_id>')
def interactions_by_id(interaction_id):
    interaction_object_id = ObjectId(interaction_id)
    return json_util.dumps(db.interactions.find_one({'_id': interaction_object_id}))
