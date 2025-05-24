import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🏘️ Huizenmarkt Dashboard", layout="wide")
st.title("🏘️ Huizenmarkt Dashboard")

# ✅ Vervang deze met de correcte RAW GitHub link
csv_url = "https://raw.githubusercontent.com/AbdullahOzisik/huizenmarkt-data-platform/main/woningdata_per_gemeente.csv"

try:
    df = pd.read_csv(csv_url)
    st.success("✅ Data succesvol geladen vanaf GitHub")

    if "gemeente" not in df.columns:
        st.error("❌ Kolom 'gemeente' niet gevonden in de dataset.")
        st.stop()

    # --- FILTER EN VERGELIJKING ---
    st.header("📍 Vergelijk Gemeenten")
    col1, col2 = st.columns(2)
    gemeenten = sorted(df["gemeente"].dropna().unique())
    g1 = col1.selectbox("Gemeente 1", gemeenten)
    g2 = col2.selectbox("Gemeente 2", gemeenten, index=1)

    df_g1 = df[df["gemeente"] == g1]
    df_g2 = df[df["gemeente"] == g2]

    # --- METRIEKEN VERGELIJKING ---
    st.subheader(f"📊 Vergelijking: {g1} vs {g2}")
    col1, col2, col3 = st.columns(3)

    def get_val(col, gdf):
        return gdf[col].values[0] if col in gdf.columns else None

    col1.metric("Gemiddeld Inkomen (€)", f"{get_val('gemiddeld_inkomen', df_g1):,.0f}", f"{get_val('gemiddeld_inkomen', df_g1) - get_val('gemiddeld_inkomen', df_g2):,.0f}")
    col2.metric("WOZ-waarde (€)", f"{get_val('gemiddelde_woz', df_g1):,.0f}", f"{get_val('gemiddelde_woz', df_g1) - get_val('gemiddelde_woz', df_g2):,.0f}")
    col3.metric("Totaal Inwoners", f"{get_val('totaal_inwoners', df_g1):,.0f}")

    st.markdown("---")

    # --- HISTOGRAMMEN ---
    st.subheader("📈 WOZ-waarde & Inkomen Histogrammen")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.histogram(df, x="gemiddelde_woz", nbins=30, title="Histogram: WOZ-waarde"),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            px.histogram(df, x="gemiddeld_inkomen", nbins=30, title="Histogram: Gemiddeld Inkomen"),
            use_container_width=True
        )

    # --- KAART ---
    if "latitude" in df.columns and "longitude" in df.columns:
        st.subheader("🗺️ Kaart: WOZ-waarde per Gemeente")
        fig_map = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="gemiddelde_woz",
            size="gemiddelde_woz",
            hover_name="gemeente",
            color_continuous_scale="RdBu_r",
            size_max=20,
            zoom=6,
            mapbox_style="carto-positron",
            title="WOZ-waarde (blauw = goedkoper, rood = duurder)"
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # --- DOWNLOAD ---
    st.subheader("📥 Download")
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="woningdata_per_gemeente.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"❌ Fout bij laden van data: {e}")
