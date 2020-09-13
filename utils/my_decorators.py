from functools import wraps

from flask import session, flash, url_for, redirect


# 验证是否登录的装饰器
def is_login_in(func):
    @wraps(func)
    def inner(*args, **kwargs):
        # print('这里是装饰器',session.get('logged_in'))
        if session.get('logged_in'):
            return func(*args, **kwargs)
        else:
            flash('无权访问，请先登录','danger')
            return redirect(url_for('user.login'))
    return inner

# 分页功能
class PagingFunc():
    def __init__(self,page_num,total_count):
        pass