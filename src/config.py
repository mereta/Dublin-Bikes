# See http://flask.pocoo.org/docs/0.12/config/  for flask config options.


class DevelopmentConfig:
    DEBUG = True


class ProductionConfig:
    DEBUG = False
    SERVER_NAME = "127.0.0.1:80"
