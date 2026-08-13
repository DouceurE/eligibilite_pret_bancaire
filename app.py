import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuration de la page
st.set_page_config(
    page_title="FinTech AI | Éligibilité au Prêt",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injection de CSS personnalisé pour un style moderne
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(42, 82, 152, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Chargement du modèle
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('models/model.pkl')
        return model
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return None

model = load_assets()

# 4. Barre latérale (Sidebar) pour l'identité et les paramètres
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/bank.png", width=80)
    st.title("FinTech")
    st.markdown("---")
    st.markdown("### ⚙️ Paramètres système")
    engine = st.radio("Moteur de prédiction", ["Modèle ML Principal (Random Forest/LogReg)", "Réseau de Neurones (Keras)"])
    st.markdown("---")
    st.caption("🚀 Version 2.0 | Système d'Évaluation de Risque")

# 5. En-tête Principal
st.title("💳 Évaluation Automatisée de Crédit")
st.markdown("Système d'intelligence artificielle d'analyse de solvabilité bancaire en temps réel.")

# 6. Organisation en Onglets (Formulaire vs Analytics)
tab1, tab2 = st.tabs(["📝 Formulaire de Demande", "📊 Analyse Comparative"])

with tab1:
    with st.form("loan_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 👤 Demandeur")
            gender = st.selectbox("Genre", ["Male", "Female"])
            married = st.selectbox("Statut Marital", ["Yes", "No"])
            dependents = st.selectbox("Personnes à charge", ["0", "1", "2", "3+"])
            education = st.selectbox("Niveau d'Études", ["Graduate", "Not Graduate"])
            self_employed = st.selectbox("Indépendant", ["Yes", "No"])

        with col2:
            st.markdown("#### 💰 Situation Financière")
            applicant_income = st.number_input("Revenu Principal ($)", min_value=0, value=5000, step=500)
            coapplicant_income = st.number_input("Revenu Co-demandeur ($)", min_value=0, value=0, step=500)
            loan_amount = st.number_input("Montant Sollicité ($ en milliers)", min_value=1, value=150, step=10)
            loan_term = st.number_input("Durée du Prêt (Jours)", min_value=12, value=360, step=12)

        with col3:
            st.markdown("#### 📜 Risque & Dossier")
            credit_history = st.selectbox("Historique de Crédit", [1.0, 0.0], format_func=lambda x: "✅ Exemplaire (1.0)" if x == 1.0 else "❌ Défavorable (0.0)")
            property_area = st.selectbox("Zone de Résidence", ["Urban", "Semiurban", "Rural"])

        submit = st.form_submit_button("🚀 Lancer l'Évaluation du Dossier", use_container_width=True)

    if submit:
        # Préparation des données
        input_data = pd.DataFrame([{
            'Gender': gender, 'Married': married, 'Dependents': dependents,
            'Education': education, 'Self_Employed': self_employed,
            'ApplicantIncome': applicant_income, 'CoapplicantIncome': coapplicant_income,
            'LoanAmount': loan_amount, 'Loan_Amount_Term': loan_term,
            'Credit_History': credit_history, 'Property_Area': property_area
        }])

        st.markdown("---")
        st.subheader("📋 Décision du Système")

        if model is not None:
            encoded_data = pd.get_dummies(input_data)
            model_features = model.feature_names_in_
            final_data = encoded_data.reindex(columns=model_features, fill_value=0)

            prediction = model.predict(final_data)[0]
            prob = model.predict_proba(final_data)[0][1] if hasattr(model, "predict_proba") else (1.0 if prediction == 1 else 0.0)

            # Cartes Métriques et Indicateurs visuels
            m_col1, m_col2, m_col3 = st.columns(3)

            with m_col1:
                st.metric("Décision Automatique", "ACCORDÉ" if prediction == 1 else "REFUSÉ", delta="Favorable" if prediction == 1 else "-Défavorable")

            with m_col2:
                st.metric("Score de Confiance", f"{prob*100:.1f}%")

            with m_col3:
                total_inc = applicant_income + coapplicant_income
                ratio = (loan_amount * 1000) / (total_inc + 1e-5)
                st.metric("Ratio Dette / Revenu", f"{ratio:.1f}x")

            # Jauge visuelle Plotly
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Probabilité d'Éligibilité (%)"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2a5298"},
                    'steps': [
                        {'range': [0, 50], 'color': "#ffcdd2"},
                        {'range': [50, 75], 'color': "#fff9c4"},
                        {'range': [75, 100], 'color': "#c8e6c9"}
                    ],
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("📈 Visualisation des Revenus vs Montant Demandé")
    
    # Graphique interactif
    sample_df = pd.DataFrame({
        "Categorie": ["Revenu Demandeur", "Revenu Co-demandeur", "Montant Prêt (x1000)"],
        "Montant ($)": [applicant_income, coapplicant_income, loan_amount * 1000]
    })
    
    fig_bar = px.bar(sample_df, x="Categorie", y="Montant ($)", color="Categorie", title="Aperçu des montants de la demande actuelle")
    st.plotly_chart(fig_bar, use_container_width=True)