import requests
import datetime
import os
from flask import Flask

# ==== CONFIGURACIÓN FLASK PARA RENDER ====
FLASK_PORT = int(os.environ.get("PORT", 3000))
app = Flask(__name__)

# ==== FUNCIÓN: Obtener datos del clima ====
def obtener_datos_clima():
    try:
        ip = requests.get("https://api.ipify.org").text
        ubicacion = requests.get(f"https://ipinfo.io/{ip}/json").json()
        ciudad = ubicacion.get("city", "Ciudad Desconocida")
        loc = ubicacion.get("loc", "0,0").split(',')
        latitud, longitud = loc[0], loc[1]

        api_key = os.getenv("API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={api_key}&units=metric&lang=es"
        clima = requests.get(url).json()

        datos = {
            "ciudad": ciudad,
            "ip": ip,
            "lat": latitud,
            "lon": longitud,
            "temperatura": clima["main"]["temp"],
            "descripcion": clima["weather"][0]["description"]
        }
        return datos

    except Exception as e:
        return {"error": f"No se pudo obtener el clima: {str(e)}"}

# ==== FUNCIÓN: Generar texto del mensaje ====
def generar_mensaje(datos):
    if "error" in datos:
        return datos["error"]

    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = (
        f"🌤️ *LIORA CLIMA 24/7*\n"
        f"📆 {ahora}\n"
        f"📍 {datos['ciudad']} ({datos['lat']}, {datos['lon']})\n"
        f"🌡️ {datos['temperatura']}°C - {datos['descripcion'].capitalize()}\n"
        f"🔗 IP: {datos['ip']}"
    )
    return mensaje

# ==== FUNCIÓN: Enviar a Telegram ====
def enviar_mensaje_telegram(mensaje):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")

# ==== RUTAS DE FLASK ====
@app.route("/")
def home():
    return "🟢 Servidor LIORA activo", 200

@app.route("/clima")
def clima():
    datos = obtener_datos_clima()
    mensaje = generar_mensaje(datos)
    enviar_mensaje_telegram(mensaje)
    return "✅ Alerta enviada a Telegram", 200

# ==== EJECUCIÓN LOCAL Y EN RENDER ====
if __name__ == "__main__":
    datos = obtener_datos_clima()
    mensaje = generar_mensaje(datos)
    enviar_mensaje_telegram(mensaje)
    app.run(host="0.0.0.0", port=FLASK_PORT)
