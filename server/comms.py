from flask import Blueprint, render_template

comm = Blueprint('comm',__name__)

# 首页展示
@comm.route('/', methods=['GET'])
def index():
    return render_template('home.html')

# 关于我们
@comm.route('/about')
def about():
    return render_template('about.html')