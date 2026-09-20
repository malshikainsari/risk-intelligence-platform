import pandas as pd
import lightgbm as lgb
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
import pickle

# ── 1. Load Data ─────────────────────────────────────
X_train = pd.read_csv("../data/X_train.csv")
X_test  = pd.read_csv("../data/X_test.csv")
y_train = pd.read_csv("../data/y_train.csv").squeeze()
y_test  = pd.read_csv("../data/y_test.csv").squeeze()

# ── 2. SMOTE (class imbalance fix) ───────────────────
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)

print(f"Before SMOTE: {y_train.value_counts().to_dict()}")
print(f"After SMOTE:  {y_train_bal.value_counts().to_dict()}")

# ── 3. Model ──────────────────────────────────────────
model = lgb.LGBMClassifier(
    n_estimators=300,
    learning_rate=0.03,
    max_depth=8,
    num_leaves=31,
    min_child_samples=20,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# ── 4. Train ─────────────────────────────────────────
model.fit(
    X_train_bal, y_train_bal,
    eval_set=[(X_test, y_test)],
    callbacks=[lgb.early_stopping(50), lgb.log_evaluation(50)]
)

# ── 5. Evaluate ──────────────────────────────────────
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))
print(f"🎯 ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")

# ── 6. Save Model ────────────────────────────────────
with open("../data/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model saved!")