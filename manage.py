from flask import Flask

from server.articles import article
from server.comms import comm
from server.users import user
from settings import DebugConfig


# 创建应用
app = Flask(__name__)

app.register_blueprint(comm)
app.register_blueprint(user)
app.register_blueprint(article)


if __name__ == '__main__':
    # app.secret_key = 'tianyi'
    app.config.from_object(DebugConfig)
    # app.run(debug=True)
    app.run('0.0.0.0',9527)