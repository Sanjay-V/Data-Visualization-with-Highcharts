import os
from flask import Flask, render_template, make_response, request
import sys
import logging
from time import time
import json
from random import random
import sqlite3
from sqlite3 import Error
import zenv

database = zenv.DB_LOCATION


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_by_Name_1(conn, name_1):
    """
    Query all rows in the MOVIE table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    name_obj = {
        'name_1': name_1
    }
    cur.execute(
        "SELECT * FROM POPULATIONS WHERE CountryName = :name_1", name_obj)

    rows = cur.fetchall()
    return rows


def select_by_Name_2(conn, name_2):
    """
    Query all rows in the MOVIE table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    name_obj = {
        'name_2': name_2
    }
    cur.execute(
        "SELECT * FROM POPULATIONS WHERE CountryName = :name_2", name_obj)

    rows = cur.fetchall()
    return rows

    # print('rows count : '+str(len(rows)))

   # if(len(rows) <= 0):
    #    print('No Data available')

    # for row in rows:
    #   print(row)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/<name_1>', methods=["GET", "POST"])
def data_1(name_1):

    # Data Format
    # [TIME, Temperature, Humidity]

    #Temperature = random() * 100
    #Humidity = random() * 55

    #data = [time() * 1000, Temperature, Humidity]

    conn = create_connection(database)
    with conn:
        rows = select_by_Name_1(conn, name_1)

    response = make_response(json.dumps(rows))
    response.content_type = 'application/json'
    print(response.data)
    return response


'''
@app.route('/data/<name_2>', methods=["GET", "POST"])
def data_2(name_2):

    # Data Format
    # [TIME, Temperature, Humidity]

    #Temperature = random() * 100
    #Humidity = random() * 55

    #data = [time() * 1000, Temperature, Humidity]

    conn = create_connection(database)
    with conn:
        rows = select_by_Name_2(conn, name_2)

    response = make_response(json.dumps(rows))
    response.content_type = 'application/json'
    print(response.data)
    return response
'''
# @app.route('/getData', methods = ["GET"])
# def getData():


@app.route('/highchart', methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        conn = create_connection(database)
        name_1 = request.form['name_1']
        name_2 = request.form['name_2']
        name1_list = json.dumps(select_by_Name_1(conn, name_1))
        name2_list = json.dumps(select_by_Name_2(conn, name_2))

    return render_template('test.html', name_1=name_1, name_2=name_2, name1_list=name1_list, name2_list=name2_list)
    # return render_template('graph.html', name_2=name_2)

if __name__ == '__main__':
    app.debug = True
    app.run()
