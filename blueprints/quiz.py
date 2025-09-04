from flask import Blueprint, render_template, request, jsonify
from flask import redirect, url_for
from database import db
from bson import ObjectId
import math
import jwt
from blueprints.auth import page_auth_required

quiz_bp = Blueprint('quiz', __name__)

SECRET_KEY = "your-secret-key-here-change-this-in-production"

def get_current_user_id():
    token = request.cookies.get('mytoken')
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('id')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

@quiz_bp.route("/list")
@page_auth_required
def quiz_list():
    page = request.args.get('page', 1, type=int)
    search_keyword = request.args.get('search', '', type=str)
    limit = 8

    query = {'quizInfo': {'$exists': True}}

    if search_keyword:
        regex = {'$regex': search_keyword, '$options': 'i'}
        query['$and'] = [
            {
                '$or': [
                    {'quizInfo.nickName': regex},
                    {'quizInfo.selfIntro': regex},
                    {'quizInfo.mbti': regex},
                    {'quizInfo.hobby': regex},
                    {'quizInfo.favoriteFood': regex}
                ]
            }
        ]
    
    query['userWhoSolvedMeCount'] = 0
    
    current_user_id = get_current_user_id()
    if current_user_id:
        query['userId'] = {'$ne': current_user_id}
    
    total_users = db.users.count_documents(query)
    total_pages = math.ceil(total_users / limit)
    skip_count = (page - 1) * limit
    
    users = list(db.users.find(query).skip(skip_count).limit(limit))

    return render_template(
        "quiz/list.html",
        users=users,
        total_pages=total_pages,
        current_page=page,
        search_keyword=search_keyword
    )

@quiz_bp.route("/usr/<string:_userId>")
def change_userid_to_dbid(_userId):
  print ("in herre")
  user = db.users.find_one({'userId': _userId})
  return redirect(url_for('quiz.quiz_dashboard', db_id=str(user['_id'])))

@quiz_bp.route("/dashboard/<string:db_id>")
@page_auth_required
def quiz_dashboard(db_id):
  if not ObjectId.is_valid(db_id):
    return "Invalid user ID format", 400

  user = db.users.find_one({'_id': ObjectId(db_id)})
  
  if not user:
      return redirect(url_for('quiz.quiz_list'))

  if user.get('userWhoSolvedMeCount', 0) != 0:
    return redirect(url_for('quiz.quiz_list'))

  return render_template(
    "quiz/dashboard.html", 
    nickName = user['quizInfo']['nickName'],
    profilePhoto = user['quizInfo']['profilePhoto'],
    selfIntro = user['quizInfo']['selfIntro'],
    selfMotive = user['quizInfo']['selfMotive'],
    favoriteFood = user['quizInfo']['favoriteFood'],
    mbti = user['quizInfo']['mbti'],
    hobby = user['quizInfo']['hobby'],
    correctName = user['userName'], 
    targetId = user['userId']
  )

@quiz_bp.route("/api/quiz_solved", methods=['POST'])
def update_db_after_quiz_solved() :
   solverId = request.form.get("_solverId")
   targetId = request.form.get("_targetId")

   db.users.update_one(
      {'userId':solverId}, 
      {
        "$addToSet": {"usersISolved": targetId},
        "$inc": {"usersISolvedCount" : 1}
      }
    )
   db.users.update_one(
      {'userId':targetId}, 
      {
        "$set": {"userWhoSolvedMe" : solverId},
        "$inc": {"userWhoSolvedMeCount": 1}
      }
   )

   return jsonify({"result" : "success"})