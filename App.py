import streamlit as st
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator

st.set_page_config(page_title="Gold MCX Terminal", layout="centered")

st.title("🪙 Gold MCX & Global Terminal")
st.markdown("International Comex ani Technical Indicators varun market trend tpasaha.")

timeframe = st.selectbox("Select Timeframe", ["1h", "1d"])

if st.button("Run Market Analysis", type="primary"):
    with st.spinner('Fetching live data...'):
        try:
            comex = yf.Ticker("GC=F")
            df_comex = comex.history(period="10d", interval=timeframe)
            
            if df_comex.empty:
                st.error("Data milnyat adchan ahe. Krupaya punha prayatna kara.")
            else:
                current_comex = df_comex['Close'].iloc[-1]
                prev_comex = df_comex['Close'].iloc[-2]
                comex_chg = ((current_comex - prev_comex) / prev_comex) * 100
                
                rsi_val = 50.0
                if len(df_comex) > 14:
                    rsi_indicator = RSIIndicator(close=df_comex['Close'], window=14)
                    rsi_val = rsi_indicator.rsi().iloc[-1]
                
                st.metric(label="Comex Gold Price", value=f"${current_comex:.2f}", delta=f"{comex_chg:.2f}%")
                st.metric(label="RSI Indicator (14)", value=f"{rsi_val:.2f}")
                
                st.markdown("---")
                st.subheader("📊 Market Signal Verdict")
                
                if rsi_val < 30:
                    st.success("🟢 **BULLISH SIGNAL:** Market oversold zone madhe ahe. Bounce back chi shakhyata ahe.")
                elif rsi_val > 70:
                    st.error("🔴 **BEARISH SIGNAL:** Market overbought zone madhe ahe. Profit booking yeu shakte.")
                else:
                    st.info("🟡 **NEUTRAL / SIDEWAYS:** Market madhe konta hi strong extreme trend nahi.")
                    
        except Exception as e:
            st.error(f"Kahi tri chukle ahe: {e}")
