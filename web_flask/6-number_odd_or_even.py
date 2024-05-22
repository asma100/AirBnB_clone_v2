#!/usr/bin/python3
"""A simple Flask web application with multiple routes"""
from flask import Flask
from markupsafe import escape
from flask import render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def show_c_text(text):
    text = text.replace('_', ' ')
    return f'C {text}'


@app.route("/python/", defaults={'text': 'is cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def show_python_text(text):
    text = text.replace('_', ' ')
    return f'Python {text}'


@app.route('/number/<int:n>', strict_slashes=False)
def handle_number(n):
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def handle_number_html(n):
    return render_template('6-number_odd_or_even.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def handle_number_evodd(n):
    if n % 2 == 0:
        type = "even"
    else:
        type = "odd"
    return render_template('6-number_odd_or_even.html', number=n, type=type)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
