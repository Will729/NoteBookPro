# 创建Flask Debug模式相关配置
class DebugConfig(object):
    DEBUG = True
    SECRET_KEY = 'tianyi!@$@$#@$#@%$@%$'
    PERMANENT_SESSION_LIFETIME = 3600
    SESSION_COKKIE_NAME = 'MY SESSION'

# Flask Test模式相关配置
class TestConfig(object):
    pass

