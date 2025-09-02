from    flask   import  Blueprint, jsonify, abort, request
from    bson    import  ObjectId

from    pymongo import  MongoClient

# client = MongoClient('localhost', 27017)
# db = client.yournameis

info_bp = Blueprint("user_info", __name__)

@info_bp.route("/api/users/<string:db_id>", methods=['GET'])
def get_user_info(db_id):

    if not ObjectId.is_valid(db_id) :
        abort(400)

    # user = db.users.find_one({'_id':ObjectId(db_id)})
    
    if not user:
        abort(404, description="user not found")

    return jsonify({
        'result': 'success',
        'nickname': user['nickname'],
        'self_intro': user['self_intro'],
        'self_motive': user['self_motive'],
        'favorite_food': user['favorite_food'],
        'hobby': user['hobby'],
        'mbti': user['mbti']
    })

