# jsonify를 추가로 import 해야 합니다.
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from database import db
# werkzeug는 비밀번호를 안전하게 해싱(암호화)하기 위해 사용합니다.
from werkzeug.security import generate_password_hash

# 'auth' 라는 이름의 Blueprint를 생성합니다.
auth_bp = Blueprint('auth', __name__)

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
        
        profile_photo_filename = None

        # 2. 받아온 데이터들을 딕셔너리 형태로 가공합니다.
        doc = {
            'userId' : userId,
            'password' : password,
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
        
        # 3. 'users' 컬렉션에 위에서 만든 doc을 삽입(저장)합니다.
        db.users.insert_one(doc)
        
        # --- 여기가 바뀝니다! ---
        # 4. 저장이 완료되면 페이지를 이동시키는 대신,
        #    성공했다는 신호(JSON)를 JavaScript에게 보냅니다.
        
        # 이전 코드: return redirect(url_for('auth.login_page'))
        
        # 새 코드:
        login_url = url_for('auth.login_page') # JavaScript가 이동할 URL 주소를 만들어주고
        return jsonify({
            'result': 'success',
            'msg': '회원가입이 완료되었습니다.',
            'redirect_url': login_url  # 이 주소를 JSON에 담아서 보냅니다.
        })

    # GET 요청은 단순히 회원가입 페이지를 보여줍니다.
    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        # TODO: 로그인 로직 구현
        pass
    return render_template("auth/login.html")

