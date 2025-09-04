from flask import Flask, render_template, jsonify, request, redirect
from database import db

from blueprints.user_profile import profile_bp
from blueprints.auth import auth_bp
from blueprints.quiz import quiz_bp

app = Flask(__name__)

app.register_blueprint(profile_bp, url_prefix="/user")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(quiz_bp, url_prefix="/quiz")


@app.route("/")
def main_page() :
  tokenCheck = request.cookies.get('mytoken')
  if tokenCheck :
    return redirect('/quiz/list')
  return render_template("auth/login.html")


if __name__ == "__main__" :
  app.run("0.0.0.0",port=3000,debug=True)
