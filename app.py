# 필요한 라이브러리 import
from flask import Flask, render_template

# blueprints 폴더에 있는 user_profile 모듈에서 profile_bp를 가져옵니다.
from blueprints.user_profile import profile_bp
from blueprints.auth import auth_bp  # 'profile_bp'를 'auth_bp'로 수정했습니다!

app = Flask(__name__)

# Blueprint 등록
# url_prefix를 사용하면 이 Blueprint에 등록된 모든 라우트 앞에 '/user'가 붙습니다.
# 예: /profile -> /user/profile
app.register_blueprint(profile_bp, url_prefix="/user")

# 2. auth 블루프린트 등록
# profile_bp를 auth_bp로 바꿔주세요.
app.register_blueprint(auth_bp, url_prefix="/auth") # <- 이렇게 auth_bp로 수정해야 합니다.

#페이지 라우터

@app.route("/")
def main_page() :
  return render_template("main.html")

# @app.route("/login")
# def login_page():
#   return render_template("auth/login.html")

# @app.route("/signup")
# def signup_page():
#   return render_template("auth/signup.html")


@app.route("/quiz")
def quiz_list():
  return render_template("quiz/list.html")

@app.route("/dashboard")
def quiz_dashboard():
  return render_template("quiz/dashboard.html")


if __name__ == "__main__" :
  app.run("0.0.0.0",port=3000,debug=True)
