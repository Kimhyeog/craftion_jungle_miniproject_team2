from flask import Blueprint, render_template
from database import db

# Quiz Blueprint 생성
quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route("/list")
def quiz_list():
    """유저 목록 페이지 - DB에서 모든 유저의 quizInfo를 가져와서 카드로 표시"""
    # DB에서 모든 유저의 quizInfo 데이터를 가져옵니다
    users = list(db.users.find({}, {'quizInfo': 1, 'userId': 1}))
    return render_template("quiz/list.html", users=users)

@quiz_bp.route("/dashboard")
def quiz_dashboard():
    """퀴즈 대시보드 페이지"""
    return render_template("quiz/dashboard.html")
