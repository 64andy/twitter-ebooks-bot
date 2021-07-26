from flask import Flask, render_template
from multiprocessing import Process
app = Flask('')


errors = []


@app.route('/')
def home():
    return render_template("index.html", errors=errors)

def run():
  app.run(host='localhost', port=8080)

def run_server():  
    t = Process(target=run)
    t.start()
    return t
