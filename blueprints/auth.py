# jsonify, check_password_hash를 추가로 import 합니다.
from flask import Blueprint, render_template, request, url_for, jsonify
from database import db
# werkzeug는 비밀번호를 안전하게 해싱(암호화)하기 위해 사용합니다.
from werkzeug.security import generate_password_hash, check_password_hash

# 'auth' 라는 이름의 Blueprint를 생성합니다.
auth_bp = Blueprint('auth', __name__)


# 회원 가입 api 라우터
@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup_page():
    # POST 요청은 회원가입 폼을 제출했을 때 들어옵니다.
    if request.method == 'POST':
        # 1. signup.html의 form에서 보낸 데이터를 받습니다.
        userId = request.form.get('userId')
        password = request.form.get('password')
        username = request.form.get('userName')
        nickname = request.form.get('nickName')
        hobby = request.form.get('hobby')
        mbti = request.form.get('mbti')
        one_line_intro = request.form.get('oneLineIntro')
        motivate = request.form.get('motivate')
        favorite_food = request.form.get('favoriteFood')
        
        # 비밀번호를 해싱(암호화)합니다.
        password_hash = generate_password_hash(password)
        profile_photo_filename = None

        # 2. DB에 저장할 document를 만듭니다.
        doc = {
            'userId' : userId,
            'password' : password_hash, # 암호화된 비밀번호를 저장합니다.
            'userName': username,
            'quizInfo': {
                'nickName': nickname,
                'profilePhoto': profile_photo_filename,
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
        
        # 3. 'users' 컬렉션에 문서를 삽입합니다.
        db.users.insert_one(doc)
        
        # 4. 성공 신호를 JavaScript에게 보냅니다.
        login_url = url_for('auth.login_page')
        return jsonify({
            'result': 'success',
            'msg': '회원가입이 완료되었습니다.',
            'redirect_url': login_url
        })

    # GET 요청 시에는 회원가입 페이지만 보여줍니다.
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
            # 4. 로그인 성공 시, JS에게 보낼 데이터를 만듭니다.
            main_page_url = url_for('main_page')
            return jsonify({
                'result': 'success',
                'msg': '로그인에 성공했습니다!',
                'redirect_url': main_page_url, # <--- 여기에 쉼표(,)를 추가했습니다.
                'userId': user.get('userId')
            })
        else:
            # 5. 로그인 실패 시 (아이디가 없거나, 비밀번호가 틀리면)
            return jsonify({
                'result': 'fail',
                'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'
            })

    # GET 요청 시에는 그냥 로그인 페이지만 보여줍니다.
    return render_template("auth/login.html")

