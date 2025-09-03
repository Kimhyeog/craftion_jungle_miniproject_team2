from flask import Blueprint, Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
from datetime import datetime
import os

upload_bp = Blueprint("picture_upload", __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_picture_type(fileName):
   if '.' not in fileName:
      return False
   ext = fileName.rsplit('.', 1)[1].lower()
   return ext in ALLOWED_EXTENSIONS

@upload_bp.route('/tmp')
def upload_page() :
    return render_template("tmp_upload.html")

@upload_bp.route('/upload', methods=['POST']) 
def test_upload() :
    if 'file' not in request.files :
       return '파일이 없습니다.', 400
    
    file = request.files['file']

    if file.filename == '':
       return '선택된 파일이 없습니다.', 400
    
    if not allowed_picture_type(file.filename):
       return '허용되지 않는 파일 유형입니다.(jpg, jpeg, png만 가능)', 400
    
    if not os.path.exists(UPLOAD_FOLDER) :
        os.makedirs(UPLOAD_FOLDER)
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    saved_filename = f"{timestamp}_{filename}"
    saved_path = os.path.join(UPLOAD_FOLDER, saved_filename)
    file.save(saved_path)


    return jsonify({"status": "ok", 'url':saved_filename}), 200
