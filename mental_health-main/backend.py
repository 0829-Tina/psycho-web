# backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS      # 解决网页跨域
import requests
import os

app = Flask(__name__)
CORS(app)                        # 允许 8501 访问 5000

API_KEY = os.getenv("MOONSHOT_API_KEY")          # 从终端读取密钥
URL = "https://api.moonshot.cn/v1/chat/completions"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_text = request.json.get("message")
        if not user_text:
            return jsonify({"error": "Empty input"}), 400

        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "moonshot-v1-8k",
            "messages": [
                {"role": "system", "content": "你是一位温和的心理健康助手，请给出科学、可操作的建议，不诊断不开药。"},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.7
        }

        print("【DEBUG】请求体：", payload)  # ← 这里手动打印
        r = requests.post(URL, json=payload, headers=headers, timeout=30)
        print("【DEBUG】响应状态：", r.status_code)  # ← 打印状态码
        print("【DEBUG】响应文本：", r.text)  # ← 打印原始返回

        if r.status_code != 200:
            return jsonify({"error": "模型调用失败", "detail": r.text}), 500

        reply = r.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        import traceback
        traceback.print_exc()  # ← 关键：把异常完整打印到终端
        return jsonify({"error": "服务器内部错误", "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)