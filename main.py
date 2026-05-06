import requests
import datetime

TELEGRAM_TOKEN = "8774099880:AAFyVd-Id8eC4sGVztg9W0Z-1kPstLu6Hb0"
CHAT_ID = "1373100163"

# ---------------- TELEGRAM ----------------
def send(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# ---------------- DATOS ----------------
def price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        data = requests.get(url).json()
        return data["quoteResponse"]["result"][0]["regularMarketPrice"]
    except:
        return None

# ---------------- SESIÓN ----------------
def get_session():
    hour = datetime.datetime.utcnow().hour

    if 0 <= hour < 8:
        return "🌏 TOKYO SESSION"
    elif 12 <= hour < 20:
        return "🇺🇸 NEW YORK SESSION"
    else:
        return "⏳ FUERA DE SESIÓN"

# ---------------- SENTIMIENTO ----------------
def sentiment(vix, dxy, btc):

    if None in (vix, dxy, btc):
        return "🟡 MIXTO"

    if vix > 20 and dxy > 104:
        return "🔴 RISK OFF"

    if vix < 15 and btc > 65000:
        return "🟢 RISK ON"

    return "🟡 MIXTO"

# ---------------- SETUPS ----------------
def setup(price, r, s, sentiment):

    if price is None:
        return "N/A"

    # LONG
    if price > r and "🟢" in sentiment:
        return "🟢 LONG SETUP"

    # SHORT
    if price < s and "🔴" in sentiment:
        return "🔴 SHORT SETUP"

    return "🟡 NO TRADE"

# ---------------- MENSAJE ----------------
def build():

    now = datetime.datetime.now().strftime("%H:%M")
    session = get_session()

    # DATOS
    vix = price("%5EVIX")
    dxy = price("DX-Y.NYB")
    btc = price("BTC-USD")
    nasdaq = price("^NDX")
    gold = price("GC=F")

    # CONTEXTO
    s = sentiment(vix, dxy, btc)

    # NIVELES
    nsq_r, nsq_s = 18000, 17500
    btc_r, btc_s = 70000, 65000
    gold_r, gold_s = 2400, 2300

    # SETUPS
    nsq_setup = setup(nasdaq, nsq_r, nsq_s, s)
    btc_setup = setup(btc, btc_r, btc_s, s)
    gold_setup = setup(gold, gold_r, gold_s, s)

    # DECISIÓN GLOBAL
    if "LONG" in (nsq_setup + btc_setup):
        decision = "🟢 MERCADO OPERABLE (LONG)"
    elif "SHORT" in (nsq_setup + btc_setup):
        decision = "🔴 MERCADO OPERABLE (SHORT)"
    else:
        decision = "🟡 NO OPERAR / ESPERAR"

    msg = f"""
📊 MARKET BRIEFING PRO
{session} | {now}

━━━━━━━━━━━━━━━
🧠 CONTEXTO

{s}
VIX: {vix} | DXY: {dxy}

━━━━━━━━━━━━━━━
🚨 SETUPS

NSQ100 → {nsq_setup}
BTC → {btc_setup}
ORO → {gold_setup}

━━━━━━━━━━━━━━━
📉 NIVELES

NSQ100 → {nsq_r} / {nsq_s}
BTC → {btc_r} / {btc_s}
ORO → {gold_r} / {gold_s}

━━━━━━━━━━━━━━━
⚠️ DECISIÓN FINAL

{decision}

• Solo entrar con ruptura confirmada
• Evitar operar en rango
• Priorizar contexto del mercado

━━━━━━━━━━━━━━━
"""

    return msg

# ---------------- RUN ----------------
def run():
    send(build())

if __name__ == "__main__":
    run()
