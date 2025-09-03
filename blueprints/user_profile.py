from flask import Blueprint, render_template, abort, request, jsonify
from bson import ObjectId
from datetime import datetime, timezone, timedelta
import jwt
# 독립적인 MongoClient 연결 대신, 공유되는 db 객체를 가져옵니다.
from database import db

# Blueprint 이름은 그대로 사용하되, 파일 위치가 바뀌었습니다.
profile_bp = Blueprint("user_profile", __name__)

# JWT 시크릿 키 (auth.py와 동일해야 함)
SECRET_KEY = "your-secret-key-here-change-this-in-production"


# 참고: app.py에서 url_prefix="/user"를 설정했기 때문에,
# 이 라우트의 실제 접속 주소는 '/user/profile'이 됩니다.
# --- 마이페이지 렌더링 함수를 수정합니다 ---
@profile_bp.route("/profile", methods=['GET'])
def make_profile():
    # JWT 기반으로 클라이언트가 /user/api/me를 호출하므로 쿼리 id가 필요 없습니다.
    return render_template("user/mypage.html")


#  db아이디 대신 userId로 변경 
# --- get_user_info 함수를 좀 더 안전하게 수정합니다 (오류 방지) ---
@profile_bp.route("/api/users/<string:_userId>", methods=['GET'])
def get_user_info(_userId):
    # userId는 단순 문자열이므로 ObjectId 검증을 하지 않습니다.
    user = db.users.find_one({'userId': _userId})
    
    if not user:
        return jsonify({'result': 'fail', 'msg': '사용자를 찾을 수 없습니다.'}), 404

    # .get() 메소드를 사용하면 해당 키가 없을 때 오류 대신 기본값(None 또는 [])을 반환하여 더 안전합니다.
    quiz_info = user.get('quizInfo', {})
    return jsonify({
        'result': 'success',
        'userName': user.get('userName'),
        'nickName': quiz_info.get('nickName'),
        'profilePhoto': quiz_info.get('profilePhoto'),
        'selfIntro': quiz_info.get('selfIntro'),
        'selfMotive': quiz_info.get('selfMotive'),
        'favoriteFood': quiz_info.get('favoriteFood'),
        'hobby': quiz_info.get('hobby'),
        'mbti': quiz_info.get('mbti'),
        'userWhoSolvedMe': user.get('userWhoSolvedMe', []),
        'usersISolved': user.get('usersISolved', []),
        'userWhoSolvedMeCount': user.get('userWhoSolvedMeCount', 0),
        'usersISolvedCount': user.get('usersISolvedCount', 0)
    })

# 현재 로그인한 사용자 정보 (JWT 필요)
@profile_bp.route("/api/me", methods=['GET'])
def get_my_profile():
    token = request.cookies.get('mytoken')
    if not token:
        return jsonify({'result': 'fail', 'msg': '로그인이 필요합니다.'}), 401

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('id')
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'}), 401
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '유효하지 않은 토큰입니다.'}), 401

    if not user_id:
        return jsonify({'result': 'fail', 'msg': '토큰에 사용자 정보가 없습니다.'}), 400

    user = db.users.find_one({'userId': user_id})
    if not user:
        return jsonify({'result': 'fail', 'msg': '사용자를 찾을 수 없습니다.'}), 404

    quiz_info = user.get('quizInfo', {})
    return jsonify({
        'result': 'success',
        'userId': user.get('userId'),
        'userName': user.get('userName'),
        'nickName': quiz_info.get('nickName'),
        'profilePhoto': quiz_info.get('profilePhoto'),
        'selfIntro': quiz_info.get('selfIntro'),
        'selfMotive': quiz_info.get('selfMotive'),
        'favoriteFood': quiz_info.get('favoriteFood'),
        'hobby': quiz_info.get('hobby'),
        'mbti': quiz_info.get('mbti'),
        'userWhoSolvedMe': user.get('userWhoSolvedMe', []),
        'usersISolved': user.get('usersISolved', []),
        'userWhoSolvedMeCount': user.get('userWhoSolvedMeCount', 0),
        'usersISolvedCount': user.get('usersISolvedCount', 0)
    })

# 실제 접속 주소: '/user/profile/edit'
@profile_bp.route("/profile/edit", methods=['GET'])
def get_edit_page():
    return render_template("user/mypage_edit.html")

@profile_bp.route("/profile/edit", methods=['POST'])
def post_edit_info():
    # 여기에 프로필 수정 로직을 구현하면 됩니다.
    # 예: nickName = request.form['nickName']
    #     db.users.update_one(...)
    return jsonify({'result': 'success', 'msg': '수정이 완료되었습니다.'})

# # 실제 접속 주소: '/user/api/users/<db_id>'
# @profile_bp.route("/api/users/<string:db_id>", methods=['GET'])
# def get_user_info(db_id):

#     if not ObjectId.is_valid(db_id):
#         abort(400, description="Invalid user ID format")

#     # 공유된 db 객체를 사용하여 'users' 컬렉션에 쿼리합니다.
#     user = db.users.find_one({'_id': ObjectId(db_id)})
    
#     if not user:
#         abort(404, description="User not found")

#     # 기존 로직과 동일
#     return jsonify({
#         'result': 'success',
#         'userName': user['userName'],
#         'nickName': user['quizInfo']['nickName'],
#         'profilePhoto': user['quizInfo']['profilePhoto'],
#         'selfIntro': user['quizInfo']['selfIntro'],
#         'selfMotive': user['quizInfo']['selfMotive'],
#         'favoriteFood': user['quizInfo']['favoriteFood'],
#         'hobby': user['quizInfo']['hobby'],
#         'mbti': user['quizInfo']['mbti'],
#         'userWhoSolvedMe': user['userWhoSolvedMe'],
#         'usersISolved': user['usersISolved'],
#         'userWhoSolvedMeCount': user['userWhoSolvedMeCount'],
#         'usersISolvedCount': user['usersISolvedCount']
#     })
