from flask import Flask, render_template, request, jsonify
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    doc = nlp(user_input.lower())

    # Basic keyword + entity-based NLP logic
    if any(tok.lemma_ in ["rain", "rainfall", "precipitation"] for tok in doc):
        reply = "☔ Rainfall data is available via INSAT-3DR and Megha-Tropiques."
    elif any(tok.lemma_ in ["cloud", "clouds", "cover"] for tok in doc):
        reply = "☁️ You can monitor cloud cover using Kalpana-1 and INSAT-3D."
    elif any(ent.label_ == "GPE" for ent in doc):  # GPE = Geo-Political Entity
        locations = [ent.text.title() for ent in doc.ents if ent.label_ == "GPE"]
        reply = f"📍 Geo-spatial data for {', '.join(locations)} is available via MOSDAC portal."
    elif "satellite" in user_input:
        reply = "🛰️ India operates satellites like RISAT, Oceansat, and Cartosat for different applications."
    else:
        reply = "🧠 I'm still learning. Try asking about rainfall, satellites, or locations like Gujarat."

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
