import streamlit as st
import pandas as pd

st.set_page_config(page_title="🏘️ Huizenmarkt Dashboard", layout="wide")
st.title("🏘️ Huizenmarkt Dashboard")

# RAW GitHub CSV-link
csv_url = "https://raw.githubusercontent.com/AbdullahOzisik/huizenmarkt-data-platform/main/woningdata_per_gemeente.csv"

try:
    df = pd.read_csv(csv_url)
    st.success("✅ Data succesvol geladen vanaf GitHub")

    # Gemeente filter
    gemeenten = sorted(df["gemeente"].dropna().unique())
    gekozen = st.selectbox("📍 Selecteer een gemeente", ["Alle"] + gemeenten)

    if gekozen != "Alle":
        df = df[df["gemeente"] == gekozen]

    # Toon hoofd-statistieken
    st.subheader("📊 Statistieken")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gemiddeld Inkomen (€)", f"{df['gemiddeld_inkomen'].mean():,.0f}")
    col2.metric("Gem. WOZ-waarde (€)", f"{df['gemiddelde_woz'].mean():,.0f}")
    col3.metric("Totaal Inwoners", f"{df['totaal_inwoners'].sum():,.0f}")

    st.markdown("---")

    # Bar chart: inkomen en WOZ per gemeente
    st.subheader("💰 Gemiddeld Inkomen vs. WOZ-waarde per gemeente")
    chart_data = df[["gemeente", "gemiddeld_inkomen", "gemiddelde_woz"]].sort_values("gemiddeld_inkomen", ascending=False)
    st.bar_chart(chart_data.set_index("gemeente"))

    st.markdown("---")

    # Toon de ruwe data
    st.subheader("📄 Dataoverzicht")
    st.dataframe(df, use_container_width=True)

    # Downloadknop
    st.download_button(
        label="📥 Download huidige data als CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="woningdata_per_gemeente.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"❌ Fout bij laden van data: {e}")
