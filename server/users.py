from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from passlib.hash import sha256_crypt

from forms import RegisterForm
from mysql_util import MysqlUtil
from utils.my_decorators import is_login_in

user = Blueprint('user', __name__)

# 用户注册
@user.route('/register', methods=['GET','POST'])
def register():
    re_form = RegisterForm(request.form)

    if request.method == 'POST' and re_form.validate():
        # 判断请求方式，和字段是否符合要求
        db1 = MysqlUtil()
        # 实例化数据库操作类，并将数据插入数据库
        username = re_form.username.data
        print(username)
        print(type(username))
        re_sql = 'select * from users where username = "%s"' % (username)
        result = db1.fetchone(re_sql) # 获取记录
        print(result)
        if not result:
        # 判断用户名是否已经被注册
            db = MysqlUtil()
            email = re_form.email.data
            password = sha256_crypt.encrypt(str(re_form.password.data))
        # 对密码进行加密
            sql = "INSERT INTO users(email,username,password) \
                       VALUES ('%s', '%s', '%s')" % (email, username, password)  # user表中插入记录
        # 写sql语句
            db.insert(sql)
            flash('您已注册成功，请先登录','success') # 闪存信息
            # return redirect(url_for('login')) #跳转到登陆页面
            return redirect('/login')
        else:
            flash('用户名已经存在，请重新输入','false')
            return render_template('register.html', form=re_form)
    else:
        return render_template('register.html', form=re_form) #模板渲染


@user.route('/login', methods=['POST', 'GET'])
def login():
    if 'login_in' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST': #提过请求为post提交表单
        username = request.form.get('username')
        password_candidate = request.form.get('password')
        sql = 'select * from users where username = "%s"' % (username) #查找用户名信息
        db = MysqlUtil()
        result = db.fetchone(sql)
        if result:
            password = result.get('password')
            if sha256_crypt.verify(password_candidate,password):
                # 写入session
                session['logged_in'] = True
                session['username'] = username
                session['email'] = result.get('email') #暂时无用，后续涉及修改邮件使用
                print(session)
                flash('登陆成功！', 'success') #闪存信息
                return redirect(url_for('article.dashboard')) #跳转到控制台
                # return redirect('/dashboard') #跳转到控制台
            else: # 密码错误
                error = '用户名密码不匹配'
                return render_template('login.html', error=error)
        else:
            error = '用户名不存在'
            return render_template('login.html',error=error)
    return render_template('login.html')

@user.route('/logout')
@is_login_in
def logout():
    session.clear()
    flash('您已经注销', 'success')
    return redirect(url_for('user.login'))

