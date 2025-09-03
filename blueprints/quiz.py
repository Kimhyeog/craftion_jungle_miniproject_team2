from flask import Blueprint, render_template, request, jsonify
from database import db
from bson import ObjectId

# Quiz Blueprint 생성
quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route("/list")
def quiz_list():
   
        users = list(db.users.find({}, {'quizInfo': 1, 'userId': 1}))
    
        return render_template("quiz/list.html", users=users )


@quiz_bp.route("/dashboard/<string:db_id>")
def quiz_dashboard(db_id):
  if not ObjectId.is_valid(db_id):
    return "Invalid user ID format", 400

  user = db.users.find_one({'_id': ObjectId(db_id)})
  
  if (user['userWhoSolvedMeCount'] != 0) :
    return render_template("quiz/list.html")

  # print(user['userName'])

  return render_template(
    "quiz/dashboard.html", 
    nickName = user['quizInfo']['nickName'],
    profilePhoto = user['quizInfo']['profilePhoto'],
    selfIntro = user['quizInfo']['selfIntro'],
    selfMotive = user['quizInfo']['selfMotive'],
    favoriteFood = user['quizInfo']['favoriteFood'],
    mbti = user['quizInfo']['mbti'],
    hobby = user['quizInfo']['hobby'],
    correctName = user['userName']
  )
