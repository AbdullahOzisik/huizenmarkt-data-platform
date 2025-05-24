import streamlit as st
import pandas as pd

st.set_page_config(page_title="🏘️ Huizenmarkt Dashboard", layout="wide")
st.title("🏘️ Huizenmarkt Dashboard")

# Gebruik de RAW link van GitHub, niet de gewone weergavelink
csv_url = "https://raw.githubusercontent.com/AbdullahOzisik/huizenmarkt/main/woningdata_per_gemeente.csv"

try:
    # Laad CSV vanaf GitHub
    df = pd.read_csv(csv_url)
    st.success("✅ Data succesvol geladen vanaf GitHub")

    # Gemeente filter
    gemeenten = sorted(df["GEMEENTE"].dropna().unique())
    gekozen = st.selectbox("Selecteer een gemeente", ["Alle"] + gemeenten)

    if gekozen != "Alle":
        df = df[df["GEMEENTE"] == gekozen]

    # Toon data
    st.dataframe(df, use_container_width=True)

    # Download als CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="woningdata_per_gemeente.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"❌ Fout bij laden van data: {e}")
