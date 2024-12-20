ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}


# 파일 확장자 유효성 검사 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

