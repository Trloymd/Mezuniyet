from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# --- veritabanı hazırlama ---
def init_db():
    conn = sqlite3.connect("site.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isim TEXT,
                    kategori TEXT,
                    dil TEXT,
                    foto TEXT,
                    aciklama TEXT
                )""")
    # C# ve C++ yazılımcısı ekle
    c.execute("SELECT COUNT(*) FROM users WHERE kategori=? AND dil=?", ("yazılımcı", "C#"))
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (isim, kategori, dil, foto, aciklama) VALUES (?, ?, ?, ?, ?)",
                  ("Ahmet CSharp", "yazılımcı", "C#", "/static/default.jpg", "C# uzmanı yazılımcı."))
    c.execute("SELECT COUNT(*) FROM users WHERE kategori=? AND dil=?", ("yazılımcı", "C++"))
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (isim, kategori, dil, foto, aciklama) VALUES (?, ?, ?, ?, ?)",
                  ("Mehmet Cpp", "yazılımcı", "C++", "/static/default.jpg", "C++ uzmanı yazılımcı."))
    conn.commit()
    conn.close()

init_db()

# --- anasayfa ---
@app.route("/")
def index():
    return render_template("index.html")

# --- yaratıcı hesap ekleme ---
@app.route("/yaratici", methods=["GET", "POST"])
def yaratici():
    if request.method == "POST":
        isim = request.form.get("isim")
        aciklama = request.form.get("aciklama")
        kategori = request.form.get("kategori")
        dil = request.form.get("dil") if kategori == "yazılımcı" else None

        foto = request.files["foto"]
        if foto and foto.filename != "":
            foto_path = os.path.join(app.config["UPLOAD_FOLDER"], foto.filename)
            foto.save(foto_path)
            foto_db_path = "/" + foto_path.replace("\\", "/")
        else:
            foto_db_path = "/static/default.jpg"

        conn = sqlite3.connect("site.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (isim, kategori, dil, foto, aciklama) VALUES (?, ?, ?, ?, ?)",
                  (isim, kategori, dil, foto_db_path, aciklama))
        conn.commit()
        conn.close()

        return redirect(url_for("yaraticilar"))

    return render_template("yaratici.html")

# --- yaratıcıları listeleme ---
@app.route("/yaraticilar")
def yaraticilar():
    conn = sqlite3.connect("site.db")
    c = conn.cursor()
    c.execute("SELECT id, isim, kategori, dil, foto, aciklama FROM users")
    users = c.fetchall()
    conn.close()
    return render_template("yaraticilar.html", users=users)

# --- menü sayfası ---
@app.route("/menu")
def menu():
    return render_template("menu.html")

# --- müşteri sayfası ---
@app.route("/musteri")
def musteri():
    return render_template("musteri.html")

@app.route("/musteri/yazilimci")
def musteri_yazilimci():
    return render_template("musteri_yazilimci.html")

@app.route("/musteri/yazilimci/<dil>")
def musteri_yazilimci_dil(dil):
    conn = sqlite3.connect("site.db")
    c = conn.cursor()
    c.execute("SELECT isim, foto, aciklama FROM users WHERE LOWER(kategori)=? AND LOWER(dil)=?", ("yazılımcı", dil.lower()))
    users = c.fetchall()
    conn.close()
    return render_template("yazilimci_listesi.html", users=users, dil=dil)

@app.route("/musteri/modeler")
def musteri_modeler():
    conn = sqlite3.connect("site.db")
    c = conn.cursor()
    c.execute("SELECT isim, foto, aciklama FROM users WHERE LOWER(kategori)=?", ("modeler",))
    users = c.fetchall()
    conn.close()
    return render_template("modeler_listesi.html", users=users)

@app.route("/musteri/sessanatcisi")
def musteri_sessanatcisi():
    conn = sqlite3.connect("site.db")
    c = conn.cursor()
    c.execute("SELECT isim, foto, aciklama FROM users WHERE LOWER(kategori)=?", ("ses sanatçısı",))
    users = c.fetchall()
    conn.close()
    return render_template("ses_listesi.html", users=users)

@app.route("/musteri/leveldesigner")
def musteri_leveldesigner():
    conn = sqlite3.connect("site.db")
    c = conn.cursor()
    c.execute("SELECT isim, foto, aciklama FROM users WHERE LOWER(kategori)=?", ("level designer",))
    users = c.fetchall()
    conn.close()
    return render_template("level_listesi.html", users=users)

if __name__ == "__main__":
    if not os.path.exists("static/uploads"):
        os.makedirs("static/uploads")
    app.run(debug=True)
