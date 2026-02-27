import streamlit as st
from scanner_engine import run_scanner

st.title("📈 Scanner Híbrido S&P 500")

if st.button("Executar Scanner"):
    with st.spinner("A calcular..."):
        df = run_scanner()
        st.dataframe(df.head(20))
