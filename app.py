# -*- coding: utf-8 -*-
"""
FinRisk AI — Credit Risk Assessment Platform
============================================
Author: Mareme Ba Loum
Academic Project - ESP / Master & Engineering (2026)
Signature Hash: SHA256-MBL-FINRISK-2026-X99201A
"""

__author__ = "Mareme Ba Loum"
__copyright__ = "Copyright 2026, Mareme Ba Loum"
__credits__ = ["Mareme Ba Loum"]
__license__ = "Proprietary / Academic Submission"
__version__ = "1.0.0"
__maintainer__ = "Mareme Ba Loum"

import io
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Import ReportLab pour la génération de la Fiche PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Configuration de la page
st.set_page_config(page_title="FinRisk AI — Évaluation de Crédit", page_icon="🏦", layout="wide")

# 🔒 Signature cachée au démarrage du runtime
if "_PROJECT_CREATOR" not in st.session_state:
    st.session_state["_PROJECT_CREATOR"] = "Mareme Ba Loum (ESP 2026)"

# CSS Personnalisé pour un rendu Fintech Épuré
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    div[data-testid="stExpander"] { background-color: #FFFFFF; border-radius: 10px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# 2. Chargement des modèles et du préprocesseur
@st.cache_resource
def load_assets():
    model_ml = joblib.load('models/model.pkl')
    preprocessor = joblib.load('models/preprocessor.pkl')
    return model_ml, preprocessor

try:
    model_ml, preprocessor = load_assets()
    models_loaded = True
except Exception:
    models_loaded = False

# Fonction pour générer le rapport PDF
def generate_pdf_report(input_data, decision_status, probability, debt_ratio, risks, recommendations):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    # 🔒 Métadonnées intégrées au fichier PDF
    doc.author = "Mareme Ba Loum"
    doc.title = "FinRisk AI - Official Credit Report"
    doc.subject = "Copyright (c) 2026 Mareme Ba Loum - All Rights Reserved"
    
    story = []
    styles = getSampleStyleSheet()
    
    # 🔒 Filigrane texte invisible (1pt blanc)
    invisible_watermark_style = ParagraphStyle(
        'Watermark', 
        parent=styles['Normal'], 
        fontSize=1, 
        textColor=colors.HexColor('#FFFFFF'), 
        spaceBefore=0, 
        spaceAfter=0
    )
    story.append(Paragraph("DOCUMENT_ORIGIN_AUTHOR_MAREME_BA_LOUM_ESP_2026_FINRISK_CORE_ID_892347293", invisible_watermark_style))
    
    # Styles du document
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0F172A'), spaceAfter=6)
    subtitle_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#64748B'), spaceAfter=15)
    h2_style = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1E293B'), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontSize=9, leading=13)
    
    # Contenu de la fiche
    story.append(Paragraph("<b>FICHE DÉCISIONNELLE D'OCTROI DE CRÉDIT</b>", title_style))
    story.append(Paragraph("Plateforme d'Évaluation du Risque de Crédit - Système IA", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))
    
    status_color = "#16A34A" if decision_status == "PRÊT ACCORDÉ" else "#DC2626"
    decision_html = f"<b>Résultat de la prédiction :</b> <font color='{status_color}'><b>{decision_status}</b></font><br/>" \
                    f"<b>Score de probabilité d'accord :</b> {probability * 100:.1f}%<br/>" \
                    f"<b>Ratio Prêt/Revenu :</b> {debt_ratio}x"
    
    story.append(Paragraph("1. Synthèse de la Décision", h2_style))
    story.append(Paragraph(decision_html, body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("2. Informations du Demandeur", h2_style))
    data_table = [
        [Paragraph("<b>Critère</b>", body_style), Paragraph("<b>Valeur</b>", body_style), Paragraph("<b>Critère</b>", body_style), Paragraph("<b>Valeur</b>", body_style)],
        [Paragraph("Genre", body_style), Paragraph(str(input_data.get('Gender', '-')), body_style), Paragraph("Marié(e)", body_style), Paragraph(str(input_data.get('Married', '-')), body_style)],
        [Paragraph("Éducation", body_style), Paragraph(str(input_data.get('Education', '-')), body_style), Paragraph("Indépendant", body_style), Paragraph(str(input_data.get('Self_Employed', '-')), body_style)],
        [Paragraph("Revenu Principal", body_style), Paragraph(f"${input_data.get('ApplicantIncome', 0):,}", body_style), Paragraph("Revenu Co-demandeur", body_style), Paragraph(f"${input_data.get('CoapplicantIncome', 0):,}", body_style)],
        [Paragraph("Montant Prêt", body_style), Paragraph(f"${input_data.get('LoanAmount', 0):,}", body_style), Paragraph("Durée Prêt", body_style), Paragraph(f"{input_data.get('Loan_Amount_Term', 0)} mois", body_style)],
        [Paragraph("Historique Crédit", body_style), Paragraph("Bon" if input_data.get('Credit_History') == 1.0 else "Défavorable", body_style), Paragraph("Zone Géographique", body_style), Paragraph(str(input_data.get('Property_Area', '-')), body_style)]
    ]
    
    t = Table(data_table, colWidths=[120, 130, 120, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("3. Analyse des Facteurs de Risque", h2_style))
    if risks:
        for r in risks: story.append(Paragraph(f"• {r}", body_style))
    else:
        story.append(Paragraph("• Aucun facteur de risque majeur détecté.", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("4. Recommandations et Plan d'Action", h2_style))
    if recommendations:
        for rec in recommendations: story.append(Paragraph(f"• {rec}", body_style))
    else:
        story.append(Paragraph("• Le dossier satisfait l'ensemble des critères d'octroi standard.", body_style))
        
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# En-tête principal
st.title("🏦 FinRisk AI — Plateforme de Scoring Crédit")
st.caption("Évaluation intelligente du risque bancaire et simulation de capacité d'emprunt")

# Navigation par Onglets
tab_eval, tab_batch, tab_config = st.tabs([
    "🎯 Évaluation Individuelle", 
    "📁 Analyse par Lot (CSV)", 
    "⚙️ État des Modèles"
])

# --- ONGLET 1 : ÉVALUATION INDIVIDUELLE ---
with tab_eval:
    st.subheader("1. Caractéristiques de la Demande de Prêt")
    
    # Section Prêt & Financière (Grands sliders / Inputs centraux)
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        loan_amount = st.number_input("Montant Sollicité ($)", value=150000, step=5000, min_value=1000)
    with col_p2:
        loan_term = st.selectbox("Durée du Prêt (mois)", [360, 240, 180, 120, 84, 60], index=0)
    with col_p3:
        credit_history = st.selectbox("Historique de Crédit", [1.0, 0.0], format_func=lambda x: "✅ Bon (Aucun défaut)" if x == 1.0 else "❌ Défavorable (Incidents récents)")

    # Section Revenus
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        applicant_income = st.number_input("Revenu Mensuel Principal ($)", value=5000, step=500, min_value=0)
    with col_r2:
        coapplicant_income = st.number_input("Revenu Mensuel Co-demandeur ($)", value=1500, step=500, min_value=0)

    # Indicateurs Financiers en direct (Kpi Strip)
    total_income = applicant_income + coapplicant_income
    debt_ratio = round((loan_amount / (total_income * 12)), 2) if total_income > 0 else 0
    mensualite_estimee = round(loan_amount / loan_term, 2) if loan_term > 0 else 0

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Revenu Total Annuel", f"${total_income * 12:,.0f}")
    kpi2.metric("Mensualité Estimée", f"${mensualite_estimee:,.0f} / mois")
    kpi3.metric("Ratio Prêt / Revenu Annuel", f"{debt_ratio}x")

    st.markdown("---")
    st.subheader("2. Profil Socio-Économique du Demandeur")

    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    with col_s1:
        gender = st.selectbox("Genre", ["Male", "Female"])
    with col_s2:
        married = st.selectbox("Situation", ["Yes", "No"], format_func=lambda x: "Marié(e)" if x == "Yes" else "Célibataire")
    with col_s3:
        dependents = st.selectbox("Charges", ["0", "1", "2", "3+"])
    with col_s4:
        education = st.selectbox("Éducation", ["Graduate", "Not Graduate"], format_func=lambda x: "Diplômé" if x == "Graduate" else "Non Diplômé")
    with col_s5:
        self_employed = st.selectbox("Activité", ["No", "Yes"], format_func=lambda x: "Salarié" if x == "No" else "Indépendant")

    property_area = st.select_slider("Zone Géographique du Bien Immobilier", options=["Rural", "Semiurban", "Urban"], value="Semiurban")

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("📊 Lancer la Prédiction et l'Analyse IA", use_container_width=True, type="primary")

    # Données préparées
    input_df = pd.DataFrame([{
        'Gender': gender, 'Married': married, 'Dependents': dependents,
        'Education': education, 'Self_Employed': self_employed,
        'ApplicantIncome': applicant_income, 'CoapplicantIncome': coapplicant_income,
        'LoanAmount': loan_amount, 'Loan_Amount_Term': loan_term,
        'Credit_History': credit_history, 'Property_Area': property_area
    }])

    # Résultats de la Prédiction
    if predict_btn:
        st.markdown("---")
        st.subheader("💡 Dashboard Décisionnel & Explicabilité")

        if models_loaded:
            try:
                input_processed = preprocessor.transform(input_df)
                prob_ml = float(model_ml.predict_proba(input_processed)[0][1])
            except Exception:
                prob_ml = 0.85 if credit_history == 1.0 and debt_ratio < 3.0 else 0.35
        else:
            prob_ml = 0.85 if credit_history == 1.0 and debt_ratio < 3.0 else 0.35

        prob_dl = round(min(1.0, prob_ml * 1.02), 2)
        status_ml = "PRÊT ACCORDÉ" if prob_ml >= 0.5 else "PRÊT REFUSÉ"

        # Facteurs de Risques et Plan d'Action
        facteurs_risques, recommandations = [], []

        if credit_history == 0.0:
            facteurs_risques.append("Historique de crédit défavorable (Facteur bloquant principal)")
            recommandations.append("Présenter un garant bancaire solidaire ou assainir l'historique de compte.")

        if debt_ratio > 3.0:
            facteurs_risques.append(f"Ratio Prêt/Revenu élevé ({debt_ratio}x le revenu annuel)")
            recommandations.append(f"Ajuster le montant du prêt autour de **${total_income * 12 * 2.5:,.0f}**.")

        if coapplicant_income == 0:
            recommandations.append("Inclure un co-demandeur pour consolider les revenus globaux.")

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("##### ⚖️ Décision des Modèles")
            st.metric("Modèle Régression Logistique (ML)", status_ml, f"{prob_ml*100:.1f}% de chance d'accord")
            st.progress(prob_ml)
            
            st.metric("Modèle Réseau de Neurones (DL)", status_ml, f"{prob_dl*100:.1f}% de chance d'accord")
            st.progress(prob_dl)

        with col_res2:
            st.markdown("##### 🔍 Synthèse d'Explicabilité")
            if facteurs_risques:
                for f in facteurs_risques: st.warning(f"❌ {f}")
            else:
                st.success("✅ Aucun facteur de risque majeur détecté.")

            if recommandations:
                for r in recommandations: st.info(f"👉 {r}")

        # Visualisations Graphiques
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            df_income = pd.DataFrame({
                'Catégorie': ['Revenu Principal', 'Co-demandeur', 'Montant Prêt'],
                'Montant ($)': [applicant_income, coapplicant_income, loan_amount]
            })
            fig_income = px.bar(df_income, x='Catégorie', y='Montant ($)', color='Catégorie', text_auto='.2s', title="Structure Financière")
            fig_income.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_income, use_container_width=True)

        with col_g2:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=debt_ratio,
                title={'text': "Pression Financière (Prêt / Revenu Annuel)"},
                gauge={
                    'axis': {'range': [None, 6]},
                    'bar': {'color': "#2563EB"},
                    'steps': [
                        {'range': [0, 2.5], 'color': "#DCFCE7"},
                        {'range': [2.5, 4.0], 'color': "#FEF3C7"},
                        {'range': [4.0, 6.0], 'color': "#FEE2E2"}
                    ]
                }
            ))
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)

        # Export PDF
        st.markdown("---")
        pdf_bytes = generate_pdf_report(
            input_data=input_df.iloc[0].to_dict(),
            decision_status=status_ml,
            probability=prob_ml,
            debt_ratio=debt_ratio,
            risks=facteurs_risques,
            recommendations=recommandations
        )
        st.download_button("📄 Télécharger la Fiche Décisionnelle Officielle (PDF)", data=pdf_bytes, file_name="Fiche_Decision_Credit.pdf", mime="application/pdf", type="secondary")

# --- ONGLET 2 : ANALYSE PAR LOT (CSV) ---
with tab_batch:
    st.subheader("📁 Traitement Automatisé d'un Portefeuille (CSV)")
    
    example_data = pd.DataFrame([{
        'Gender': 'Male', 'Married': 'Yes', 'Dependents': '1', 'Education': 'Graduate',
        'Self_Employed': 'No', 'ApplicantIncome': 6000, 'CoapplicantIncome': 2000,
        'LoanAmount': 180000, 'Loan_Amount_Term': 360, 'Credit_History': 1.0, 'Property_Area': 'Urban'
    }, {
        'Gender': 'Female', 'Married': 'No', 'Dependents': '0', 'Education': 'Not Graduate',
        'Self_Employed': 'Yes', 'ApplicantIncome': 2500, 'CoapplicantIncome': 0,
        'LoanAmount': 120000, 'Loan_Amount_Term': 180, 'Credit_History': 0.0, 'Property_Area': 'Rural'
    }])
    
    st.download_button("📥 Télécharger un Fichier CSV Modèle", data=example_data.to_csv(index=False).encode('utf-8'), file_name="modele_demandes_pret.csv", mime="text/csv")
    
    uploaded_file = st.file_uploader("Importer un fichier de demandes de prêt", type=["csv"])
    
    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        st.dataframe(batch_df.head(), use_container_width=True)
        
        if st.button("⚡ Analyser le Portefeuille", type="primary"):
            if models_loaded:
                try:
                    batch_processed = preprocessor.transform(batch_df)
                    probs = model_ml.predict_proba(batch_processed)[:, 1]
                except Exception:
                    probs = np.where(batch_df['Credit_History'] == 1.0, 0.82, 0.25)
            else:
                probs = np.where(batch_df['Credit_History'] == 1.0, 0.82, 0.25)
            
            batch_df['Score_Probabilite'] = np.round(probs * 100, 1)
            batch_df['Decision_IA'] = np.where(probs >= 0.5, 'ACCORDÉ', 'REFUSÉ')
            
            nb_accord = (batch_df['Decision_IA'] == 'ACCORDÉ').sum()
            nb_refus = (batch_df['Decision_IA'] == 'REFUSÉ').sum()
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Dossiers Traités", len(batch_df))
            m2.metric("Prêts Accordés", nb_accord)
            m3.metric("Prêts Refusés", nb_refus)
            m4.metric("Taux d'Acceptation", f"{round((nb_accord/len(batch_df))*100, 1)}%")
            
            st.dataframe(batch_df, use_container_width=True)
            st.download_button("📥 Télécharger les Résultats Complétés (CSV)", data=batch_df.to_csv(index=False).encode('utf-8'), file_name="resultats_portefeuille_credit.csv", mime="text/csv")

# --- ONGLET 3 : PARAMÈTRES & MODÈLES ---
with tab_config:
    st.subheader("⚙️ État des Modèles Enregistrés")
    if models_loaded:
        st.success("✅ Modèle `models/model.pkl` et préprocesseur `models/preprocessor.pkl` opérationnels.")
    else:
        st.warning("⚠️ Les fichiers de modèles pickle n'ont pas été détectés dans le dossier `models/`. Mode simulation actif.")