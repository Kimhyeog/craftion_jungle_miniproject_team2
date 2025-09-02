
# 필요한 라이브러리 import
from flask import Flask, render_template

from user_profile import profile_bp  # 프로필 페이지 blueprint 불러오기 
from user_info import info_bp

app = Flask(__name__)
app.register_blueprint(profile_bp)   # app에 등록 
app.register_blueprint(info_bp)

@app.route("/")
def mainPage() :
  return render_template("index.html")

if __name__ == "__main__" :
  app.run("0.0.0.0",port=3000,debug=True)

