from flask import Flask
from flask import jsonify
from flask import request
import os
from utils import DatabaseConnector as dbc
import firebase_admin
from firebase_admin import auth
from flask_httpauth import HTTPTokenAuth
from firebase_admin import credentials
import logging

logging.basicConfig(level=logging.DEBUG)

cred = credentials.Certificate("config/cinema-food-firebase-adminsdk-dskp9-98ba81129d.json")
firebase_admin.initialize_app(cred)
authorization = HTTPTokenAuth(scheme='Bearer')

app = Flask("Cinema Backend")

host = os.environ['MYSQL_HOST']
user = os.environ['MYSQL_USERNAME']
passw = os.environ['MYSQL_PASS']


def create_cart(uid):
    conn = dbc.DatabaseConnector(host, user, passw)
    conn.connect()
    conn.query(f'INSERT INTO cart (Customer_ID,totalDue,status) VALUES ({uid},0.0,\'PENDING\')')
    conn.close()


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
    productid = request.form.get('productId')
    #uid = request.form.get('uid') #cambiare con id preso da token
    uid = authorization.current_user()
    uid = f'\'{uid}\''
    conn = dbc.DatabaseConnector(host, user, passw)
    response = dict()
    response['productId'] = request.form.get('productId')
    try:
        conn.connect()
        cartid = conn.query(f'SELECT Cart_ID from cart WHERE Customer_ID = {uid} AND status = \'PENDING\'')
        logging.debug('Last statement: '+conn.getstatement())
        if len(cartid) == 0:
            create_cart(uid)
            cartid = conn.query(f'SELECT Cart_ID from cart WHERE Customer_ID = \'{uid}\' AND status = \'PENDING\'')
        logging.debug(f'After {cartid}')
        cartid = cartid[0][0]
        conn.query(f'INSERT INTO cart_item (Product_ID,Cart_ID) VALUES ({productid},{cartid})')
        conn.close()
        response['status'] = 'success'
    except Exception as e:
        logging.debug(e)
        response['status'] = 'fail'
    return jsonify(response), 200


@app.route('/api/cart/removeproduct', methods=['POST'])
@authorization.login_required
def remove_product_from_cart():
    productid = request.form.get('productId')
    #uid = request.form.get('uid')  # cambiare con id preso da token
    uid = authorization.current_user()
    conn = dbc.DatabaseConnector(host, user, passw)
    response = dict()
    response['productId'] = request.form.get('productId')
    try:
        conn.connect()
        cartid = conn.query(f'SELECT Cart_ID from cart WHERE Customer_ID = \'{uid}\' AND status = \'PENDING\'')
        cartid = cartid[0][0]
        conn.query(f'DELETE FROM cart_item WHERE Cart_ID = \'{cartid}\' AND Product_ID = {productid} \
        LIMIT 1')
        conn.close()
        response['status'] = 'success'
    except Exception as e:
        logging.debug(e)
        response['status'] = 'fail'
    return jsonify(response), 200


@app.route('/api/cart/getcart', methods=['GET'])
@authorization.login_required
def get_user_cart():
    #uid = request.form.get('uid')  # cambiare con id preso da token
    uid = authorization.current_user()
    #uid = f'"{uid}"'
    conn = dbc.DatabaseConnector(host, user, passw)
    conn.connect()
    query = conn.query(f'\
    SELECT product.Product_ID, title, ingredients, image, price, calories, description, size, cat\
    FROM product \
    JOIN \
    (SELECT Product_ID \
     FROM cart\
     JOIN cart_item ON cart_item.Cart_ID = cart.Cart_ID\
    WHERE Customer_ID = \'{uid}\') T \
    ON T.Product_ID = product.Product_ID;')
    conn.close()
    food_list = []
    for (food_id, title, ingredients, image, price, calories, description, size, cat) in query:
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


@app.route('/api/food/getall', methods=['GET'])
#@authorization.login_required
def get_all_food():
    conn = dbc.DatabaseConnector(host, user, passw)
    conn.connect()
    query = conn.query('SELECT * FROM product')
    conn.close()
    food_list = []
    for (food_id, title, ingredients, image, price, calories, description, size, cat) in query:
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
#@authorization.login_required
def get_all_drinks():
    conn = dbc.DatabaseConnector(host, user, passw)
    conn.connect()
    query = conn.query("SELECT * FROM product WHERE cat = 'DRINK'")
    conn.close()
    food_list = []
    for (food_id, title, ingredients, image, price, calories, description, size, cat) in query:
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
