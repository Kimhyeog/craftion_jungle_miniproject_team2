# blueprints/quiz.py

from flask import Blueprint, render_template, request, jsonify
from flask import redirect, url_for
from database import db
from bson import ObjectId
import math

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route("/list")
def quiz_list():
    page = request.args.get('page', 1, type=int)
    search_keyword = request.args.get('search', '', type=str)
    limit = 8

    # ▼▼▼ [수정] 기본 쿼리에 quizInfo 필드가 존재하는 조건 추가 ▼▼▼
    query = {'quizInfo': {'$exists': True}}

    if search_keyword:
        regex = {'$regex': search_keyword, '$options': 'i'}
        # 검색 시에도 quizInfo 존재 조건을 AND 조건으로 합침
        query['$and'] = [
            {
                '$or': [
                    {'quizInfo.nickName': regex},
                    {'quizInfo.selfIntro': regex},
                    {'quizInfo.mbti': regex},
                    {'quizInfo.hobby': regex},
                    {'quizInfo.favoriteFood': regex}
                ]
            }
        ]
    
    total_users = db.users.count_documents(query)
    total_pages = math.ceil(total_users / limit)
    skip_count = (page - 1) * limit
    
    users = list(db.users.find(query).skip(skip_count).limit(limit))
    
    # --- 디버깅을 위한 코드 ---
    # 터미널에서 조회된 데이터가 정상적인지 확인해보세요.
    # print(f"페이지: {page}, 검색어: '{search_keyword}', 찾은 유저 수: {len(users)}")
    # for u in users:
    #     print(u)
    # -------------------------

    return render_template(
        "quiz/list.html",
        users=users,
        total_pages=total_pages,
        current_page=page,
        search_keyword=search_keyword
    )

# ... (이하 다른 라우터는 동일) ...
@quiz_bp.route("/dashboard/<string:db_id>")
def quiz_dashboard(db_id):
  if not ObjectId.is_valid(db_id):
    return "Invalid user ID format", 400

  user = db.users.find_one({'_id': ObjectId(db_id)})
  
  if not user:
      return redirect(url_for('quiz.quiz_list'))

  # [수정] 이미 푼 퀴즈일 경우, 데이터 없이 렌더링하는 대신 리스트 페이지로 리다이렉트
  if user.get('userWhoSolvedMeCount', 0) != 0:
    return redirect(url_for('quiz.quiz_list'))

  return render_template(
    "quiz/dashboard.html", 
    nickName = user['quizInfo']['nickName'],
    profilePhoto = user['quizInfo']['profilePhoto'],
    selfIntro = user['quizInfo']['selfIntro'],
    selfMotive = user['quizInfo']['selfMotive'],
    favoriteFood = user['quizInfo']['favoriteFood'],
    mbti = user['quizInfo']['mbti'],
    hobby = user['quizInfo']['hobby'],
    correctName = user['userName']
  )