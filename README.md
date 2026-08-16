# 🏦 Prédiction d'Éligibilité à un Prêt Bancaire (ML & Deep Learning)

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Latest-orange.svg)
![TensorFlow](https://img.shields.io/badge/Keras%2FTensorFlow-Latest-green.svg)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Generation-blue.svg)

Une solution de Machine Learning et Deep Learning déployée sous forme d'application web interactive, permettant aux institutions financières d'évaluer automatiquement l'éligibilité d'un client à un prêt bancaire et d'exporter des fiches décisionnelles synthétiques.

---

## 🎯 Objectif du Projet

L'évaluation manuelle des demandes de prêt est souvent lente et sujette à des erreurs ou biais. L'objectif de ce projet est de proposer une approche **data-driven** pour :
* **Automatiser le filtrage initial** des dossiers de crédit individuels et par lots (batch CSV).
* **Estimer le risque financier** sur la base du profil, du ratio d'endettement et de l'historique de crédit du client.
* **Proposer un plan d'optimisation personnalisé** pour retravailler les dossiers refusés.
* **Générer automatiquement une Fiche Décisionnelle officielle au format PDF**.
* **Offrir une interface intuitive et moderne** conforme aux standards UX de la Fintech.

Ce projet a été réalisé dans le cadre du projet de fin de certificat en **Intelligence Artificielle & Données (FORCE-N)**.

---

## 📊 Jeu de Données & Features

Le jeu de données contient des informations socio-économiques et financières des demandeurs de prêt :

| Variable | Description | Type |
| :--- | :--- | :--- |
| `Gender`, `Married`, `Education` | Informations démographiques | Catégorielle |
| `ApplicantIncome`, `CoapplicantIncome` | Revenus du demandeur et co-demandeur | Numérique |
| `LoanAmount`, `Loan_Amount_Term` | Montant et durée du crédit | Numérique |
| `Credit_History` | Historique de crédit (0 = Mauvais, 1 = Bon) | Numérique (Binaire) |
| `Property_Area` | Localisation du bien (Urban, Semiurban, Rural) | Catégorielle |
| **`Loan_Status` (Cible)** | **Accord du prêt (Y = Oui, N = Non)** | **Target** |

---

## 🛠️ Pipeline Technique & Méthodologie

### 1. Analyse Exploratoire & Prétraitement (`preprocessing.ipynb`)
* **Gestion des données manquantes :** Imputation par la médiane pour les variables numériques et par le mode pour les variables catégorielles.
* **Feature Engineering :**
  * `Total_Income` = `ApplicantIncome` + `CoapplicantIncome`
  * `Debt_Ratio` = Ratio Montant du prêt / Revenus totaux
* **Encodage & Normalisation :**
  * Transformation logarithmique (`np.log1p`) sur les revenus pour lisser l'asymétrie.
  * One-Hot Encoding des variables catégorielles.
  * Standardisation des données via `StandardScaler` (sauvegardé dans `preprocessor.pkl`).

### 2. Modélisation & Performance (`train.ipynb` & `deep_learning.ipynb`)
Mise en compétition de deux approches :
* **Régression Logistique (Machine Learning) :**
  * **Avantages :** Modèle hautement explicable, rapide et conforme aux contraintes d'audit bancaire.
* **Réseau de Neurones Dense / Keras (Deep Learning) :**
  * **Architecture :** Multi-Layer Perceptron avec couches `Dense` et régularisation `Dropout` pour évaluer le risque non linéaire.

---

## ✨ Fonctionnalités Clés de l'Application Web

1. **🎯 Évaluation Individuelle & Explicabilité :**
   * Saisie guidée des données du demandeur.
   * Calcul en temps réel du ratio Prêt/Revenu et estimation des mensualités.
   * Détection automatique des facteurs de risque et recommandations financières sur mesure.
2. **⚖️ Comparaison Multi-Modèles (ML vs DL) :**
   * Comparaison en direct des prédictions de la Régression Logistique et du Réseau de Neurones Keras.
3. **📄 Génération & Export PDF (ReportLab) :**
   * Exportation instantanée d'un rapport décisionnel structuré comprenant le profil du client, la décision d'octroi, le score de probabilité et les préconisations.
4. **📁 Évaluation par Lot (Batch CSV) :**
   * Traitement automatisé de fichiers CSV contenant plusieurs demandes de prêt avec affichage des métriques globales du portefeuille et export des résultats complets.
5. **📊 Graphiques Interactifs (Plotly) :**
   * Visualisation de la structure financière (revenus vs prêt) et jauge de pression financière / endettement.

---

## 🚀 Déploiement & Démo

L'application est déployée en ligne grâce à Streamlit Community Cloud.

* 🔗 **Lien de la Démo Interactive :** [https://portfoliomareme.vercel.app/](https://portfoliomareme.vercel.app/)

---

## 📁 Structure du Projet

```text
eligibilte_pret_projet_ml/
├── data/
│   ├── raw/                  # Données brutes (train_loan.csv)
│   └── processed/            # Données nettoyées (cleaned_loan.csv, transformed_loan.csv)
├── models/
│   ├── model.pkl             # Modèle de Régression Logistique sauvegardé
│   ├── preprocessor.pkl      # Pipeline de prétraitement (scaler, encoders)
│   └── dl_model.keras        # Modèle Deep Learning Keras
├── notebooks/
│   ├── preprocessing.ipynb   # Nettoyage et Feature Engineering
│   ├── train.ipynb           # Entraînement ML classique
│   └── deep_learning.ipynb   # Entraînement du réseau de neurones Keras
├── src/
│   └── app.py                # Interface utilisateur Streamlit (Dashboard Fintech & PDF Export)
├── requirements.txt          # Dépendances Python (streamlit, plotly, reportlab, joblib...)
└── README.md                 # Documentation du projet
