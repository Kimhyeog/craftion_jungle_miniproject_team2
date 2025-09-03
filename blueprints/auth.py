# jsonify, check_password_hash를 추가로 import 합니다.
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
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
        
        # --- [중요] 비밀번호 해싱 ---
        # werkzeug 라이브러리를 사용해 비밀번호를 암호화합니다.
        password_hash = generate_password_hash(password)

        profile_photo_filename = None

        # 2. 받아온 데이터들을 딕셔너리 형태로 가공합니다.
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


# --- 여기가 바뀝니다! ---
@auth_bp.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        # 1. 사용자가 입력한 id, pw를 받아옵니다.
        userId = request.form.get('userId')
        password = request.form.get('password')

        # 2. DB에서 userId가 일치하는 사용자 정보를 찾습니다.
        user = db.users.find_one({'userId': userId})

        # 3. 사용자 정보를 찾았고, 비밀번호도 일치하는지 확인합니다.
        # check_password_hash(DB의 암호화된 비번, 사용자가 입력한 평문 비번)
        if user and check_password_hash(user['password'], password):
            # 4. 로그인 성공 시, 성공 신호와 이동할 메인페이지 URL을 보냅니다.
            main_page_url = url_for('main_page') # app.py의 main_page 함수를 가리킵니다.
            return jsonify({
                'result': 'success',
                'msg': '로그인에 성공했습니다!',
                'redirect_url': main_page_url
            })
        else:
            # 5. 로그인 실패 시 (아이디가 없거나, 비밀번호가 틀리면)
            return jsonify({
                'result': 'fail',
                'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'
            })

    # GET 요청 시에는 그냥 로그인 페이지만 보여줍니다.
    return render_template("auth/login.html")


