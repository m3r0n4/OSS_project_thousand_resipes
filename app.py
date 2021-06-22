#!/usr/bin/python
#-*-coding:utf-8-*-

from flask import *

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route('/step1', methods=["GET", "POST"])
def step1():
    error = None
    return render_template('step1.html')

@app.route('/step2', methods=["GET", "POST"])
def step2():
    error = None
    if request.method == 'POST':
        gri1 = request.form['gri1']
        gri2 = request.form['gri2']
        gri3 = request.form['gri3']
        return render_template('step2.html', gri1 = gri1, gri2 = gri2, gri3 = gri3)
    else:
        gri1 = request.args.get['gri1']
        gri2 = request.args.get['gri2']
        gri3 = request.args.get['gri3']
        return render_template('step2.html', gri1 = gri1, gri2 = gri2, gri3 = gri3)

@app.route('/step3', methods=["GET", "POST"])
def step3():
    error = None
    if request.method == 'POST':
        gri1 = request.form['gri1']
        gri2 = request.form['gri2']
        gri3 = request.form['gri3']
        cate = request.form['cate']
        return render_template('step3.html', gri1 = gri1, gri2 = gri2, gri3 = gri3, cate = cate)
    else:
        gri1 = request.args.get['gri1']
        gri2 = request.args.get['gri2']
        gri3 = request.args.get['gri3']
        cate = request.args.get['cate']
        return render_template('step3.html', gri1 = gri1, gri2 = gri2, gri3 = gri3 cate = cate)

if __name__ == '__main__':
    app.run()