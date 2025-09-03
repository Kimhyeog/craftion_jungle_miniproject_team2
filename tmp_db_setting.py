from flask import Blueprint, render_template, abort, request, jsonify
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.yournameis

from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('localhost', 27017)
db = client.yournameis

# 1번과 2번 유저 불러오기
user1 = db.users.find_one({'userId': 'user1'})
user2 = db.users.find_one({'userId': 'user2'})

if user1 and user2:
    # 1번 유저 (문제 출제자) 정보 수정
    db.users.update_one(
        {'_id': user1['_id']},
        {
            '$set': {
                'userWhoSolvedMe': str(user2['_id']),
                'userWhoSolvedMeCount': 1
            }
        }
    )

    # 2번 유저 (문제 맞춘 사람) 정보 수정
    db.users.update_one(
        {'_id': user2['_id']},
        {
            '$set': {
                'usersISolved': [str(user1['_id'])],
                'usersISolvedCount': 1
            }
        }
    )

    print("✅ user2가 user1의 문제를 맞춘 상태로 반영 완료!")
else:
    print("❌ user1 또는 user2가 존재하지 않습니다.")
