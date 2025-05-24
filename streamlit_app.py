import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🏘️ Huizenmarkt Dashboard", layout="wide")
st.title("🏘️ Huizenmarkt Dashboard")

# CSV vanaf GitHub
csv_url = "https://raw.githubusercontent.com/AbdullahOzisik/huizenmarkt-data-platform/main/woningdata_per_gemeente.csv"

try:
    df = pd.read_csv(csv_url)
    st.success("✅ Data succesvol geladen vanaf GitHub")

    # Selecteer twee gemeenten om te vergelijken
    gemeenten = sorted(df["gemeente"].dropna().unique())
    col1, col2 = st.columns(2)
    g1 = col1.selectbox("📍 Selecteer gemeente 1", gemeenten, index=gemeenten.index("Amsterdam") if "Amsterdam" in gemeenten else 0)
    g2 = col2.selectbox("📍 Selecteer gemeente 2", gemeenten, index=gemeenten.index("Rotterdam") if "Rotterdam" in gemeenten else 1)

    data_g1 = df[df["gemeente"] == g1].iloc[0]
    data_g2 = df[df["gemeente"] == g2].iloc[0]

    # ➕ Vergelijkingskaarten
    st.subheader("📊 Vergelijking Statistieken")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gemiddeld Inkomen", f"€{data_g1['gemiddeld_inkomen']:,.0f}", f"{data_g1['gemiddeld_inkomen'] - data_g2['gemiddeld_inkomen']:,.0f} verschil" if g1 != g2 else "")
    col2.metric("Gemiddelde WOZ", f"€{data_g1['gemiddelde_woz']:,.0f}", f"{data_g1['gemiddelde_woz'] - data_g2['gemiddelde_woz']:,.0f} verschil" if g1 != g2 else "")
    col3.metric("Totaal Inwoners", f"{int(data_g1['totaal_inwoners']):,}", f"{int(data_g1['totaal_inwoners'] - data_g2['totaal_inwoners']):,} verschil" if g1 != g2 else "")

    st.markdown("---")

    # ➗ Grafieken naast elkaar
    st.subheader("📈 Inkomens- en WOZ-verdeling")
    col1, col2 = st.columns(2)

    with col1:
        fig_inkomen = px.histogram(df, x="gemiddeld_inkomen", nbins=30, title="📊 Inkomensverdeling", color_discrete_sequence=["#1f77b4"])
        fig_inkomen.add_vline(x=data_g1['gemiddeld_inkomen'], line_dash="dash", line_color="red", annotation_text=g1, annotation_position="top right")
        fig_inkomen.add_vline(x=data_g2['gemiddeld_inkomen'], line_dash="dash", line_color="green", annotation_text=g2, annotation_position="top left")
        st.plotly_chart(fig_inkomen, use_container_width=True)

    with col2:
        fig_woz = px.histogram(df, x="gemiddelde_woz", nbins=30, title="🏠 WOZ-waardeverdeling", color_discrete_sequence=["#ff7f0e"])
        fig_woz.add_vline(x=data_g1['gemiddelde_woz'], line_dash="dash", line_color="red", annotation_text=g1, annotation_position="top right")
        fig_woz.add_vline(x=data_g2['gemiddelde_woz'], line_dash="dash", line_color="green", annotation_text=g2, annotation_position="top left")
        st.plotly_chart(fig_woz, use_container_width=True)

    st.markdown("---")

    # ➕ Bonus: kaartje met WOZ per gemeente (rood = duur, blauw = goedkoop)
    st.subheader("🗺️ WOZ-waarde per gemeente")
    if "latitude" in df.columns and "longitude" in df.columns:
        map_fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="gemiddelde_woz",
            hover_name="gemeente",
            size="gemiddelde_woz",
            color_continuous_scale="RdBu_r",
            mapbox_style="carto-positron",
            zoom=6,
            title="Kaart: WOZ-waarde per gemeente"
        )
        st.plotly_chart(map_fig, use_container_width=True)
    else:
        st.info("ℹ️ Voeg latitude en longitude toe aan je CSV om de kaart te activeren.")

    # Downloadknop
    st.download_button(
        label="📥 Download huidige data als CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="woningdata_per_gemeente.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"❌ Fout bij laden van data: {e}")
