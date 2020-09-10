from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt

from mysql_util import MysqlUtil
from forms import RegisterForm, ArticleForm
from settings import DebugConfig
from server.comms import comm
from server.users import user


# 创建应用
app = Flask(__name__)

app.register_blueprint(comm)
app.register_blueprint(user)


if __name__ == '__main__':
    # app.secret_key = 'tianyi'
    app.config.from_object(DebugConfig)
    # app.run(debug=True)
    app.run('0.0.0.0',9527)