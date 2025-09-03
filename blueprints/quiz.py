from flask import Blueprint, render_template, request, jsonify
from database import db

# Quiz Blueprint 생성
quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route("/list")
def quiz_list():
   
        users = list(db.users.find({}, {'quizInfo': 1, 'userId': 1}))
    
        return render_template("quiz/list.html", users=users )


@quiz_bp.route("/dashboard")
def quiz_dashboard():
    """퀴즈 대시보드 페이지"""
    return render_template("quiz/dashboard.html")
