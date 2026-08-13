import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. Configuration de la page
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Credit risk AI Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Injection de CSS personnalisé (Style SaaS FinTech)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Style global */
    .main {
        background-color: #F8FAFC;
    }
    
    /* Cartes stylisées */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 500;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Personnalisation des boutons */
    .stButton > button {
        background: linear-gradient(135deg, #0066FF 0%, #0044B3 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 12px rgba(0, 102, 255, 0.25);
    }
    
    /* Titres d'onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 8px 16px;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Charger les modèles
# -----------------------------------------------------------------------------
@st.cache_resource
def load_models():
    model_ml = joblib.load('models/model.pkl')
    preprocessor = joblib.load('models/preprocessor.pkl')
    return model_ml, preprocessor

# (Assurez-vous de charger vos modèles ici si disponible)
# model_ml, preprocessor = load_models()

# -----------------------------------------------------------------------------
# 4. En-tête de la plateforme
# -----------------------------------------------------------------------------
st.markdown("<h1 style='color: #0F172A; font-weight: 800;'>🏦 Plateforme d'Éligibilité au Crédit</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 16px; margin-bottom: 30px;'>Système prédictif d'évaluation du risque bancaire basé sur l'IA</p>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Formulaire dans la barre latérale
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank.png", width=60)
    st.markdown("### 📋 Profil du Demandeur")
    st.caption("Renseignez les données du dossier")
    
    gender = st.selectbox("Genre", ["Male", "Female"])
    married = st.selectbox("État civil", ["Yes", "No"])
    education = st.selectbox("Niveau d'études", ["Graduate", "Not Graduate"])
    
    st.divider()
    
    applicant_income = st.number_input("Revenu Principal ($)", min_value=0, value=5000, step=500)
    coapplicant_income = st.number_input("Revenu Co-demandeur ($)", min_value=0, value=1500, step=500)
    loan_amount = st.number_input("Montant du Prêt ($)", min_value=0, value=150000, step=5000)
    loan_term = st.selectbox("Durée (mois)", [360, 180, 240, 120, 84])
    
    st.divider()
    
    credit_history = st.radio("Historique de crédit", [1.0, 0.0], format_func=lambda x: "Bon (Pas de retard)" if x == 1.0 else "Mauvais (Historique de défaut)")
    property_area = st.selectbox("Zone géographique", ["Urban", "Semiurban", "Rural"])
    
    predict_btn = st.button("📊 Analyser le Dossier")

# -----------------------------------------------------------------------------
# 6. Corps principal & Résultats
# -----------------------------------------------------------------------------

# Calculs préliminaires
total_income = applicant_income + coapplicant_income
debt_ratio = round((loan_amount / total_income), 2) if total_income > 0 else 0

# KPIs rapides
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Revenu Total</div>
            <div class="metric-value">{total_income:,.0f} $</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Montant Prêt</div>
            <div class="metric-value">{loan_amount:,.0f} $</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Ratio Prêt/Revenu</div>
            <div class="metric-value">{debt_ratio}x</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    credit_status_color = "#10B981" if credit_history == 1.0 else "#EF4444"
    credit_text = "Favorable" if credit_history == 1.0 else "Risqué"
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Historique Crédit</div>
            <div class="metric-value" style="color: {credit_status_color};">{credit_text}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Configuration des onglets
tab_decision, tab_analytics, tab_config = st.tabs(["🎯 Décision IA", "📊 Analyse Graphique", "⚙️ Paramètres Modèle"])

with tab_decision:
    if predict_btn:
        st.subheader("Résultat de l'analyse")
        # Exemple de logique de prédiction (À connecter avec votre modèle)
        if credit_history == 1.0 and debt_ratio < 30:
            st.success("✅ **PRÊT ACCORDÉ** — Le profil répond aux critères de solvabilité.")
        else:
            st.error("❌ **PRÊT REFUSÉ** — Le niveau de risque dépasse le seuil autorisé.")
    else:
        st.info("👈 Renseignez les paramètres dans le panneau latéral et cliquez sur **'Analyser le Dossier'**.")

with tab_analytics:
    st.subheader("Analyse comparative des Revenus et du Crédit")
    
    # Graphique Plotly moderne avec palette FinTech
    df_chart = pd.DataFrame({
        'Catégorie': ['Revenu Principal', 'Revenu Co-demandeur', 'Montant du Prêt'],
        'Valeur ($)': [applicant_income, coapplicant_income, loan_amount]
    })
    
    fig = px.bar(
        df_chart, 
        x='Catégorie', 
        y='Valeur ($)', 
        color='Catégorie',
        color_discrete_sequence=['#0066FF', '#38BDF8', '#F59E0B'],
        template='plotly_white'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family="sans-serif", size=12, color="#0F172A")
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab_config:
    st.subheader("Configuration des modèles d'Apprentissage Automatique")
    selected_model = st.radio("Sélectionner le moteur de prédiction :", ["Régression Logistique (ML)", "Réseau de Neurones Keras (Deep Learning)"])
    st.caption(f"Moteur actuellement actif : **{selected_model}**")