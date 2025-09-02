# 필요한 라이브러리 import
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
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

@app.route("/mypage")
def mypage():
  return render_template("user/mypage.html")

@app.route("/quiz")
def quiz_list():
  return render_template("quiz/list.html")

@app.route("/dashboard")
def quiz_dashboard():
  return render_template("quiz/dashboard.html")


  # DB 실험용 라우터 GET

@app.route("/api/posts", methods=["GET"])
def list_posts() :
  data = list(posts.find({}, {"_id": 0}))
  return jsonify(data)


  # DB 실험용 라우터 post
@app.route("/api/posts", methods=["POST"])
def create_post() :
  body = request.get_json(silent=True) or {}
  doc = {"title": body.get("title", ""), "content": body.get("content", "")}
  posts.insert_one(doc)
  return jsonify({"ok": True}), 201



if __name__ == "__main__" :
  app.run("0.0.0.0",port=3000,debug=True)