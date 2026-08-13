# 🏦 Prédiction d'Éligibilité à un Prêt Bancaire (ML & Deep Learning)

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Framework](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![ML](https://img.shields.io/badge/Scikit--Learn-Latest-orange.svg)
![DL](https://img.shields.io/badge/Keras%2FTensorFlow-Latest-green.svg)

Une solution de Machine Learning et Deep Learning déployée sous forme d'application web interactive, permettant aux institutions financières d'évaluer automatiquement l'éligibilité d'un client à un prêt bancaire.

---

## 🎯 Objectif du Projet

L'évaluation manuelle des demandes de prêt est souvent lente et sujette à des erreurs ou biais. L'objectif de ce projet est de proposer une approche **data-driven** pour :
* **Automatiser le filtrage initial** des dossiers de crédit.
* **Estimer le risque financier** sur la base du profil et de l'historique du client.
* **Offrir une interface intuitive** exploitable par des agents bancaires.

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
  * `Income_to_Loan_Ratio` = Ratio capacité de remboursement / prêt
* **Encodage & Normalisation :**
  * Transformation logarithmique (`np.log1p`) sur les revenus pour lisser l'asymétrie.
  * One-Hot Encoding (`pd.get_dummies`) des variables catégorielles.
  * Standardisation des données via `StandardScaler`.

### 2. Modélisation & Performance (`train.ipynb` & `deep_learning.ipynb`)
Mise en compétition de deux approches :
* **Régression Logistique (Machine Learning) :**
  * **Avantages :** Modèle hautement explicable, rapide à entraîner et conforme aux contraintes d'audit bancaire.
* **Réseau de Neurones Dense / Keras (Deep Learning) :**
  * **Architecture :** Multi-Layer Perceptron avec couches `Dense` et régularisation `Dropout` pour limiter le surapprentissage (*overfitting*).

---

## 🚀 Déploiement & Démo

L'application est déployée en ligne grâce à Streamlit Community Cloud.

* 🔗 **Lien de la Démo Interactive :** [https://votrenom-eligibilite-pret.streamlit.app](https://votre-demo-streamlit.streamlit.app)

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
│   └── app.py                # Interface utilisateur Streamlit
├── requirements.txt          # Dépendances Python
└── README.md                 # Documentation du projet