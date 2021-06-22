#!/usr/bin/python
#-*-coding:utf-8-*-

from flask import *

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    error = None
    return render_template('home.html')

@app.route('/step1', methods=["GET", "POST"])
def step1():
    return render_template('step1.html')

@app.route('/step2', methods=["GET", "POST"])
def step2():
    return render_template('step2.html')

@app.route('/step3', methods=["GET", "POST"])
def step3():
    return render_template('step3.html')

@app.route('/step4', methods=["GET", "POST"])
def step4():
    return render_template('step4.html')
if __name__ == '__main__':
    app.run()