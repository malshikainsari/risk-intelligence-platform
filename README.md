# 🔍 RiskIQ — AI Software Project Risk Intelligence Platform

> Predict software project failure risk using Machine Learning + AI-powered explanations.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)
![LightGBM](https://img.shields.io/badge/LightGBM-ML_Model-orange?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-AI_Explanation-purple?style=flat-square)

---

## 🎯 Overview

**RiskIQ** is an AI-powered platform that predicts the risk of software project failure based on project parameters such as team size, complexity, duration, and developer experience.

The system combines:
- **LightGBM** — trained on NASA KC1 software defect dataset
- **SHAP** — for explainable AI (feature importance)
- **Groq LLM** — for human-readable risk explanations and recommendations

---

## 🖥️ Demo

| Input | Output |
|-------|--------|
| Team size, duration, complexity, budget | Risk score (%), risk level, top factors, AI explanation |

---

## 🏗️ Architecture

```
User Input (Next.js)
       ↓
FastAPI Backend
       ↓
Feature Mapping Layer (User inputs → KC1 metrics)
       ↓
LightGBM Model → Risk Score + SHAP Top Factors
       ↓
Groq LLM → AI Explanation + Recommendations
       ↓
Dashboard (Next.js)
```

---

## 🧠 ML Pipeline

| Step | Detail |
|------|--------|
| Dataset | NASA PROMISE KC1 (1,212 samples, 21 features) |
| Preprocessing | Feature mapping, null removal, deduplication |
| Class Balancing | SMOTE (717 → balanced classes) |
| Model | LightGBM Classifier |
| Explainability | SHAP TreeExplainer |
| ROC-AUC | 0.62 (consistent with published KC1 benchmarks) |

> **Note:** KC1 is a module-level software defect dataset used as a proxy for project risk modeling. Project-level inputs are mapped to KC1 features via a statistical mapping layer.

---

## 🛠️ Tech Stack

**Backend**
- Python 3.11
- FastAPI + Uvicorn
- LightGBM, SHAP, scikit-learn, imbalanced-learn
- Groq API (LLaMA)

**Frontend**
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/malshikainsari/risk-intelligence-platform.git
cd risk-intelligence-platform
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file in `backend/`:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Train the Model
```bash
cd ml
python preprocess.py
python train.py
```

Copy model to backend:
```bash
copy data\model.pkl backend\data\model.pkl
```

### 4. Run Backend
```bash
cd backend
python -m uvicorn app:app --reload
```
API available at: `http://localhost:8000/docs`

### 5. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
App available at: `http://localhost:3000`

---

## 📁 Project Structure

```
risk-intelligence-platform/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── data/
│   │   └── model.pkl
│   └── routes/
│       └── predict.py
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   └── globals.css
│   └── package.json
├── ml/
│   ├── preprocess.py
│   ├── train.py
│   └── shap_analysis.py
└── data/
    └── NASA-promise-dataset-repository-main/
```

---


