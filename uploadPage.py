import os
from flask import Blueprint, flash, redirect, request, render_template, current_app, url_for
from utils.auth_utils import validate_session
from utils.imageFile_utils import allowed_file


uploadPage_bp = Blueprint("upload", __name__)
UPLOAD_FOLDER = 'images'  # 서버에 이미지가 저장될 폴더

@uploadPage_bp.before_request
def load_session():
    print("load_session 실행")
    # 클라이언트 쿠키에서 세션 ID를 가져와 g 객체에 저장
    session_id = request.cookies.get("session_id")
    # get_active_sessions()
    session_valid, response = validate_session(session_id)

    if response:
        flash("세션이 만료되었습니다.", "danger")
        return response

    if session_valid:
        flash("로그아웃 완료!", "success")
        # return redirect(url_for("login.login"))
        return

    flash("이미 로그아웃 상태입니다.", "info")
    return redirect(url_for("login.login"))

# 이미지 업로드 페이지
@uploadPage_bp.route('/upload', methods=['GET', 'POST'])
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
            # Flask 설정에서 업로드 폴더 경로 가져오기
            upload_folder = current_app.config['UPLOAD_FOLDER']

            # 폴더가 없다면 생성
            os.makedirs(upload_folder, exist_ok=True)

            # 파일 저장
            filepath = os.path.join(upload_folder, file.filename)
            file.save(filepath)
            flash(f'이미지가 성공적으로 업로드되었습니다: {file.filename}', 'success')

            result = ["SMC","100.00%"] # ==> [ 화가 이름 / 퍼센트 ]

            return redirect(request.url)
        else:
            flash('JPG 형식의 파일만 업로드 가능합니다.', 'danger')
            return redirect(request.url)

    # GET 요청일 경우 업로드 페이지 렌더링
    return render_template('upload.html')

