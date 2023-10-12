from flask import Flask, url_for, render_template
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click


WIN = sys.platform.startswith('win')
if WIN:
    # 如果是 windows 平台 前缀是 ///
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对 模型修改 的监控

# 在扩展类实例化 之前加载配置

db = SQLAlchemy(app)


class User(db.Model):
    # 表名将会是user （自动生成 小写处理)
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command()  # 注册命令  可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop')  # 设置选项
def init_db(drop):
    "Initialize the database"
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialize the database")


@app.cli.command()
def forge():
    """生成虚拟数据 并写入到数据库中"""
    db.create_all()

    name = 'BruceChen'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


@app.route('/user/<name>')
def user_page(name):
    return f'User:{escape(name)}'


@app.route('/test')
def test_url_for():
    print(url_for('index'))
    print(url_for('test_url_for'))
    print(url_for('user_page', name='cen'))
    return 'test page'
