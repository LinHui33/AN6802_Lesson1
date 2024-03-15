#!/usr/bin/env python
# coding: utf-8

from flask import Flask,request,render_template,Markup
import datetime
import sqlite3

app = Flask(__name__)


name_flag = False
name = ""

@app.route("/",methods = ["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/main",methods = ["GET","POST"])
def main():
    global name_flag, name
    if name_flag == False:
        name = request.form.get("name")
        name_flag = True
        
        conn = sqlite3.connect("log.db")
        c = conn.cursor()
        current_dateTime = datetime.datetime.now()
        c.execute("INSERT INTO employee (name, timestamp) VALUES (?, ?)", (name, current_dateTime))
        conn.commit()
        c.close()
        conn.close()
    
    return render_template("main.html", name = name)
@app.route("/ethical_test",methods = ["GET","POST"])
def ethical_test():
    return render_template("ethical_test.html")

@app.route("/query",methods = ["GET","POST"])
def query():
    conn = sqlite3.connect("log.db")
    results = conn.execute("select * from employee")
    output = ""
    for row in results:
        output = output + str(row) + "<br>"
    output = Markup(output)
    conn.close()
    return render_template("query.html", text = output)

@app.route("/answer",methods = ["GET","POST"])
def answer():
    answer = request.form.get("options")
    if answer.lower() == "true":
        return render_template("wrong.html")
    else:
        return render_template("correct.html")

@app.route("/end",methods = ["GET","POST"])
def end():
    global name_flag, name
    name_flag = False
    name = ""
    return render_template("end.html")
    
    

if __name__ == "__main__":
    app.run()




