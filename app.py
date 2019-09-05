import os
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def start():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
