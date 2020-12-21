import os
import mysql.connector
from flask import Flask, jsonify, make_response, render_template
from flask_cors import CORS


from dotenv import load_dotenv
load_dotenv()

myDB = mysql.connector.connect(
    host=os.environ.get("host"),
    user=os.environ.get("user"),
    password=os.environ.get("password"),
    port=os.environ.get("port"),
    database='PROJECT'
)


my_cursor = myDB.cursor()

app = Flask(__name__)
CORS(app)


@app.route('/')
def show_view():
    answer = []
    my_cursor.execute("SHOW DATABASES")
    for x in my_cursor:
        for y in x:
            if y not in ["mysql", "information_schema", "performance_schema"]:
                answer.append(y)

    return render_template('index.html', info=f"/mysql/{answer[0]}")


@app.route("/mysql/command/")
def command():
    return render_template('command.html')


@app.route('/mysql/')
def mysql_viz():
    answer = []
    my_cursor.execute("SHOW DATABASES")
    for x in my_cursor:
        for y in x:
            if y not in ["mysql", "information_schema", "performance_schema"]:
                answer.append(y)
    return make_response(
        jsonify(
            {
                "databases": answer
            }
        )
    )


@app.route('/mysql/<database>/')
def get_db(database):
    answer = []
    my_cursor.execute(f"USE {database}")
    my_cursor.execute("SHOW TABLES")
    for x in my_cursor:
        for y in x:
            answer.append(y)

    return make_response(
        jsonify(
            {
                f"tables_in_{database}": answer
            }
        )
    )


@app.route('/mysql/<database>/<table>/')
def mysql_table(database, table):
    answer = []
    my_cursor.execute(f"USE {database}")
    my_cursor.execute(f"SELECT * FROM {table}")
    column_name = [i[0] for i in my_cursor.description]

    for x in my_cursor:
        empty = {}
        for y in range(len(x)):
            empty[column_name[y]] = x[y]
        answer.append(empty)

    return make_response(
        jsonify(
            {
                f"{table}": answer
            }
        )
    )


@app.route('/mysql/post/<command>/')
def post_command(command):
    try:
        my_cursor.execute(command)
        for x in my_cursor:
            print(x)
        print(command)
        return command, 200
    except Exception as err:
        print(err.msg)
        return err.msg, 400
