# 필요한 라이브러리 import
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

from user_profile import profile_bp  # 프로필 페이지 blueprint 불러오기 

app = Flask(__name__)
app.register_blueprint(profile_bp)


client = MongoClient("mongodb://localhost:27017")  # 인증 비활성화 상태
db = client["dbNameSns"]
posts = db["posts"]

#페이지 라우터

@app.route("/")
def main_page() :
  return render_template("main.html")

@app.route("/login")
def login_page():
  return render_template("auth/login.html")

@app.route("/signup")
def signup_page():
  return render_template("auth/signup.html")

@app.route("/profile")
def mypage():
  return render_template("user/mypage.html")

@app.route("/quiz")
def quiz_list():
  return render_template("quiz/list.html")

@app.route("/dashboard")
def quiz_dashboard():
  return render_template("quiz/dashboard.html")


if __name__ == "__main__" :
  app.run("0.0.0.0",port=3000,debug=True)
