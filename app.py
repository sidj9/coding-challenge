# -*- coding: utf-8 -*-
"""
Created on Fri Aug 02 13:26:53 2019

@author: siddh
"""

from flask import Flask, render_template, request ,redirect, url_for
from flask.ext.mysql import MySQL
app = Flask(__name__)

# Configure db
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'flaskapp'



mysql.init_app(app)

@app.route("/", methods=['GET', 'Post'])
def main():
    conn = mysql.connect()
    cur = conn.cursor()
    resultValue = cur.execute("SELECT * FROM courses")
    if resultValue > 0:
       # page = request.args.get('page', 1, type = int)
        courseDetails = cur.fetchall()
    return render_template('index.html',courseDetails = courseDetails)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        courseDetails = request.form
        title = courseDetails['title']
        desc = courseDetails['desc']
        duration = courseDetails['duration']
        start = courseDetails['start']
        end = courseDetails['end']
        prof = courseDetails['prof']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO courses(course_title, course_desc, course_duration, course_startDate, course_endDate, course_prof) VALUES(%s, %s, %s, %s, %s, %s)",(title,desc,duration,start,end,prof))
        conn.commit()
        cur.close()
        return redirect(url_for('main'))
    return render_template('add.html')

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        courseDetails = request.form
        course_id = courseDetails['id']
        title = courseDetails['title']
        prof = courseDetails['prof']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("UPDATE courses SET course_title=%s, course_prof=%s WHERE course_id=%s", (title,prof,course_id))
        conn.commit()
        cur.close()
        return redirect(url_for('main'))
    return render_template('update.html')

@app.route('/remove', methods=['GET','POST'])
def remove():
    if request.method == 'POST':
        courseDetails = request.form
        course_id = courseDetails['id']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM courses WHERE course_id = %s", (course_id))
        conn.commit()
        cur.close()
        return redirect(url_for('main'))
    return render_template('remove.html')


    
    
    
  
    


if __name__ == "__main__":
    app.run(debug=True )