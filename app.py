from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/musteri")
def musteri():
    return render_template("musteri.html")

@app.route("/yaratici")
def yaratici():
    return "<h1>Yaratıcı Sayfası</h1>"

# Yazılımcı sekmesi için eksik route eklendi
@app.route("/musteri/yazilimci")
def musteri_yazilimci():
    return render_template("musteri_yazilimci.html")

# Şimdilik müşteri alt sayfaları

@app.route("/musteri/leveldesigner")
def musteri_level():
    return render_template("musteri_level.html")

@app.route("/musteri/modeler")
def musteri_model():
    return render_template("musteri_model.html")

@app.route("/musteri/sessanatcisi")
def musteri_ses():
    return render_template("musteri_ses.html")

if __name__ == "__main__":
    app.run(debug=True)
