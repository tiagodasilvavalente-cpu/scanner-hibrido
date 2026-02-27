import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.title("📈 Scanner Híbrido S&P 500")

url = "https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"
sp500_table = pd.read_csv(url)
sp500_tickers = sp500_table['Symbol'].tolist()

if st.button("Executar Scanner"):

    results = []
    progress = st.progress(0)

    for i, ticker in enumerate(sp500_tickers):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            score = 0

            # FUNDAMENTAL
            if info.get("revenueGrowth", 0) and info["revenueGrowth"] > 0.05:
                score += 2
            
            if info.get("trailingEps", 0) and info["trailingEps"] > 0:
                score += 1
            
            if info.get("profitMargins", 0) and info["profitMargins"] > 0.10:
                score += 1
            
            if info.get("debtToEquity", 999) < 100:
                score += 1
            
            if info.get("returnOnEquity", 0) and info["returnOnEquity"] > 0.10:
                score += 1

            # TÉCNICO
            hist = stock.history(period="6mo")

            if len(hist) > 120:
                hist["MA50"] = hist["Close"].rolling(50).mean()
                hist["MA200"] = hist["Close"].rolling(200).mean()

                last_price = hist["Close"].iloc[-1]
                ma50 = hist["MA50"].iloc[-1]
                ma200 = hist["MA200"].iloc[-1]

                if ma50 > ma200:
                    score += 2

                if last_price > ma50:
                    score += 1

                recent = hist.iloc[-40:]
                first_half = recent.iloc[:20]
                second_half = recent.iloc[20:]

                if second_half["Close"].max() > first_half["Close"].max():
                    score += 1

                if second_half["Close"].min() > first_half["Close"].min():
                    score += 1

            name = info.get("shortName", "N/A")
            results.append((ticker, name, score))

            progress.progress((i+1)/len(sp500_tickers))

            time.sleep(0.02)

        except:
            pass

    df = pd.DataFrame(results, columns=["Ticker", "Nome", "Score"])
    df = df.sort_values("Score", ascending=False)

    st.subheader("🔥 Top 10 Força")
    st.dataframe(df.head(10))

    st.subheader("❄️ Top 10 Fraqueza")
    st.dataframe(df.tail(10))