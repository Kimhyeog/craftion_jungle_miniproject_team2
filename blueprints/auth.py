# jsonify, check_password_hash를 추가로 import 합니다.
from flask import Blueprint, render_template, request, url_for, jsonify
from flask import make_response, redirect
from datetime import datetime, timedelta, timezone
import jwt
from database import db
# werkzeug는 비밀번호를 안전하게 해싱(암호화)하기 위해 사용합니다.
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
# 'auth' 라는 이름의 Blueprint를 생성합니다.
auth_bp = Blueprint('auth', __name__)

# JWT 시크릿 키 (프로덕션에서는 환경변수/설정으로 관리)
SECRET_KEY = "your-secret-key-here-change-this-in-production"


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_picture_type(fileName):
    if '.' not in fileName:
        return False
    ext = fileName.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


# 회원 가입 api 라우터
@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        userId = request.form.get('userId')
        password = request.form.get('password')
        username = request.form.get('userName')
        nickname = request.form.get('nickName')
        # ... (나머지 form 데이터들)
        hobby = request.form.get('hobby')
        mbti = request.form.get('mbti')
        one_line_intro = request.form.get('oneLineIntro')
        motivate = request.form.get('motivate')
        favorite_food = request.form.get('favoriteFood')

        # ▼▼▼ [수정 1] 필수 입력값 확인 ▼▼▼
        if not all([userId, password, username, nickname]):
            return jsonify({'result': 'error', 'msg': '필수 입력 항목이 누락되었습니다.'}), 400

        # ▼▼▼ [수정 2] ID 중복 시 명확한 에러 메시지 반환 ▼▼▼
        if db.users.find_one({"userId": userId}):
            return jsonify({'result': 'error', 'msg': '이미 사용 중인 아이디입니다.'}), 409

        password_hash = generate_password_hash(password)
        profile_photo_url = None # 기본값은 None (사진 없음)

        # ▼▼▼ [수정 3] 파일 처리 로직 개선 ▼▼▼
        file = request.files.get('profileImage')
        
        # 파일이 존재하고, 파일 이름이 있는 경우에만 처리
        if file and file.filename != '':
            if not allowed_picture_type(file.filename):
                return jsonify({'result': 'error', 'msg': '허용되지 않는 파일 형식입니다. (jpg, jpeg, png)'}), 400

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            saved_filename = f"{timestamp}_{filename}"
            
            # DB에 저장할 경로를 URL 친화적인 형태로 생성
            # Windows에서도 / 를 사용하도록 보장
            saved_path_for_db = os.path.join(UPLOAD_FOLDER, saved_filename).replace("\\", "/")
            
            # 실제 파일 저장 시에는 OS에 맞는 경로 사용
            server_save_path = os.path.join(UPLOAD_FOLDER, saved_filename)
            file.save(server_save_path)

            profile_photo_url = saved_path_for_db
        # ------------------------------------------

        doc = {
            'userId' : userId,
            'password' : password_hash,
            'userName': username,
            'quizInfo': {
                'nickName': nickname,
                'profilePhoto': profile_photo_url, # 수정된 경로 변수 사용
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


# 로그인 api 라우터
@auth_bp.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        # 1. 사용자가 입력한 id, pw를 받아옵니다.
        userId = request.form.get('userId')
        password = request.form.get('password')

        # 2. DB에서 userId가 일치하는 사용자 정보를 찾습니다.
        user = db.users.find_one({'userId': userId})

        # 3. 사용자가 존재하고, 비밀번호도 일치하는지 확인합니다.
        if user and check_password_hash(user['password'], password):
            # 4. 로그인 성공: JWT 발급 (14일 만료)
            exp = datetime.now(timezone.utc) + timedelta(days=14)
            payload = {"id": userId, "exp": exp}
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            # 5. 응답(JSON) + HttpOnly 쿠키 설정
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
                secure=False  # HTTPS 환경이면 True 권장
            )
            return resp
        else:
            # 5. 로그인 실패 시 (아이디가 없거나, 비밀번호가 틀리면)
            return jsonify({
                'result': 'fail',
                'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'
            })

    # GET 요청 시에는 그냥 로그인 페이지만 보여줍니다.
    return render_template("auth/login.html")

# 로그아웃: 쿠키 삭제 후 로그인 페이지로 이동
@auth_bp.route("/logout", methods=['GET'])
def logout():
    resp = make_response(redirect(url_for('auth.login_page')))
    resp.set_cookie("mytoken", "", expires=0)
    return resp

