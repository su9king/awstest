from flask import Flask, render_template, g, request
from dotenv import load_dotenv
import os

from loginPage import loginPage_bp
from registerPage import registerPage_bp
from uploadPage import uploadPage_bp

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.secret_key = "asb"  # 플래시 메시지에 필요
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 블루프린트 등록
app.register_blueprint(loginPage_bp)
app.register_blueprint(registerPage_bp)
app.register_blueprint(uploadPage_bp)


@app.before_request
def load_session():
    # 클라이언트 쿠키에서 세션 ID를 가져와 g 객체에 저장
    g.session_id = request.cookies.get("session_id")


@app.context_processor
def inject_session():
    # 템플릿에 session_id 변수 전달
    return {"session_id": g.session_id}


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

