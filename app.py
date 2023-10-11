from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'


@app.route('/user/<name>')
def user_page(name):
    return f'User:{escape(name)}'


@app.route('/test')
def test_url_for():
    print(url_for('index'))
    print(url_for('test_url_for'))
    print(url_for('user_page', name='cen'))
    return 'test page'
