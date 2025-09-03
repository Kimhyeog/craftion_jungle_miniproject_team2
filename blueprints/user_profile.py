from flask import Blueprint, render_template, abort, request, jsonify
from bson import ObjectId
from datetime import datetime, timezone, timedelta
import jwt
from database import db

profile_bp = Blueprint("user_profile", __name__)

SECRET_KEY = "your-secret-key-here-change-this-in-production"

@profile_bp.route("/profile", methods=['GET'])
def make_profile():
    return render_template("user/mypage.html")

@profile_bp.route("/api/users/<string:_userId>", methods=['GET'])
def get_user_info(_userId):
    user = db.users.find_one({'userId': _userId})
    
    if not user:
        return jsonify({'result': 'fail', 'msg': '사용자를 찾을 수 없습니다.'}), 404

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

@profile_bp.route("/profile/edit", methods=['GET'])
def get_edit_page():
    return render_template("user/mypage_edit.html")

@profile_bp.route("/profile/edit", methods=['POST'])
def post_edit_info():
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

    nickName = request.form.get('nickName', '').strip()
    hobby = request.form.get('hobby', '').strip()
    mbti = request.form.get('mbti', '').strip()
    oneLineIntro = request.form.get('oneLineIntro', '').strip()
    motivate = request.form.get('motivate', '').strip()
    favoriteFood = request.form.get('favoriteFood', '').strip()

    update_doc = {
        'quizInfo.nickName': nickName,
        'quizInfo.hobby': hobby,
        'quizInfo.mbti': mbti,
        'quizInfo.selfIntro': oneLineIntro,
        'quizInfo.selfMotive': motivate,
        'quizInfo.favoriteFood': favoriteFood,
    }

    result = db.users.update_one({'userId': user_id}, {'$set': update_doc})
    if result.matched_count == 0:
        return jsonify({'result': 'fail', 'msg': '사용자를 찾을 수 없습니다.'}), 404

    return jsonify({'result': 'success', 'msg': '수정이 완료되었습니다.'})
