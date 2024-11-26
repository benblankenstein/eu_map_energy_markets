import streamlit as st
import pandas as pd
import plotly.express as px

# Laden der Daten
data = {
    "Region compared to Germany": [
        "Estonia", "Latvia", "Lithuania", "Belgium", "Bulgaria", "Denmark",
        "Finland", "France", "Greece", "United Kingdom", "Ireland", "Italy",
        "Croatia", "Netherlands", "Norway", "Austria", "Poland", "Portugal",
        "Romania", "Sweden", "Switzerland", "Slovakia", "Slovenia", "Spain",
        "Czech Republic", "Hungary", "Germany"
    ],
    "Bidding zones + capacity mechanism": [
        0.08, 0.08, 0.08, 0, 0.08, 0.08, 0, 0.08, 0.08, 0.08, 0.08, 0.14, 0.08,
        0.08, 0.14, 0.09, 0.08, 0.08, 0.08, 0.07, 0.08, 0.08, 0.08, 0.08, 0.08,
        0.08, 0
    ],
    "Intraday market": [
        0, 0, 0, 0, 0.12, 0, 0, 0, 0.16, 0.05, 0.2, 0.14, 0.15, 0, 0, 0, 0, 0.15,
        0.12, 0., 0.05, 0, 0.11, 0.15, 0.12, 0.1, 0
    ],
    "Balancing services": [
        0.07, 0.07, 0.07, 0.3, 0.21, 0.495, 0.46, 0.28, 0.28, 0.55, 0.53, 0.46,
        0.26, 0.33, 0.34, 0.11, 0.43, 0.34, 0.39, 0.49, 0.23, 0.22, 0.32, 0.48,
        0.46, 0.32, 0
    ],
    "Forward markets": [
        0, 0, 0, 0.17, 0.15, 0.1, 0.1, 0.05, 0.15, 0.1, 0, 0.1, 0, 0.08, 0.1,
        0.17, 0.17, 0, 0.15, 0.1, 0.08, 0.15, 0.15, 0.06, 0.11, 0.11, 0
    ],
    "Overall score": [
        0.15, 0.15, 0.15, 0.47, 0.55, 0.675, 0.56, 0.4, 0.66, 0.77, 0.81, 0.84,
        0.48, 0.48, 0.59, 0.37, 0.68, 0.57, 0.73, 0.66, 0.43, 0.44, 0.65, 0.77,
        0.77, 0.61, 0
    ],
    "Capacity mechanisms in Europe": [
        "Energy-Only-Market", "Energy-Only-Market", "Strategic reserve",
        "Strategic reserve", "Tender for new capacity", "Energy-Only-Market",
        "Strategic reserve", "Decentralized obligation", "Central buyer",
        "Central buyer", "Central buyer", "Central buyer",
        "Tender for new capacity", "Energy-Only-Market",
        "Energy-Only-Market", "Energy-Only-Market", "Central buyer",
        "Targeted capacity payment", "Energy-Only-Market", "Strategic reserve",
        "Energy-Only-Market", "Energy-Only-Market", "Energy-Only-Market",
        "Targeted capacity payment", "Energy-Only-Market", "Energy-Only-Market",
        "Strategic reserve"
    ]
}

df = pd.DataFrame(data)

# Farbcodierung für die Kapazitätsmechanismen
capacity_color_map = {
    "Energy-Only-Market": "#1f77b4",
    "Strategic reserve": "#ff7f0e",
    "Tender for new capacity": "#2ca02c",
    "Decentralized obligation": "#d62728",
    "Central buyer": "#9467bd",
    "Targeted capacity payment": "#8c564b"
}

# Streamlit App Layout
st.title('European Energy Markets Analysis')
st.markdown("""
- Based on the results of a paper by the Forschungsstelle für Energiewirtschaft e. V. (FfE)
- Analysed for different criteria and markets (bidding zones + capacity mechanism, intraday market, balancing services, forward markets)
- Summarised in an overall score
- A low score (green) indicates that the electricity market design is similar to that of Germany
- A high score (red) indicates a strong deviation from the German electricity market design
- The Capacity Mechanisms in Europe map shows the different approaches to capacity mechanisms

[Read the full paper here.](https://www.ffe.de/wp-content/uploads/2022/09/GSM20_Paper_G0105_European-Electricity-Markets_Ganz.pdf)
""")

selected_metric = st.sidebar.selectbox(
    'Select a metric to display:',
    options=[
        'Bidding zones + capacity mechanism',
        'Intraday market',
        'Balancing services',
        'Forward markets',
        'Overall score',
        'Capacity mechanisms in Europe'
    ],
    index=4
)

# Hover-Daten anpassen, damit nur die ausgewählte Metrik angezeigt wird
hover_data = {
    "Region compared to Germany": True,
    selected_metric: True
}

if selected_metric == "Capacity mechanisms in Europe":
    fig = px.choropleth(
        df,
        locations="Region compared to Germany",
        locationmode="country names",
        color=selected_metric,
        hover_name="Region compared to Germany",
        hover_data=hover_data,
        color_discrete_map=capacity_color_map,
        title="Capacity Mechanisms in Europe",
    )
    fig.update_layout(
        legend=dict(
            orientation="h",  # horizontale Ausrichtung
            x=0.5,  # Zentriert die Legende
            xanchor="center",
            y=-0.3  # Positioniert sie unterhalb der Karte
        )
    )

else:
    fig = px.choropleth(
        df,
        locations="Region compared to Germany",
        locationmode="country names",
        color=selected_metric,
        hover_name="Region compared to Germany",
        hover_data=hover_data,
        color_continuous_scale=[(0, "green"), (0.5, "yellow"), (1, "red")],
        title=f"{selected_metric} in Europe",
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            orientation='h',
            x=0.5,
            xanchor='center',
            y=-0.3
        )
    )

fig.update_geos(
    scope='europe',
    showcountries=True,
    countrycolor="LightGray",
    showcoastlines=True,
    coastlinecolor="LightBlue",
    projection_type="natural earth"
)

fig.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    height=600
)

st.plotly_chart(fig, use_container_width=True)
