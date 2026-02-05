#######################################################################################
# 필요한 모듈 import, 기본 설정
# pip install flask
from flask import Flask, render_template, request, redirect, url_for, session
import os

# 데이터 관리를 위한 폴더 (data 폴더가 없으면 생성)
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_FILE_PATH):
  os.makedirs(DATA_FILE_PATH)

 # 이전에 만들어 놓은 sjcusvm.py 소스코드를 복사하여 저장해 놓은 상태
 # sjcusvm.py 모듈을 import
import sjcusvm as svm

# 웹 서버 만들기
app = Flask(__name__, static_folder='public', template_folder='templates')
app.secret_key = '##_SJCU_AIService_Secret_Key_##'

#######################################################################################
# 사용자 정보 (권장하지 않는 방식이나 테스트를 위한 사용자 계정 정보 설정)
users = {
    "user": "password"
}

#######################################################################################
# 공통 함수
# 로그인이 필요한 페이지에서 호출되는 함수
def login_required(func):
    def wrapper(*args, **kwargs):
        if session.get("logged_in"):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("login"))
    return wrapper

#######################################################################################
# 라우터 - URL 요청과 기능의 연결
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password.")
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("index"))

# /upload , 로그인이 필요한 페이지.
@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template("upload.html")

    file = request.files['file']
    if file:
        filename = os.path.join(DATA_FILE_PATH, file.filename)
        file.save(filename)
        # 성적 CSV 업로드 시 data 폴더에 저장 후 머신러닝에 활용 => weights 파일 생성
        # csv 파일일 경우에만 처리, 현재는 소문자 확장자만 대상으로 하나 대소문자 구분없이 처리하도록 수정 필요.
        if filename.endswith(".csv"):
            svm.makeweights(filename)

    return redirect(url_for("index"))

# /grade 성적 예측 페이지 => 국어, 수학 점수를 입력받고 예측 결과를 출력
@app.route("/grade", methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        kor = int(request.form["kor"])
        math = int(request.form["math"])
        # 만들어 놓은 svm.py 모듈을 이용하여 성적 예측
        grade = svm.runsvm(kor, math)
        return render_template("grade_result.html", kor=kor, math=math, grade=grade)
    else:
        return render_template("grade.html")

#######################################################################################
# Flask App Starting
def start():
    app.run(
    host="0.0.0.0",
    port=7777,
    debug=True)
    
if __name__ == '__main__':
    start()