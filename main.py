import requests
import datetime
import os

def obtener_datos_clima():
    try:
        # Obtener IP y ubicación dinámica
        ip = requests.get("https://api.ipify.org").text
        ubicacion = requests.get(f"https://ipinfo.io/{ip}/json").json()
        ciudad = ubicacion.get("city", "Ciudad Desconocida")
        loc = ubicacion.get("loc", "0,0").split(',')
        latitud = loc[0]
        longitud = loc[1]

        # API de OpenWeatherMap
        api_key = os.getenv("API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={api_key}&units=metric&lang=es"
        clima = requests.get(url).json()

        datos = {
            "ciudad": ciudad,
            "ip": ip,
            "lat": latitud,
            "lon": longitud,
            "temperatura": clima["main"]["temp"],
            "temp_min": clima["main"]["temp_min"],
            "temp_max": clima["main"]["temp_max"],
            "sensacion": clima["main"]["feels_like"],
            "descripcion": clima["weather"][0]["description"],
            "viento": clima["wind"]["speed"]
        }
        return datos

    except Exception as e:
        return {"error": f"No se pudo obtener el clima: {str(e)}"}

def generar_mensaje(datos):
    if "error" in datos:
        return datos["error"]

    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mensaje = (
        f"🌦️ *LIORA ALERTA METEOROLÓGICA EXTENDIDA 24/7*\n"
        f"🕓 Fecha y hora: {ahora}\n"
        f"📍 Ciudad detectada: {datos['ciudad']}\n"
        f"🌐 IP: {datos['ip']}\n"
        f"📡 Coordenadas: {datos['lat']}, {datos['lon']}\n\n"
        f"🌡️ Temperatura: {datos['temperatura']}°C\n"
        f"🌡️ Mínima: {datos['temp_min']}°C | Máxima: {datos['temp_max']}°C\n"
        f"🤒 Sensación térmica: {datos['sensacion']}°C\n"
        f"🌬️ Viento: {datos['viento']} m/s\n"
        f"☁️ Estado: {datos['descripcion'].capitalize()}\n\n"
        f"📲 *UNOSOMOS*"
    )
    return mensaje

def enviar_mensaje_telegram(mensaje):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

# Punto de entrada principal
if __name__ == "__main__":
    datos = obtener_datos_clima()
    mensaje = generar_mensaje(datos)
    enviar_mensaje_telegram(mensaje)
