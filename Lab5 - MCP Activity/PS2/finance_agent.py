import streamlit as st
import requests
import yfinance as yf
from groq import Groq
import os;

# ---------------- CONFIG ----------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ---------------- UI ----------------
st.title("🌍 Currency & Stock Market Agent (Groq Powered)")

country = st.text_input("Enter Country Name (Japan, India, US, UK, China)")

if st.button("Get Details"):

    country_data = {
        "Japan": {"currency": "JPY", "index": "^N225", "exchange": "Tokyo Stock Exchange"},
        "India": {"currency": "INR", "index": "^BSESN", "exchange": "Bombay Stock Exchange"},
        "US": {"currency": "USD", "index": "^GSPC", "exchange": "New York Stock Exchange"},
        "UK": {"currency": "GBP", "index": "^FTSE", "exchange": "London Stock Exchange"},
        "China": {"currency": "CNY", "index": "000001.SS", "exchange": "Shanghai Stock Exchange"}
    }

    if country in country_data:

        currency = country_data[country]["currency"]
        index_symbol = country_data[country]["index"]
        exchange_name = country_data[country]["exchange"]

        # -------- Exchange Rates --------
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{currency}"
        response = requests.get(url).json()

        usd = response["conversion_rates"]["USD"]
        inr = response["conversion_rates"]["INR"]
        gbp = response["conversion_rates"]["GBP"]
        eur = response["conversion_rates"]["EUR"]

        # -------- Stock Index --------
        stock = yf.Ticker(index_symbol)
        stock_data = stock.history(period="1d")
        latest_value = stock_data["Close"].iloc[-1]

        # -------- LLM Explanation --------
        explanation_prompt = f"""
        Explain the importance of the currency {currency}
        and the role of {exchange_name} in the economy of {country}.
        """

        explanation = ask_llm(explanation_prompt)

        # -------- Display --------
        st.subheader("💱 Official Currency")
        st.write(currency)

        st.subheader("📊 Exchange Rate (1 Unit)")
        st.write(f"{currency} → USD: {usd}")
        st.write(f"{currency} → INR: {inr}")
        st.write(f"{currency} → GBP: {gbp}")
        st.write(f"{currency} → EUR: {eur}")

        st.subheader("📈 Stock Exchange")
        st.write(exchange_name)
        st.write(f"Index Value: {latest_value}")

        st.subheader("📍 Google Maps Location")
        st.write(f"https://www.google.com/maps/search/{exchange_name}")

        st.subheader("📘 Explanation")
        st.write(explanation)

    else:
        st.write("Country not available.")
