from flask import Flask, render_template, request, session
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = "any_secret_key_here"  # 세션을 사용하기 위해 필요합니다.

# 클라이언트 설정
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


@app.route("/", methods=["GET", "POST"])
def index():
    # 1. 세션에 대화 내역이 없으면 초기화
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form.get("user_input")
        engine = request.form.get("engine")

        # 2. 사용자 질문을 히스토리에 추가
        session["chat_history"].append({"role": "user", "content": user_input})

        # 엔진 선택 및 답변 생성
        client = openai_client if engine == "openai" else ollama_client
        model = "gpt-4o-mini" if engine == "openai" else "llama3.2"

        # 3. 전체 히스토리를 모델에 전달 (이전 대화를 기억하게 함)
        response = client.chat.completions.create(
            model=model,
            messages=session["chat_history"]
        )
        answer = response.choices[0].message.content

        # 4. AI 답변을 히스토리에 추가
        session["chat_history"].append({"role": "assistant", "content": answer})

        # 세션 데이터 변경을 확정
        session.modified = True

    return render_template("index.html", chat_history=session["chat_history"])


@app.route("/clear")
def clear():
    session.pop("chat_history", None)
    return """<script>window.location.href='/';</script>"""


if __name__ == "__main__":
    app.run(debug=True)