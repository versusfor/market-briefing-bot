import requests
import datetime

# 🔐 PEGA AQUÍ TUS CREDENCIALES NUEVAS (NO LAS COMPARTAS)
TELEGRAM_TOKEN = "8774099880:AAFyVd-Id8eC4sGVztg9W0Z-1kPstLu6Hb0"
CHAT_ID = "1373100163"  # Ej: 123456789

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)

    # Debug (para ver errores en GitHub Actions)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

def get_sentiment():
    # Simple (luego lo mejoramos con datos reales)
    return "🟡 NEUTRAL"

def build_briefing(session):
    now = datetime.datetime.now().strftime("%H:%M")

    message = f"""
==========================
📊 MARKET BRIEFING
Sesión: {session}
Hora: {now}
==========================

🧠 SENTIMIENTO
{get_sentiment()}

📰 NOTICIAS CLAVE
- Mercado atento a inflación
- Movimientos en tecnología
- Volatilidad en cripto

📉 NIVELES CLAVE

NSQ100
R: 18000
S: 17500

BTC
R: 70000
S: 65000

ORO
R: 2400
S: 2300

DXY
R: 105
S: 103

VIX
R: 20
S: 15

BRENT
R: 85
S: 80

⏰ EVENTOS HOY
- Revisar calendario económico
(ALTO IMPACTO)

⚠️ ACCIÓN
- Esperar confirmación
- Evitar operar en noticias
"""
    return message

def run():
    # Puedes luego detectar sesión por horario si quieres
    briefing = build_briefing("AUTO")
    send_telegram(briefing)

if __name__ == "__main__":
    run()
