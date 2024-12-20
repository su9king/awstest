from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASH_SECRET_KEY")  # 플래시 메시지에 필요

# 회원가입 파일 경로
USERS_FILE_PATH = "users.json"

# JSON 파일 초기화
def initialize_json():
    if not os.path.exists(USERS_FILE_PATH):
        with open(USERS_FILE_PATH, "w") as file:
            json.dump({}, file)


# 회원가입 시 사용자 추가 함수
def add_user(user_id, username, password):
    initialize_json()
    with open(USERS_FILE_PATH, "r") as file:
        data = json.load(file)

    if user_id in data:
        return False  # 아이디 중복

    # 새 사용자 추가
    data[user_id] = {"username": username, "password": password}
    with open(USERS_FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
    return True


# 로그인 확인 함수
def validate_user(user_id, password):
    initialize_json()
    with open(USERS_FILE_PATH, "r") as file:
        data = json.load(file)

    return user_id in data and data[user_id]["password"] == password

# 로그인 페이지
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        if validate_user(user_id, password):
            flash("로그인 성공!", "success")  ## flash message 지정
            #return redirect(url_for("welcome", username=user_id))   ## url path parameter로 데이터 전달 방법
            return redirect("upload")
        else:
            flash("아이디 또는 비밀번호가 올바르지 않습니다.", "danger")

    return render_template("login.html")


# 회원가입 페이지
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        username = request.form.get("username")
        password = request.form.get("password")

        if add_user(user_id, username, password):
            flash("회원가입 성공! 로그인하세요.", "success")
            return redirect(url_for("login"))
        else:
            flash("이미 존재하는 아이디입니다. 다른 아이디를 사용하세요.", "danger")

    return render_template("register.html")


# 이미지 업로드 경로 설정
UPLOAD_FOLDER = 'images'  # 서버에 이미지가 저장될 폴더
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 폴더가 없다면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 파일 확장자 유효성 검사 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 이미지 업로드 페이지
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # 파일이 요청에 포함되어 있는지 확인
        if 'image' not in request.files:
            flash('이미지 파일이 선택되지 않았습니다.', 'danger')
            return redirect(request.url)

        file = request.files['image']

        # 파일명이 없는 경우 처리
        if file.filename == '':
            flash('파일명이 없습니다. 파일을 다시 선택하세요.', 'danger')
            return redirect(request.url)

        # 파일 유효성 검사
        if file and allowed_file(file.filename):
            # 파일 저장
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            flash(f'이미지가 성공적으로 업로드되었습니다: {filename}', 'success')
            return redirect(request.url)
        else:
            flash('JPG 형식의 파일만 업로드 가능합니다.', 'danger')
            return redirect(request.url)

    # GET 요청일 경우 업로드 페이지 렌더링
    return render_template('upload.html')


# 기본 루트 페이지
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
