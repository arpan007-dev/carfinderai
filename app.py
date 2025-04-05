from flask import Flask, render_template, request, redirect, session
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "your_secret_key"

genai.configure(api_key="AIzaSyAe-1xQBHTPAZ2GxC3xhfKeOJ9U_LPyzts")

model = genai.GenerativeModel("gemini-2.0-flash-lite")

def get_car_response(user_input):
    prompt = f"""
You are an AI Car Advisor.

User says: "{user_input}"

Understand the needs and reply concisely:
- Car Name & Brand
- Price Range
- Key Features
- Why it fits their need

Use friendly bullet points in 5-6 lines max.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat" not in session:
        session["chat"] = []

    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_response = get_car_response(user_input)

        session["chat"].append({"user": user_input, "bot": bot_response})
        session.modified = True  # Ensures session update

    return render_template("index.html", chat_history=session["chat"])

@app.route("/reset")
def reset_chat():
    session.pop("chat", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

