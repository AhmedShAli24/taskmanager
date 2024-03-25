import os
from flask import Flask,render_template,redirect,url_for,request
from datetime import datetime,timezone
from dotenv import find_dotenv, load_dotenv
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

dotenv_path = find_dotenv()
load_dotenv()

mysql = MySQL(app)

app.config['MYSQL_HOST'] = os.getenv("host")
app.config['MYSQL_USER'] = os.getenv("user")
app.config['MYSQL_PASSWORD'] = os.getenv("data_pass")
app.config['MYSQL_DB'] = os.getenv("db")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

@app.route('/', methods=["GET","POST"])
def index():
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    if request.method == "POST":
        date = datetime.now(timezone.utc)
        task = request.form.get("task")
        conn.execute('INSERT into tasks VALUES (NULL, %s, %s, %s)',(task,0 ,date,))
        mysql.connection.commit()
        return redirect(url_for('index'))
    conn.execute("SELECT * from tasks")
    all_tasks = conn.fetchall()
    return render_template("index.html", all_tasks =all_tasks)

@app.route('/update/<int:id>', methods=["POST","GET"])
def update(id):
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    conn.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    one_task =conn.fetchone()
   
    if request.method == "POST":
        task = request.form.get("task")
        date = datetime.now(timezone.utc)
        options = request.form.get("options")
        if options == "Completed":
            options = 1
        else:
            options = 0
        conn.execute("UPDATE tasks SET description = %s, completed = %s, date_created = %s WHERE id = %s", (task, options, date, id,))
        mysql.connection.commit()
        return redirect(url_for("index")) 
     
    return render_template('update.html',one_task = one_task)

@app.get('/delete/<int:id>')
def delete(id):
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute('DELETE FROM tasks WHERE id = %s',(id,)) 
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)