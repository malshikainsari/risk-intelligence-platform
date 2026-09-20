from fastapi import APIRouter
from pydantic import BaseModel
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

FEATURES = [
    "project_size", "complexity_score", "essential_complexity",
    "design_complexity", "code_volume", "halstead_volume",
    "program_length", "difficulty_score", "intelligence_score",
    "effort_score", "error_estimate", "time_estimate",
    "code_lines", "comment_lines", "blank_lines",
    "code_comment_lines", "unique_operators", "unique_operands",
    "total_operators", "total_operands", "branch_count"
]

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── User-Friendly Input Model ─────────────────────────
class ProjectInput(BaseModel):
    team_size: int
    duration_months: int
    complexity: str        # "Low", "Medium", "High"
    budget: float
    requirement_changes: str  # "Rare", "Sometimes", "Frequent"
    developer_experience: str  # "Junior", "Mid", "Senior"

# ── Mapping Function ──────────────────────────────────
def map_to_kc1(p: ProjectInput) -> dict:
    complexity_map = {"Low": 2, "Medium": 5, "High": 9}
    changes_map    = {"Rare": 1, "Sometimes": 3, "Frequent": 6}
    exp_map        = {"Junior": 8, "Mid": 5, "Senior": 2}

    c  = complexity_map[p.complexity]
    ch = changes_map[p.requirement_changes]
    ex = exp_map[p.developer_experience]

    loc         = p.team_size * p.duration_months * 200
    effort      = loc * c * 0.5
    volume      = loc * 4.5
    difficulty  = (c * ch * ex) / 2
    time_est    = effort / (p.team_size * 160)
    error_est   = round(volume / 3000, 2)

    return {
        "project_size"       : loc,
        "complexity_score"   : c,
        "essential_complexity": max(1, c - 2),
        "design_complexity"  : max(1, c - 1),
        "code_volume"        : loc * 2,
        "halstead_volume"    : volume,
        "program_length"     : round(loc / 5000, 3),
        "difficulty_score"   : difficulty,
        "intelligence_score" : round(volume / difficulty, 2) if difficulty else 10,
        "effort_score"       : effort,
        "error_estimate"     : error_est,
        "time_estimate"      : round(time_est, 2),
        "code_lines"         : int(loc * 0.75),
        "comment_lines"      : int(loc * 0.10),
        "blank_lines"        : int(loc * 0.08),
        "code_comment_lines" : int(loc * 0.07),
        "unique_operators"   : int(15 + c * 3),
        "unique_operands"    : int(30 + p.team_size * 4 + ch * 5),
        "total_operators"    : int(loc * 1.2),
        "total_operands"     : int(loc * 1.1),
        "branch_count"       : int(c * ch * p.team_size * 1.5),
    }

@router.post("/predict")
def predict(data: ProjectInput):
    try:
        # ── Map to KC1 features ───────────────────────
        mapped = map_to_kc1(data)
        input_df = pd.DataFrame([mapped])[FEATURES]

        # ── Predict ───────────────────────────────────
        prob = model.predict_proba(input_df)[0][1]
        risk_score = round(prob * 100, 2)

        if risk_score >= 70:
            risk_level = "High"
        elif risk_score >= 40:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # ── SHAP ──────────────────────────────────────
        shap_values = explainer.shap_values(input_df)
        sv = shap_values[1] if isinstance(shap_values, list) else shap_values
        shap_series = pd.Series(
            np.abs(sv[0]), index=FEATURES
        ).sort_values(ascending=False)
        top_factors = shap_series.head(5).index.tolist()

        # ── Groq AI ───────────────────────────────────
        prompt = f"""You are a software project risk analyst.

Project Details:
- Team Size: {data.team_size} developers
- Duration: {data.duration_months} months
- Complexity: {data.complexity}
- Budget: ${data.budget:,.0f}
- Requirement Changes: {data.requirement_changes}
- Developer Experience: {data.developer_experience}

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
            "risk_score"       : risk_score,
            "risk_level"       : risk_level,
            "top_risk_factors" : top_factors,
            "defect_probability": f"{risk_score}%",
            "ai_explanation"   : explanation,
            "mapped_metrics"   : mapped,
        }

    except Exception as e:
        return {"error": str(e)}