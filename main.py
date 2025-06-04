import requests
import datetime
import os
from flask import Flask

# Configuración para servidor Flask
FLASK_PORT = int(os.environ.get("PORT", 3000))
app = Flask(__name__)

# ===== FUNCIONES PRINCIPALES =====

def obtener_datos_clima():
    try:
        ip = requests.get("https://api.ipify.org").text
        ubicacion = requests.get(f"https://ipinfo.io/{ip}/json").json()
        ciudad = ubicacion.get("city", "Ciudad Desconocida")
        loc = ubicacion.get("loc", "0,0").split(',')
        lat, lon = loc[0], loc[1]

        api_key = os.getenv("API_KEY")
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
        )
        clima = requests.get(url).json()

        return {
            "ciudad": ciudad,
            "ip": ip,
            "lat": lat,
            "lon": lon,
            "temperatura": clima["main"]["temp"],
            "descripcion": clima["weather"][0]["description"].capitalize(),
        }

    except Exception as e:
        return {"error": f"❌ Error al obtener clima: {str(e)}"}

def generar_mensaje(datos):
    if "error" in datos:
        return datos["error"]

    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"🌦️ *LIORA ALERTA CLIMÁTICA*\n"
        f"🕓 {ahora}\n"
        f"📍 {datos['ciudad']} ({datos['lat']}, {datos['lon']})\n"
        f"🌡️ {datos['temperatura']}°C\n"
        f"☁️ {datos['descripcion']}\n"
        f"🌐 IP: {datos['ip']}\n"
        f"📲 *UNOSOMOS*"
    )

def enviar_mensaje_telegram(mensaje):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        print("⚠️ Falta BOT_TOKEN o CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# ===== ENDPOINTS PARA RENDER =====

@app.route("/")
def home():
    return "🟢 Liora-clima vivo", 200

@app.route("/clima")
def alerta():
    datos = obtener_datos_clima()
    mensaje = generar_mensaje(datos)
    enviar_mensaje_telegram(mensaje)
    return "✅ Alerta enviada a Telegram", 200

# ===== INICIO DEL SERVIDOR =====

if __name__ == "__main__":
    # Enviar 1 alerta al iniciar
    try:
        datos = obtener_datos_clima()
        mensaje = generar_mensaje(datos)
        enviar_mensaje_telegram(mensaje)
    except Exception
