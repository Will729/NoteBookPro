from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#Article Form Class
# 创建文章类
class ArticleForm(Form):
    title = StringField(
        '标题',
        validators=[

            DataRequired(message='标题长度应该在2-30字符串之间'),
            Length(min=2, max=30)
        ]
    )

    content = TextAreaField(
        '内容',
        validators=[
            DataRequired(message='长度不少于5个字符串'),
            Length(min=5)
        ]
    )

# 创建用户注册类
class RegisterForm(Form):
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='请输入用户名'),
            Length(min=2, max=25, message='用户名长度为2-25个字符')
        ]
    )

    email = StringField(
        '邮箱',
        validators=[
            DataRequired(message='请输入邮箱'),
            Email(message='请输入正确的邮箱格式')
        ]
    )

    password = PasswordField(
        '密码',
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=8, max=16, message='长度在8-16个字符串之间')
        ]
    )

    confirm = PasswordField(
        '确认密码',
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=8, max=16,message='长度在8-16个字符串之间'),
            EqualTo('password', message='两次输入密码不一致，请重新输入')
        ]
    )
