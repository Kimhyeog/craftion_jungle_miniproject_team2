# 필요한 라이브러리 import
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, make_response
)
from functools import wraps
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
app = Flask(__name__)
app.secret_key = "your-secret-key-here-change-this-in-production"
client = MongoClient('localhost', 27017)
db = client.jungle
SECRET_KEY = "your name"
@app.route("/")
def home():
    return redirect(url_for("login_form"))
@app.route("/signup", methods=["GET"])
def signup_form():
    return render_template("signup.html")
@app.route("/signup", methods=["POST"])
def signup():
    # 디버깅: 받은 데이터 출력
    print("=== 회원가입 요청 데이터 ===")
    print("Form data:", dict(request.form))
    # 클라이언트에서 보낸 데이터 가져오기 (name 속성과 일치)
    receive_name         = request.form.get("userName", "").strip()
    receive_id           = request.form.get("id", "").strip()
    receive_pw           = request.form.get("password", "")
    receive_profilePhoto = request.form.get("profilePhoto", "")
    receive_selfIntro    = request.form.get("selfIntro", "")
    receive_nickName     = request.form.get("nickName", "")
    receive_selfMotive   = request.form.get("selfMotive", "")
    receive_favoriteFood = request.form.get("favoriteFood", "")
    receive_hobby        = request.form.get("hobby", "")
    receive_mbti         = request.form.get("mbti", "")
    print("=== 파싱된 데이터 ===")
    print(f"이름: {receive_name}")
    print(f"아이디: {receive_id}")
    print(f"비밀번호: {receive_pw[:3]}***")  # 보안상 일부만 출력
    print(f"프로필사진: {receive_profilePhoto}")
    print(f"한줄소개: {receive_selfIntro}")
    print(f"닉네임: {receive_nickName}")
    print(f"지원동기: {receive_selfMotive}")
    print(f"좋아하는음식: {receive_favoriteFood}")
    print(f"취미: {receive_hobby}")
    print(f"MBTI: {receive_mbti}")
    # 필수값 검증 실패
    if not receive_name or not receive_id or not receive_pw:
        return render_template("signup.html", msg="필수 입력값이 누락되었습니다.")
    # 아이디 중복 확인
    if db.user.find_one({"userId": receive_id}):
        return render_template("signup.html", msg="이미 존재하는 아이디입니다.")
    # 비밀번호 해시 저장
    pw_hash = generate_password_hash(receive_pw)
    doc = {
        "userName": receive_name,
        "userId": receive_id,
        "password": pw_hash,   # 해시 저장
        "profilePhoto": receive_profilePhoto,
        "selfIntro": receive_selfIntro,
        "nickName": receive_nickName,
        "selfMotive": receive_selfMotive,
        "favoriteFood": receive_favoriteFood,
        "hobby": receive_hobby,
        "mbti": receive_mbti,
    }
    print("=== DB에 저장할 데이터 ===")
    print("Document:", {k: v if k != 'password' else '***HASHED***' for k, v in doc.items()})
    result = db.user.insert_one(doc)
    print(f"=== DB 저장 완료 ===")
    print(f"Inserted ID: {result.inserted_id}")
    return render_template("login.html", msg="회원가입이 완료되었습니다. 로그인 해주세요.")
@app.route("/login", methods=["GET"])
def login_form():
    return render_template("login.html", form_data=None)
@app.route("/login", methods=["POST"])
def login():
    # 디버깅: 받은 데이터 출력
    print("=== 로그인 요청 데이터 ===")
    print("Form data:", dict(request.form))
    receive_id = request.form.get('id', '').strip()
    receive_pw = request.form.get('pw', '')
    print(f"=== 파싱된 로그인 데이터 ===")
    print(f"아이디: {receive_id}")
    print(f"비밀번호: {receive_pw[:3]}***")  # 보안상 일부만 출력
    # 사용자 조회
    user = db.user.find_one({"userId": receive_id})
    if not user:
        return render_template("login.html", msg="존재하지 않는 사용자입니다.")
    # 비밀번호 해시 검증
    if not check_password_hash(user.get('password', ''), receive_pw):
        return render_template("login.html", msg="비밀번호가 일치하지 않습니다.")
    # JWT 발행
    exp = datetime.now(timezone.utc) + timedelta(days=14)
    payload = {"id": receive_id, "exp": exp}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # 응답 + 쿠키 설정 후 리다이렉트
    resp = make_response(redirect(url_for("quizlist")))
    resp.set_cookie(
        "mytoken",
        token,
        httponly=True,
        samesite="Lax",
        secure=False  # HTTPS라면 True로 설정 권장
    )
    return resp
@app.route("/quizlist")
def quizlist():
    return render_template("quizlist.html")
# 토큰 인증 데코레이터, 토큰 유효 및 사용자 존재 확인 후 user라는 변수(DB회원 데이터)를 넘겨준다.
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('mytoken')
        if not token:
            return redirect(url_for("login_form", msg="로그인이 필요합니다."))
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            resp = make_response(redirect(url_for("login_form", msg="로그인 시간이 만료되었습니다.")))
            resp.set_cookie("mytoken", "", expires=0)
            return resp
        except jwt.exceptions.DecodeError:
            resp = make_response(redirect(url_for("login_form", msg="로그인 정보가 유효하지 않습니다.")))
            resp.set_cookie("mytoken", "", expires=0)
            return resp
        # 사용자 존재 확인
        user = db.user.find_one({"userId": payload['id']})
        if not user:
            resp = make_response(redirect(url_for("login_form", msg="존재하지 않는 사용자입니다.")))
            resp.set_cookie("mytoken", "", expires=0)
            return resp
        # 여기서 user 객체를 f에 인자로 넘겨줌
        return f(user, *args, **kwargs)
    return decorated
if __name__ == "__main__" :
  app.run("0.0.0.0",port=3000,debug=True)
