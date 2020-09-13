import time

from flask import Blueprint, session, render_template, request, flash, redirect, url_for

from forms import ArticleForm
from mysql_util import MysqlUtil
from utils.my_decorators import is_login_in

article = Blueprint('article', __name__)

#控制台
@article.route('/dashboard')
@is_login_in
def dashboard():
    print()
    # print(session)
    db = MysqlUtil()
    # 根据用户名名查找用户笔记信息
    sql = "SELECT * FROM articles WHERE author = '%s' ORDER BY create_date DESC limit 0,2" % (session['username'])
    result = db.fetchall(sql)  #查找所有笔记

    # print('results',result)
    if result: #如果有笔记，赋值给articles变量，并传回前端
        return render_template('dashboard.html', articles=result, p_list = [x for x in range(1,3)])
    else:
        msg = '暂无笔记信息'
        return render_template('dashboard.html', msg=msg)

# 分页功能
@article.route('/dashboard/page/<int:page>')
@is_login_in
def page(page):
    # 获取数据
    db = MysqlUtil()
    # 根据用户名名查找用户笔记信息
    sql = "SELECT COUNT(*) FROM articles WHERE author = '%s'" % (session['username'])
    result = db.fetchall(sql)  # 查找所有笔记
    page_num = 3 #分页栏显示数量
    half_page_num = int(page_num/2)
    eve_page_data = 2 #每页显示条数
    start_data_num = (int(page) - 1) * page_num #开始显示的条数
    db = MysqlUtil()
    # 根据用户名名查找用户笔记信息
    sql = "SELECT * FROM articles WHERE author = '%s' limit %i,%i" % (session['username'], (int(page)-1)*eve_page_data,eve_page_data)    #从第几条开始，取几条
    response_data = db.fetchall(sql)  # 查找所有笔记
    data_total_count = int(result[0]['COUNT(*)']) #笔记总条数
    s,y = divmod(data_total_count,eve_page_data)
    page_count = s if not y else s+1   #总页数
    #这里待优化
    if page_count <= page_num :
        p_list = [x for x in range(1,page_count+1)]
    elif (int(page) + half_page_num) > page_count :
        p_list = [x for x in range(page_count-page_num,page_count+1)]
    elif (int(page)- half_page_num) <= 0:
        p_list = [x for x in range(1,page_num+1)]
    else:
        p_list = [x for x in range(int(page)-half_page_num, int(page)+half_page_num+1)]


    return render_template('dashboard.html', articles=response_data, p_list=p_list)

# 此处暂时设置不许登陆就可以访问，如果需要显示就加装饰器，和修改sql语句
@article.route('/articles')
def articles():
    db = MysqlUtil()
    sql = 'select * from articles order by create_date desc limit 5' # 从article表中筛选5条数据，并根据日期降序排序
    articles = db.fetchall(sql)
    if articles:
        return render_template('articles.html', articles=articles)
    else:
        msg = '暂无笔记'
        return render_template('articles.html', msg=msg)

@article.route('/art_detail/<string:id>')
@is_login_in
def art_detail(id):
    db = MysqlUtil()
    sql = "select * from articles where id = '%s' " % (id)
    article = db.fetchone(sql)
    return render_template('article.html', article=article)


@article.route('/add_article', methods=['GET', 'POST'])
@is_login_in
def add_article():
    form = ArticleForm(request.form)  # 实例化wtforms的ArticleForm 获取请求值然后进行处理
    if request.method == 'POST' and form.validate():
        # 如果用户提交表单，并且通过验证
        title = form.title.data
        content = form.content.data
        author = session.get('username')
        create_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        db = MysqlUtil()
        sql = 'insert into articles(title,content,author,create_date) values ("%s","%s","%s","%s")' % (title, content, author, create_date)
        db.insert(sql)
        flash('创建成功', 'success') #闪存信息 返回给前端的get_flashed_messages  --> _messages.html
        return redirect(url_for('article.dashboard')) # 添加成功 跳转回控制台展示
    return render_template('add_article.html', form=form) #带着参数渲染模板


@article.route('/edit_article/<string:id>', methods=['POST','GET'])
@is_login_in
def edit_article(id):
    db = MysqlUtil()
    fetch_sql = "SELECT * FROM articles WHERE id = '%s' and author = '%s'" % (id,session['username']) # 根据笔记id查找笔记信息
    article = db.fetchone(fetch_sql) #查找一条记录
    if not article:
        flash('ID错误','danger') # 闪存信息
        return redirect(url_for('article.dashboard'))

    # 获取表单
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = request.form.get('title')
        content = request.form.get('content')
        update_sql = 'update articles set title = "%s", content = "%s" where id = "%s" and author = "%s"' % (title,content,id,session.get('username'))
        db = MysqlUtil()
        db.update(update_sql) #更新到数据库
        flash('更改成功', 'success')
        return redirect(url_for('article.dashboard'))

    form.title.data = article['title']
    form.content.data = article['content']
    return render_template('edit_article.html', form=form)

#删除笔记
@article.route('/delete_article/<string:id>', methods=['POST'])
@is_login_in
def delete_article(id):
    db = MysqlUtil()
    sql = "delete from articles where id = '%s' and author = '%s'" % (id, session.get('username'))
    db.delete(sql)
    flash('删除成功', 'seccess')
    return redirect(url_for('article.dashboard'))







