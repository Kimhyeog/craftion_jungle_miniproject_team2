from flask import Blueprint, render_template, abort, request, jsonify
from bson import ObjectId
# 독립적인 MongoClient 연결 대신, 공유되는 db 객체를 가져옵니다.
from database import db

# Blueprint 이름은 그대로 사용하되, 파일 위치가 바뀌었습니다.
profile_bp = Blueprint("user_profile", __name__)


# 참고: app.py에서 url_prefix="/user"를 설정했기 때문에,
# 이 라우트의 실제 접속 주소는 '/user/profile'이 됩니다.
@profile_bp.route("/profile", methods=['GET'])
def make_profile():
    return render_template("user/mypage.html")

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

# 실제 접속 주소: '/user/api/users/<db_id>'
@profile_bp.route("/api/users/<string:db_id>", methods=['GET'])
def get_user_info(db_id):

    if not ObjectId.is_valid(db_id):
        abort(400, description="Invalid user ID format")

    # 공유된 db 객체를 사용하여 'users' 컬렉션에 쿼리합니다.
    user = db.users.find_one({'_id': ObjectId(db_id)})
    
    if not user:
        abort(404, description="User not found")

    # 기존 로직과 동일
    return jsonify({
        'result': 'success',
        'userName': user['userName'],
        'nickName': user['quizInfo']['nickName'],
        'profilePhoto': user['quizInfo']['profilePhoto'],
        'selfIntro': user['quizInfo']['selfIntro'],
        'selfMotive': user['quizInfo']['selfMotive'],
        'favoriteFood': user['quizInfo']['favoriteFood'],
        'hobby': user['quizInfo']['hobby'],
        'mbti': user['quizInfo']['mbti'],
        'userWhoSolvedMe': user['userWhoSolvedMe'],
        'usersISolved': user['usersISolved'],
        'userWhoSolvedMeCount': user['userWhoSolvedMeCount'],
        'usersISolvedCount': user['usersISolvedCount']
    })
