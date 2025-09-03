from flask import Blueprint, render_template, request, redirect, url_for
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
        #    name 속성을 기준으로 값을 가져옵니다.
        username = request.form.get('userName')
        nickname = request.form.get('nickName')
        hobby = request.form.get('hobby')
        mbti = request.form.get('mbti')
        one_line_intro = request.form.get('oneLineIntro')
        motivate = request.form.get('motivate')
        favorite_food = request.form.get('favoriteFood')
        
        # TODO: 프로필 사진 처리 로직 (우선 파일 이름만 저장)
        # profile_photo = request.files.get('profilePhoto')
        # 지금은 임시로 None으로 설정합니다.
        profile_photo_filename = None

        # 2. 받아온 데이터들을 딕셔너리 형태로 가공합니다.
        #    이 딕셔너리가 DB에 저장될 문서(document)가 됩니다.
        doc = {
            'userName': username,
            'quizInfo': {
                'nickName': nickname,
                'profilePhoto': profile_photo_filename, # 파일 이름 저장
                'selfIntro': one_line_intro,
                'selfMotive': motivate,
                'favoriteFood': favorite_food,
                'hobby': hobby,
                'mbti': mbti
            },
            # 나중에 퀴즈 기능 구현 시 필요한 필드들
            'userWhoSolvedMe': [],
            'usersISolved': [],
            'userWhoSolvedMeCount': 0,
            'usersISolvedCount': 0
        }
        
        # 3. 'users' 컬렉션에 위에서 만든 doc을 삽입(저장)합니다.
        db.users.insert_one(doc)
        
        # 4. 저장이 완료되면 로그인 페이지로 이동시킵니다.
        return redirect(url_for('auth.login_page'))

    # GET 요청은 단순히 회원가입 페이지를 보여줍니다.
    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        # TODO: 로그인 로직 구현
        pass
    return render_template("auth/login.html")
