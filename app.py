from flask import Flask, render_template, request, send_from_directory
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def summarize_text(input_text):
    headers = {"Authorization": "Bearer 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"}
    data = {"inputs": input_text, "parameters": {"max_length": 100}} 

    try:
        response = requests.post(API_URL, json=data, headers=headers)
    except Exception as e:
        print(f"Error calling API: {e}")
        return None

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None

    response_data = response.json()
    summary = response_data[0]["summary_text"]
    return summary

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST":
        input_text = request.form["input_text"]
        summary = summarize_text(input_text)
    return render_template("index.html", summary=summary)

@app.route('/static/icon.png')
def static_files():
    return send_from_directory('static', 'icon.png')

@app.route('/static/logo.png')
def serve_logo():
    return send_from_directory('static', 'logo.png')


if __name__ == "__main__":
    app.run(debug=True)
