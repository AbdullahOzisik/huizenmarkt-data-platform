import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="🏘️ Huizenmarkt Dashboard", layout="wide")
st.title("🏘️ Huizenmarkt Dashboard")

# RAW CSV vanaf GitHub
csv_url = "https://raw.githubusercontent.com/AbdullahOzisik/huizenmarkt-data-platform/main/woningdata_per_gemeente.csv"

try:
    df = pd.read_csv(csv_url)
    st.success("✅ Data succesvol geladen vanaf GitHub")

    # Gemeente selectie voor vergelijking
    gemeenten = sorted(df["gemeente"].dropna().unique())

    col1, col2 = st.columns(2)
    with col1:
        gemeente1 = st.selectbox("📍 Kies eerste gemeente", gemeenten, index=gemeenten.index("Amsterdam") if "Amsterdam" in gemeenten else 0)
    with col2:
        gemeente2 = st.selectbox("📍 Kies tweede gemeente", gemeenten, index=gemeenten.index("Rotterdam") if "Rotterdam" in gemeenten else 1)

    # Filter voor de twee gemeenten
    df_select = df[df["gemeente"].isin([gemeente1, gemeente2])]

    st.markdown("## 📊 Vergelijking: Gemiddeld Inkomen & WOZ")

    # Grafieken naast elkaar
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### 💰 Gemiddeld Inkomen in €")
        fig, ax = plt.subplots()
        ax.bar(df_select["gemeente"], df_select["gemiddeld_inkomen"], color="green")
        ax.set_ylabel("€")
        st.pyplot(fig)

    with col2:
        st.markdown(f"### 🏠 Gemiddelde WOZ-waarde in €")
        fig, ax = plt.subplots()
        ax.bar(df_select["gemeente"], df_select["gemiddelde_woz"], color="orange")
        ax.set_ylabel("€")
        st.pyplot(fig)

    st.markdown("---")

    # Algemene info
    st.subheader("📄 Dataoverzicht van geselecteerde gemeenten")
    st.dataframe(df_select, use_container_width=True)

    # Downloadknop
    st.download_button(
        label="📥 Download deze data als CSV",
        data=df_select.to_csv(index=False).encode("utf-8"),
        file_name="vergelijking_woningdata.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"❌ Fout bij laden van data: {e}")
