from flask import Flask, request, render_template, jsonify
from app import run_conversation, get_debug_log

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if not user_input:
            return "请输入内容", 400

        final_response = run_conversation(user_input)
        return render_template("index.html", result=final_response)

    return render_template("index.html")

@app.route("/debug_log")
def debug_log():
    return jsonify({"log": get_debug_log()})

if __name__ == "__main__":
    app.run(debug=True)
