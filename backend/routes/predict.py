from fastapi import APIRouter
import pandas as pd
import pickle
import numpy as np
import shap
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

# ── Model Load ────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "data", "model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

explainer = shap.TreeExplainer(model)

# ── Feature list ──────────────────────────────────────
FEATURES = [
    "project_size", "complexity_score", "essential_complexity",
    "design_complexity", "code_volume", "halstead_volume",
    "program_length", "difficulty_score", "intelligence_score",
    "effort_score", "error_estimate", "time_estimate",
    "code_lines", "comment_lines", "blank_lines",
    "code_comment_lines", "unique_operators", "unique_operands",
    "total_operators", "total_operands", "branch_count"
]

# ── Groq Client ───────────────────────────────────────
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@router.post("/predict")
def predict(data: dict):
    try:
        # ── Input → DataFrame ─────────────────────────
        input_df = pd.DataFrame([data])
        input_df = input_df[FEATURES]

        # ── Predict ───────────────────────────────────
        prob = model.predict_proba(input_df)[0][1]
        risk_score = round(prob * 100, 2)

        if risk_score >= 70:
            risk_level = "High"
        elif risk_score >= 40:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # ── SHAP top factors ──────────────────────────
        shap_values = explainer.shap_values(input_df)
        sv = shap_values[1] if isinstance(shap_values, list) else shap_values
        shap_series = pd.Series(
            np.abs(sv[0]),
            index=FEATURES
        ).sort_values(ascending=False)
        top_factors = shap_series.head(5).index.tolist()

        # ── Groq AI explanation ───────────────────────
        prompt = f"""You are a software project risk analyst.

Risk Score: {risk_score}%
Risk Level: {risk_level}
Top Risk Factors: {', '.join(top_factors)}

Give a 3-sentence explanation of this risk and 2 actionable recommendations.
Keep it professional and concise."""

        message = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        explanation = message.choices[0].message.content

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "top_risk_factors": top_factors,
            "defect_probability": f"{risk_score}%",
            "ai_explanation": explanation
        }

    except Exception as e:
        return {"error": str(e)}