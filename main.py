import requests
import datetime

TELEGRAM_TOKEN = "8774099880:AAFyVd-Id8eC4sGVztg9W0Z-1kPstLu6Hb0"
CHAT_ID = "1373100163"

# -------------------- TELEGRAM --------------------
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# -------------------- DATOS --------------------
def get_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        data = requests.get(url).json()
        return data["quoteResponse"]["result"][0]["regularMarketPrice"]
    except:
        return None

def get_vix():
    return get_price("%5EVIX")

# -------------------- LÓGICA --------------------
def sentiment(vix):
    if vix is None:
        return "🟡 NEUTRAL"
    if vix > 20:
        return "🔴 RISK OFF"
    elif vix < 15:
        return "🟢 RISK ON"
    else:
        return "🟡 NEUTRAL"

def bias(price, level):
    if price is None:
        return "N/A"
    if price > level:
        return "🟢 ALCISTA"
    elif price < level:
        return "🔴 BAJISTA"
    else:
        return "🟡 NEUTRAL"

# -------------------- MENSAJE PRO --------------------
def build():

    now = datetime.datetime.now().strftime("%H:%M")

    # PRECIOS
    vix = get_vix()
    nasdaq = get_price("^NDX")
    btc = get_price("BTC-USD")
    gold = get_price("GC=F")
    dxy = get_price("DX-Y.NYB")
    brent = get_price("BZ=F")

    # SENTIMIENTO
    s = sentiment(vix)

    # BIAS SIMPLES (niveles guía)
    nasdaq_bias = bias(nasdaq, 18000)
    btc_bias = bias(btc, 70000)
    gold_bias = bias(gold, 2400)

    # SEÑAL GLOBAL
    if "🔴" in s:
        action = "🔴 SOLO SETUPS DEFENSIVOS"
    elif "🟢" in s:
        action = "🟢 PERMITE OPERATIVA"
    else:
        action = "🟡 ESPERAR CONFIRMACIÓN"

    msg = f"""
📊 MARKET BRIEFING PRO
⏰ {now}

━━━━━━━━━━━━━━━
🧠 RIESGO
{s}
VIX: {vix}

━━━━━━━━━━━━━━━
🧭 BIAS

NSQ100 → {nasdaq_bias}
BTC → {btc_bias}
ORO → {gold_bias}

━━━━━━━━━━━━━━━
📉 NIVELES CLAVE

NSQ100 → R: 18000 | S: 17500
BTC → R: 70000 | S: 65000
ORO → R: 2400 | S: 2300
DXY → R: 105 | S: 103
BRENT → R: 85 | S: 80

━━━━━━━━━━━━━━━
📰 MACRO HOY

• Inflación / tasas FED
• Movimiento en tech (Nasdaq)
• Volatilidad cripto

━━━━━━━━━━━━━━━
⚠️ PLAN

{action}

• Evitar entrada en noticias
• Confirmar estructura antes de entrar
• No sobreoperar

━━━━━━━━━━━━━━━
"""

    return msg

# -------------------- RUN --------------------
def run():
    send_telegram(build())

if __name__ == "__main__":
    run()
