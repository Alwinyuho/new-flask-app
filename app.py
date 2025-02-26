from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/select_alphabet", methods=["POST"])
def select_alphabet():
    selected_alphabet = request.form.get("alphabet")
    
    if selected_alphabet and selected_alphabet.isalpha() and len(selected_alphabet) == 1:
        alphabet_position = ord(selected_alphabet.upper()) - ord("A") + 1
        return render_template("index.html", result=f"You selected {selected_alphabet.upper()}, which is letter {alphabet_position} in the alphabet.")
    else:
        return render_template("index.html", result="Invalid input. Please enter a single alphabet.")

if __name__ == "__main__":
    app.run(debug=True)
