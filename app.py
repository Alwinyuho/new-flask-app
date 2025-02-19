from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Ensure this exists in templates/

@app.route("/select_alphabet", methods=["POST"])
def select_alphabet():
    selected_alphabet = request.form.get("alphabet")
    
    if selected_alphabet:
        alphabet_position = ord(selected_alphabet.upper()) - ord("A") + 1
        return f"You selected {selected_alphabet.upper()}, which is letter {alphabet_position} in the alphabet."
    else:
        return "No alphabet selected."

if __name__ == "__main__":
    app.run(debug=True)