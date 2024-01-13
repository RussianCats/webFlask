# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:5892@192.168.0.103/oais_web'
    SECRET_KEY = 'd2a32dd5c96845fb890beabd3896f3e0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
