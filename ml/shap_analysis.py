import pandas as pd
import lightgbm as lgb
import shap
import pickle
import matplotlib.pyplot as plt

# ── 1. Load model + data ─────────────────────────────
with open("../data/model.pkl", "rb") as f:
    model = pickle.load(f)

X_test = pd.read_csv("../data/X_test.csv")

# ── 2. SHAP explainer ─────────────────────────────────
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# ── 3. Feature importance (text output) ──────────────
import numpy as np
mean_abs_shap = np.abs(shap_values[1] if isinstance(shap_values, list) else shap_values).mean(axis=0)

importance_df = pd.DataFrame({
    'feature': X_test.columns,
    'importance': mean_abs_shap
}).sort_values('importance', ascending=False)

print("📊 Top 10 Most Important Features:\n")
print(importance_df.head(10).to_string(index=False))

# ── 4. Save plot ──────────────────────────────────────
shap.summary_plot(shap_values, X_test, show=False)
plt.tight_layout()
plt.savefig("../data/shap_summary.png")
print("\n✅ SHAP plot saved to data/shap_summary.png")