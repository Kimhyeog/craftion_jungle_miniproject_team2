from flask import Blueprint, render_template, abort, request, jsonify
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.yournameis

profile_bp = Blueprint("user_profile", __name__)


@profile_bp.route("/profile", methods=['GET'])
def make_profile():
    return render_template("user/mypage.html")

@profile_bp.route("/profile/edit", methods=['GET'])
def get_edit_page():
    return render_template("user/mypage_edit.html")

@profile_bp.route("/profile/edit", methods=['POST'])
def post_edit_info():
    return (1)

@profile_bp.route("/api/users/<string:db_id>", methods=['GET'])
def get_user_info(db_id):

    if not ObjectId.is_valid(db_id) :
        abort(400)

    user = db.users.find_one({'_id':ObjectId(db_id)})
    
    if not user:
        abort(404, description="user not found")

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
