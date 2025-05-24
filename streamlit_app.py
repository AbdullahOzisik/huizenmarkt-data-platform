import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🏘️ Huizenmarkt Dashboard", layout="wide")
st.title("🏘️ Huizenmarkt Dashboard")

# RAW GitHub CSV-link
csv_url = "https://raw.githubusercontent.com/AbdullahOzisik/huizenmarkt-data-platform/main/woningdata_per_gemeente.csv"

try:
    df = pd.read_csv(csv_url)
    st.success("✅ Data succesvol geladen vanaf GitHub")

    # Check op kolommen + datatypes
    df.columns = df.columns.str.lower()

    # Gemeente selecties voor vergelijking
    gemeenten = sorted(df["gemeente"].dropna().unique())
    col1, col2 = st.columns(2)
    g1 = col1.selectbox("📍 Gemeente 1", gemeenten, key="g1")
    g2 = col2.selectbox("📍 Gemeente 2", gemeenten, index=gemeenten.index("Amsterdam") if "Amsterdam" in gemeenten else 0, key="g2")

    df_g1 = df[df["gemeente"] == g1]
    df_g2 = df[df["gemeente"] == g2]

    # Statistieken
    st.subheader("📊 Statistieken Vergelijking")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Gemiddeld Inkomen " + g1, f"€{df_g1['gemiddeld_inkomen'].values[0]:,.0f}")
        st.metric("WOZ-waarde " + g1, f"€{df_g1['gemiddelde_woz'].values[0]:,.0f}")
    with col2:
        st.metric("Gemiddeld Inkomen " + g2, f"€{df_g2['gemiddeld_inkomen'].values[0]:,.0f}")
        st.metric("WOZ-waarde " + g2, f"€{df_g2['gemiddelde_woz'].values[0]:,.0f}")

    st.markdown("---")

    # Histogrammen
    st.subheader("📈 WOZ & Inkomen Verdeling")
    col1, col2 = st.columns(2)
    with col1:
        fig_woz = px.histogram(df, x="gemiddelde_woz", nbins=30, title="WOZ-waarde verdeling")
        st.plotly_chart(fig_woz, use_container_width=True)
    with col2:
        fig_inkomen = px.histogram(df, x="gemiddeld_inkomen", nbins=30, title="Gemiddeld Inkomen verdeling")
        st.plotly_chart(fig_inkomen, use_container_width=True)

    # Kaart - we nemen aan dat lat/lon kolommen bestaan
    if "latitude" in df.columns and "longitude" in df.columns:
        st.subheader("🗺️ Kaart: WOZ per gemeente")
        fig_map = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="gemiddelde_woz",
            color_continuous_scale=["blue", "red"],
            hover_name="gemeente",
            size_max=15,
            zoom=6,
            mapbox_style="carto-positron",
            title="WOZ-waarde per gemeente"
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("📍 Geen locatiegegevens gevonden om kaart te maken (latitude/longitude kolommen ontbreken).")

    # Ruwe data bekijken
    st.subheader("📄 Dataoverzicht")
    st.dataframe(df, use_container_width=True)

    # Downloadknop
    st.download_button(
        label="📥 Download huidige data als CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="woningdata_per_gemeente.csv",
        mime="text/csv"
    )

    # Check op jaartal
    if "jaar" in df.columns:
        jaren = sorted(df["jaar"].unique())
        st.sidebar.selectbox("🗓️ Kies jaar", jaren)
    else:
        st.info("ℹ️ Er lijkt geen kolom met jaartal in de dataset te zitten.")

except Exception as e:
    st.error(f"❌ Fout bij laden van data: {e}")
