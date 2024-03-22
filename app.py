#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask,request,render_template,Markup
import datetime
import sqlite3


# In[2]:


app = Flask(__name__)


# In[ ]:


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

@app.route("/answer",methods = ["GET","POST"])
def answer():
    answer = request.form.get("options")
    if answer.lower() == "true":
        return render_template("wrong.html")
    else:
        return render_template("correct.html")

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
@app.route("/foodexp", methods =  ["GET","POST"])
def foodexp():
    return render_template("foodexp.html")

@app.route("/prediction", methods =  ["GET","POST"])
def prediction():
    income = float(request.form.get("income"))
    expense = income *0.485 + 147.47
    return render_template("prediction.html", expense = expense)

@app.route("/delete",methods = ["GET","POST"])
def deleteDB():
    conn = sqlite3.connect("log.db")
    c = conn.cursor()
    c.execute("DELETE FROM employee;")
    conn.commit()
    c.close()
    conn.close()
    return render_template("deleteDB.html")

@app.route("/end",methods = ["GET","POST"])
def end():
    global name_flag, name
    name_flag = False
    name = ""
    return render_template("end.html")
    
    

if __name__ == "__main__":
    app.run()


# In[ ]:




