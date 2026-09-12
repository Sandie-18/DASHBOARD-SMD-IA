"""
Module 8 — Déploiement d'un dashboard marketing
Projet pédagogique : Analyse & Optimisation Marketing basée sur la Segmentation Client

Dashboard interactif réunissant TOUTES les données du projet :
  - Segmentation client (Module 3/4)      -> data/clients_dashboard.csv
  - Performances des campagnes (Module 5) -> data/kpi_dashboard.csv
  - Prédiction de la valeur client (Module 6), déjà incluse dans clients_dashboard.csv

Lancement local :
    pip install -r requirements.txt
    streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# Configuration générale de la page
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Marketing — Segmentation Client",
    page_icon="📊",
    layout="wide",
)

PERSONA_COLORS = {
    "Client Actif Multi-catégories": "#4C72B0",
    "Client Occasionnel": "#DD8452",
}


@st.cache_data
def load_data():
    clients = pd.read_csv("data/clients_dashboard.csv")
    kpi = pd.read_csv("data/kpi_dashboard.csv")
    return clients, kpi


clients, kpi = load_data()

# ----------------------------------------------------------------------------
# Barre latérale — filtres (interactivité demandée par la consigne du M8)
# ----------------------------------------------------------------------------
st.sidebar.title("🎛️ Filtres")

personas = sorted(clients["Persona"].unique())
persona_sel = st.sidebar.multiselect("Segment client (persona)", personas, default=personas)

canaux = sorted(kpi["channel"].unique())
canal_sel = st.sidebar.multiselect("Canal marketing", canaux, default=canaux)

age_min, age_max = int(clients["age"].min()), int(clients["age"].max())
age_range = st.sidebar.slider("Âge des clients", age_min, age_max, (age_min, age_max))

st.sidebar.markdown("---")
st.sidebar.caption(
    "Données issues des Modules 2 à 6 du projet : nettoyage, segmentation K-means, "
    "profilage, KPIs des campagnes et prédiction de la valeur client (CLV)."
)

clients_f = clients[
    clients["Persona"].isin(persona_sel)
    & clients["age"].between(age_range[0], age_range[1])
]
kpi_f = kpi[kpi["channel"].isin(canal_sel)]

# ----------------------------------------------------------------------------
# En-tête + indicateurs clés (KPIs globaux)
# ----------------------------------------------------------------------------
st.title("📊 Dashboard Marketing — Segmentation Client")
st.caption("Module 8 · Visualisation interactive des segments clients et des performances marketing")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Clients (filtrés)", f"{len(clients_f)}")
k2.metric("Chiffre d'affaires total", f"{clients_f['Total_Revenue'].sum():,.0f} €")
k3.metric("Panier moyen", f"{clients_f['Avg_Basket_Value'].mean():,.1f} €" if len(clients_f) else "—")
k4.metric("Budget marketing (filtré)", f"{kpi_f['budget'].sum():,.0f} €")
k5.metric("ROI moyen des campagnes", f"{kpi_f['ROI (%)'].mean():,.0f} %" if len(kpi_f) else "—")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(
    ["🧩 Segmentation client", "📈 Performance des campagnes", "💰 Valeur client (CLV)", "🗂️ Explorateur de données"]
)

# ----------------------------------------------------------------------------
# Onglet 1 — Segmentation client (Modules 3 & 4)
# ----------------------------------------------------------------------------
with tab1:
    c1, c2 = st.columns([1.3, 1])

    with c1:
        st.subheader("Clients projetés sur les 2 axes de l'ACP")
        fig_pca = px.scatter(
            clients_f, x="PCA1", y="PCA2", color="Persona", text="name",
            color_discrete_map=PERSONA_COLORS, size="Total_Revenue", size_max=40,
            hover_data={"age": True, "total_spent": True, "Nb_Transactions": True, "PCA1": False, "PCA2": False},
        )
        fig_pca.update_traces(textposition="top center")
        fig_pca.update_layout(legend_title_text="Persona")
        st.plotly_chart(fig_pca, use_container_width=True)

    with c2:
        st.subheader("Répartition des segments")
        seg_counts = clients_f["Persona"].value_counts().reset_index()
        seg_counts.columns = ["Persona", "Nb_Clients"]
        fig_pie = px.pie(
            seg_counts, names="Persona", values="Nb_Clients",
            color="Persona", color_discrete_map=PERSONA_COLORS, hole=0.45,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Profil moyen par segment")
    profile_cols = ["age", "total_spent", "Nb_Transactions", "Total_Quantity", "Avg_Basket_Value", "CLV_predite_RF"]
    profile = clients_f.groupby("Persona")[profile_cols].mean().round(1)
    profile["Nb_Clients"] = clients_f.groupby("Persona").size()
    st.dataframe(profile, use_container_width=True)

    fig_bar = px.bar(
        clients_f, x="name", y=["Clothing", "Footwear", "Outerwear", "Accessories"],
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"value": "Quantité achetée", "name": "Client", "variable": "Catégorie"},
        title="Quantités achetées par catégorie et par client",
        facet_col="Persona" if len(persona_sel) > 1 else None,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------------------------------------------------------
# Onglet 2 — Performance des campagnes marketing (Module 5)
# ----------------------------------------------------------------------------
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("ROI par campagne")
        fig_roi = px.bar(
            kpi_f, x="campaign_id", y="ROI (%)", color="channel",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"campaign_id": "Campagne"},
        )
        fig_roi.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_roi, use_container_width=True)

    with c2:
        st.subheader("Coût par acquisition (CPA)")
        fig_cpa = px.bar(
            kpi_f, x="campaign_id", y="CPA (€)", color="channel",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"campaign_id": "Campagne"},
        )
        st.plotly_chart(fig_cpa, use_container_width=True)

    st.subheader("KPIs moyens par canal")
    kpi_par_canal = kpi_f.groupby("channel")[["CTR (%)", "Taux_conversion (%)", "ROI (%)", "CPA (€)"]].mean().round(2)
    c3, c4 = st.columns([1, 1.4])
    with c3:
        st.dataframe(kpi_par_canal, use_container_width=True)
    with c4:
        fig_radar = go.Figure()
        for canal in kpi_par_canal.index:
            fig_radar.add_trace(go.Scatterpolar(
                r=[kpi_par_canal.loc[canal, "CTR (%)"], kpi_par_canal.loc[canal, "Taux_conversion (%)"],
                   kpi_par_canal.loc[canal, "ROI (%)"] / 20],  # ROI ramené à une échelle comparable
                theta=["CTR (%)", "Taux de conversion (%)", "ROI (/20)"],
                fill="toself", name=canal,
            ))
        fig_radar.update_layout(title="Comparaison des canaux (échelles ajustées)", showlegend=True)
        st.plotly_chart(fig_radar, use_container_width=True)

    st.subheader("Campagne associée à chaque segment client")
    camp_seg = clients_f.dropna(subset=["campagne_attribuee"])[["name", "Persona", "canal_prefere", "campagne_attribuee"]]
    st.dataframe(camp_seg, use_container_width=True)

# ----------------------------------------------------------------------------
# Onglet 3 — Valeur client / CLV (Module 6)
# ----------------------------------------------------------------------------
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("CLV réelle vs CLV prédite (Random Forest)")
        fig_clv = px.scatter(
            clients_f, x="Total_Revenue", y="CLV_predite_RF", color="Persona",
            text="name", color_discrete_map=PERSONA_COLORS,
            labels={"Total_Revenue": "CLV réelle (€)", "CLV_predite_RF": "CLV prédite (€)"},
        )
        max_val = max(clients_f["Total_Revenue"].max(), clients_f["CLV_predite_RF"].max()) + 20 if len(clients_f) else 100
        fig_clv.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val, line=dict(dash="dash", color="grey"))
        fig_clv.update_traces(textposition="top center", marker=dict(size=14))
        st.plotly_chart(fig_clv, use_container_width=True)

    with c2:
        st.subheader("Clients à forte valeur")
        clients_f_disp = clients_f.copy()
        clients_f_disp["Statut"] = clients_f_disp["High_Value"].map({1: "Forte valeur", 0: "Valeur standard"})
        fig_hv = px.bar(
            clients_f_disp.sort_values("CLV_predite_RF", ascending=False),
            x="name", y="CLV_predite_RF", color="Statut",
            color_discrete_map={"Forte valeur": "#55A868", "Valeur standard": "#C44E52"},
            labels={"CLV_predite_RF": "CLV prédite (€)", "name": "Client"},
        )
        st.plotly_chart(fig_hv, use_container_width=True)

# ----------------------------------------------------------------------------
# Onglet 4 — Explorateur de données (table fusionnée complète)
# ----------------------------------------------------------------------------
with tab4:
    st.subheader("Table clients — toutes les données fusionnées (M2 à M6)")
    st.dataframe(clients_f, use_container_width=True)
    st.download_button(
        "⬇️ Télécharger les clients filtrés (CSV)",
        clients_f.to_csv(index=False).encode("utf-8"),
        file_name="clients_filtres.csv",
    )

    st.subheader("Table campagnes marketing — KPIs")
    st.dataframe(kpi_f, use_container_width=True)
    st.download_button(
        "⬇️ Télécharger les campagnes filtrées (CSV)",
        kpi_f.to_csv(index=False).encode("utf-8"),
        file_name="campagnes_filtrees.csv",
    )

st.markdown("---")
st.caption(
    "Projet pédagogique — Analyse & Optimisation Marketing basée sur la Segmentation Client · Module 8"
)
