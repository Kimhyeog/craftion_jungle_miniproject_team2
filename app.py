# 필요한 라이브러리 import
from flask import Flask, render_template, jsonify
from database import db

# blueprints 폴더에 있는 모듈들에서 blueprint들을 가져옵니다.
from blueprints.user_profile import profile_bp
from blueprints.auth import auth_bp
from blueprints.quiz import quiz_bp

app = Flask(__name__)

# Blueprint 등록
# url_prefix를 사용하면 이 Blueprint에 등록된 모든 라우트 앞에 '/user'가 붙습니다.
# 예: /profile -> /user/profile
app.register_blueprint(profile_bp, url_prefix="/user")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(quiz_bp, url_prefix="/quiz")

#페이지 라우터

@app.route("/")
def main_page() :
  return render_template("auth/login.html")

# @app.route("/login")
# def login_page():
#   return render_template("auth/login.html")

# @app.route("/signup")
# def signup_page():
#   return render_template("auth/signup.html")

if __name__ == "__main__" :
  app.run("0.0.0.0",port=3000,debug=True)
