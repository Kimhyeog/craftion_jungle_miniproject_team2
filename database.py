# database.py
from pymongo import MongoClient

# MongoDB 클라이언트를 한번만 생성합니다.
client = MongoClient('localhost', 27017)

# 'dbNameSns' 데이터베이스 객체를 db 변수에 할당합니다.
# 이제 다른 파일에서는 이 'db' 객체를 import해서 사용하면 됩니다.
db = client["yournameis"]