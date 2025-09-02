# 필요한 라이브러리 import
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")  # 인증 비활성화 상태
db = client["dbNameSns"]
posts = db["posts"]

@app.route("/")
def mainPage() :
  return render_template("index.html")

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