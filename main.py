from flask import Flask
from flask import jsonify
from flask import request
import os
import mysql.connector
import firebase_admin
from firebase_admin import auth
from flask_httpauth import HTTPTokenAuth
from firebase_admin import credentials

cred = credentials.Certificate("config/cinema-food-firebase-adminsdk-dskp9-98ba81129d.json")
firebase_admin.initialize_app(cred)


class User:
    def __init__(self, email, uid):
        pass


authorization = HTTPTokenAuth(scheme='Bearer')
database_host = os.environ['MYSQL_HOST']
database_username = os.environ['MYSQL_USERNAME']
database_password = os.environ['MYSQL_PASS']

app = Flask("Cinema Backend")


@authorization.verify_token
def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except auth.InvalidIdTokenError:
        pass


@app.route('/api/restricted')
@authorization.login_required
def restricted_api():
    return authorization.current_user()


@app.route('/api/cart/addproduct', methods=['POST'])
@authorization.login_required
def add_product_to_cart():
    response = dict()
    response['uid'] = authorization.current_user()
    response['productId'] = request.form.get('productId')
    response['status'] = 'success'
    return jsonify(response), 200


@app.route('/api/cart/removeproduct', methods=['POST'])
@authorization.login_required
def remove_product_from_cart():
    response = dict()
    response['uid'] = authorization.current_user()
    response['productId'] = request.form.get('productId')
    response['status'] = 'success'
    return jsonify(response), 200


@app.route('/api/food/getall', methods=['GET'])
@authorization.login_required
def get_all_food():
    cnx = mysql.connector.connect(user=database_username, password=database_password,
                                  host=database_host,
                                  database='Cinema')
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM food ")
    food_list = []
    for (food_id, title, ingredients, image, price, calories, description, size, cat) in cursor:
        food_dict = dict()
        food_dict['id'] = food_id
        food_dict['title'] = title
        food_dict['ingredients'] = ingredients
        food_dict['image'] = image
        food_dict['price'] = price
        food_dict['calories'] = calories
        food_dict['description'] = description
        food_dict['size'] = size
        food_dict['cat'] = cat
        food_list.append(food_dict)

    return jsonify(food_list), 200


@app.route('/api/food/getdrinks', methods=['GET'])
@authorization.login_required
def get_all_drinks():
    cnx = mysql.connector.connect(user=database_username, password=database_password,
                                  host=database_host,
                                  database='Cinema')
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM food WHERE cat = 'DRINK'")
    food_list = []
    for (food_id, title, ingredients, image, price, calories, description, size, cat) in cursor:
        food_dict = dict()
        food_dict['id'] = food_id
        food_dict['title'] = title
        food_dict['ingredients'] = ingredients
        food_dict['image'] = image
        food_dict['price'] = price
        food_dict['calories'] = calories
        food_dict['description'] = description
        food_dict['size'] = size
        food_dict['cat'] = cat
        food_list.append(food_dict)

    return jsonify(food_list), 200



@app.route('/api/ping', methods=['GET'])
def ping():
    # return_values = dict()
    # return_values["host"] = database_host
    # return_values["username"] = database_username
    # return_values["password"] = database_password
    # return jsonify(return_values), 200
    return "ping", 200

app.run(host='0.0.0.0')
