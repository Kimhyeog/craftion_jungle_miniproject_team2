from flask import Blueprint, render_template, request, url_for, jsonify
from flask import make_response, redirect
from datetime import datetime, timedelta, timezone
import jwt
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = "your-secret-key-here-change-this-in-production"
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_picture_type(fileName):
    if '.' not in fileName:
        return False
    ext = fileName.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        userId = request.form.get('userId')
        password = request.form.get('password')
        username = request.form.get('userName')
        nickname = request.form.get('nickName')
        hobby = request.form.get('hobby')
        mbti = request.form.get('mbti')
        one_line_intro = request.form.get('oneLineIntro')
        motivate = request.form.get('motivate')
        favorite_food = request.form.get('favoriteFood')

        if not all([userId, password, username, nickname]):
            return jsonify({'result': 'error', 'msg': '필수 입력 항목이 누락되었습니다.'}), 400

        if db.users.find_one({"userId": userId}):
            return jsonify({'result': 'error', 'msg': '이미 사용 중인 아이디입니다.'}), 409

        password_hash = generate_password_hash(password)
        profile_photo_url = None

        file = request.files.get('profileImage')
        
        if file and file.filename != '':
            if not allowed_picture_type(file.filename):
                return jsonify({'result': 'error', 'msg': '허용되지 않는 파일 형식입니다. (jpg, jpeg, png)'}), 400

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            saved_filename = f"{timestamp}_{filename}"
            
            saved_path_for_db = os.path.join(UPLOAD_FOLDER, saved_filename).replace("\\", "/")
            
            server_save_path = os.path.join(UPLOAD_FOLDER, saved_filename)
            file.save(server_save_path)

            profile_photo_url = saved_path_for_db

        doc = {
            'userId' : userId,
            'password' : password_hash,
            'userName': username,
            'quizInfo': {
                'nickName': nickname,
                'profilePhoto': profile_photo_url,
                'selfIntro': one_line_intro,
                'selfMotive': motivate,
                'favoriteFood': favorite_food,
                'hobby': hobby,
                'mbti': mbti
            },
            'userWhoSolvedMe': [],
            'usersISolved': [],
            'userWhoSolvedMeCount': 0,
            'usersISolvedCount': 0
        }
        
        db.users.insert_one(doc)
        
        login_url = url_for('auth.login_page')
        return jsonify({
            'result': 'success',
            'msg': '회원가입이 완료되었습니다.',
            'redirect_url': login_url
        })

    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        userId = request.form.get('userId')
        password = request.form.get('password')

        user = db.users.find_one({'userId': userId})

        if user and check_password_hash(user['password'], password):
            exp = datetime.now(timezone.utc) + timedelta(days=14)
            payload = {"id": userId, "exp": exp}
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            main_page_url = url_for('quiz.quiz_list')
            resp = jsonify({
                'result': 'success',
                'msg': '로그인에 성공했습니다!',
                'redirect_url': main_page_url,
                'userId': user.get('userId'),
                'token': token,
            })
            resp.set_cookie(
                "mytoken",
                token,
                httponly=True,
                samesite="Lax",
                secure=False
            )
            return resp
        else:
            return jsonify({
                'result': 'fail',
                'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'
            })

    return render_template("auth/login.html")

@auth_bp.route("/logout", methods=['GET'])
def logout():
    resp = make_response(redirect(url_for('auth.login_page')))
    resp.set_cookie("mytoken", "", expires=0)
    return resp

