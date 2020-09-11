from flask import Blueprint, session, render_template

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

@article.route('/dashboard/page/<page>')
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



