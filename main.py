from flask import Flask
from flask import jsonify
import os
import mysql.connector

database_host = os.environ['MYSQL_HOST']
database_username = os.environ['MYSQL_USERNAME']
database_password = os.environ['MYSQL_PASS']

app = Flask("Cinema Backend")


@app.route('/api/food/getall', methods=['GET'])
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
    return_values = dict()
    return_values["host"] = database_host
    return_values["username"] = database_username
    return_values["password"] = database_password
    return jsonify(return_values), 200


app.run(host='0.0.0.0')
