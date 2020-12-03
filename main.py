from flask import Flask
from flask import jsonify
import os

database_host = os.environ['MYSQL_HOST']
database_username = os.environ['MYSQL_USERNAME']
database_password = os.environ['MYSQL_PASS']

app = Flask("Cinema Backend")


@app.route('/api/ping', methods=['GET'])
def ping():
    return_values = dict()
    return_values["host"] = database_host
    return_values["username"] = database_username
    return_values["password"] = database_password
    return jsonify(return_values), 200


app.run(host='0.0.0.0')
