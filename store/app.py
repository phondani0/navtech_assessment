from flask import Flask, jsonify, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from os.path import join, dirname, realpath
import pandas as pd


app = Flask(__name__)


app.secret_key = 'secret_key@1234'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ankit@1234'
app.config['MYSQL_DB'] = 'store'

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if(request.method == 'GET'):

        data = "hello world"
        return jsonify({'data': data})


# add new products route
@app.route("/admin/product", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
       # set the file path
        uploaded_file.save(file_path)
        parseCSV(file_path)
       # save the file

    return "Products uploaded successfully"


# used for parsing csv file
def parseCSV(filePath):
    col_names = ['name', 'price']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    # Loop through the Rows
    for i, row in csvData.iterrows():
        sql = "INSERT INTO products (name, price) VALUES (%s, %s)"

        value = (row['name'], row['price'])

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, value)
        mysql.connection.commit()

        # print(i, row['name'], row['price'])


# create order route
@app.route('/orders', methods=['POST'])
def create_order():
    msg = ''

    if request.method == 'POST':
        order_items = request.get_json()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        user_id = 1
        # create order
        sql = "INSERT INTO orders (user_id) VALUES (%s)"

        value = (user_id,)
        cursor.execute(sql, value)

        order_id = cursor.lastrowid

        for item in order_items["orders"]:
            cursor.execute("INSERT INTO order_product (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                           (order_id, item["product_id"], item["quantity"]))

        mysql.connection.commit()

        msg = 'Order added successfully!!'

    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return msg


# get orders
@app.route('/orders', methods=['GET'])
def get_orders():
    msg = ''
    all_orders = []

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        user_id = 1
        # create order
        sql = "select id from orders where order_date >= now()-interval 3 month"

        cursor.execute(sql)

        order_ids = cursor.fetchall()
        print(order_ids)

        for order_id in order_ids:
            sql = "select * from order_product join products where %s = order_product.order_id and products.id = order_product.product_id"
            value = (order_id["id"],)
            cursor.execute(sql, value)

            data = cursor.fetchall()
            all_orders.append(data)

        mysql.connection.commit()

        msg = 'Order fetched successfully!!'

    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return jsonify(all_orders)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5001"))
