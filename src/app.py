from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import config
from resources.example_controller import ExampleController

app = Flask("soft engineering")
app.config.from_object(config)
api = Api(app)
CORS(app, origin='*')

cred = credentials.Certificate('firebaseKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

api.add_resource(ExampleController, '/example/')


if __name__ == "__main__":
    app.run()