from flask import *

app = FLASK(__name__)

@app.route('/home', methods=["GET", "POST"])

@app.route('/step1', methods=["GET", "POST"])

@app.route('/step2', methods=["GET", "POST"])

@app.route('/step3', methods=["GET", "POST"])

@app.route('/step4', methods=["GET", "POST"])

if __name__ == '__main__':
    app.run()