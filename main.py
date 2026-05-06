import requests
import datetime

TELEGRAM_TOKEN = "8774099880:AAFyVd-Id8eC4sGVztg9W0Z-1kPstLu6Hb0"
CHAT_ID = "1373100163"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def get_sentiment():
    # Simulación simple (luego lo conectamos real)
    return "🟡 NEUTRAL"

def get_news():
    # Simulación simple (luego API real)
    return [
        "Inflación USA en foco",
        "Movimientos en Nasdaq",
        "Cripto con volatilidad"
    ]

def build_message(session):

    now = datetime.datetime.now().strftime("%H:%M")

    sentiment = get_sentiment()
    news = get_news()

    msg = f"""
📊 MARKET BRIEFING — {session}
⏰ {now}

━━━━━━━━━━━━━━━

🧠 SENTIMIENTO
{sentiment}

━━━━━━━━━━━━━━━

📰 CLAVES
- {news[0]}
- {news[1]}
- {news[2]}

━━━━━━━━━━━━━━━

📉 ACTIVOS

NSQ100
R: 18000 | S: 17500

BTC
R: 70000 | S: 65000

ORO
R: 2400 | S: 2300

DXY
R: 105 | S: 103

VIX
R: 20 | S: 15

BRENT
R: 85 | S: 80

━━━━━━━━━━━━━━━

⚠️ ACCIÓN

• Esperar confirmación  
• Evitar operar en noticias  
• Priorizar tendencia  

━━━━━━━━━━━━━━━
"""

    return msg

def run():
    session = "AUTO"
    message = build_message(session)
    send_telegram(message)

if __name__ == "__main__":
    run()
