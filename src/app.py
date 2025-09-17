from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# --- Cargar variables de entorno ---
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecreto"  # necesario para usar flash messages

# --- Rutas normales ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Nosotros')
def Nosotros():
    return render_template('Nosotros.html')

@app.route('/Productos')
def Productos():
    return render_template('Productos.html')

@app.route('/Contacto')
def Contacto():
    return render_template('Contacto.html')

@app.route('/Mercados')
def Mercados():
    return render_template('Mercados.html')


# --- Ruta para enviar formulario ---
@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    remitente = os.getenv("EMAIL_USER")
    clave = os.getenv("EMAIL_PASS")
    destinatario = os.getenv("EMAIL_TO")

    cuerpo = f"""
📩 Nuevo mensaje desde la web Nutricol Foods

👤 Nombre: {nombre}
📧 Email: {email}

📝 Mensaje:
{mensaje}
"""

    try:
        msg = MIMEText(cuerpo, "plain", "utf-8")
        msg["From"] = remitente
        msg["To"] = destinatario
        msg["Subject"] = "Nuevo mensaje desde la web - Nutricol Foods"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remitente, clave)
            server.sendmail(remitente, destinatario, msg.as_string())

        flash("✅ Tu mensaje fue enviado correctamente.", "success")
    except Exception as e:
        flash(f"❌ Error al enviar el mensaje: {e}", "danger")

    return redirect(url_for("Contacto"))

if __name__ == '__main__':
    app.run(debug=True)
