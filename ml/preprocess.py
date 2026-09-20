import pandas as pd
from sklearn.model_selection import train_test_split

# ── 1. Load ──────────────────────────────────────────
df = pd.read_csv("../data/NASA-promise-dataset-repository-main/kc1.csv")

# ── 2. Clean ─────────────────────────────────────────
df = df.dropna()
df = df.drop_duplicates()

# ── 3. Feature Mapping ────────────────────────────────
feature_map = {
    'loc'              : 'project_size',
    'v(g)'             : 'complexity_score',
    'ev(g)'            : 'essential_complexity',
    'iv(g)'            : 'design_complexity',
    'n'                : 'code_volume',
    'v'                : 'halstead_volume',
    'l'                : 'program_length',
    'd'                : 'difficulty_score',
    'i'                : 'intelligence_score',
    'e'                : 'effort_score',
    'b'                : 'error_estimate',
    't'                : 'time_estimate',
    'lOCode'           : 'code_lines',
    'lOComment'        : 'comment_lines',
    'lOBlank'          : 'blank_lines',
    'locCodeAndComment' : 'code_comment_lines',
    'uniq_Op'          : 'unique_operators',
    'uniq_Opnd'        : 'unique_operands',
    'total_Op'         : 'total_operators',
    'total_Opnd'       : 'total_operands',
    'branchCount'      : 'branch_count',
    'defects'          : 'has_defect'
}

df = df.rename(columns=feature_map)

# ── 4. Target Variable ────────────────────────────────
df['has_defect'] = df['has_defect'].astype(int)

# ── 5. Features + Target ─────────────────────────────
X = df.drop('has_defect', axis=1)
y = df['has_defect']

# ── 6. Train/Test Split ───────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ── 7. Save ───────────────────────────────────────────
X_train.to_csv("../data/X_train.csv", index=False)
X_test.to_csv("../data/X_test.csv", index=False)
y_train.to_csv("../data/y_train.csv", index=False)
y_test.to_csv("../data/y_test.csv", index=False)

print("✅ Preprocessing complete!")
print(f"Train size: {X_train.shape[0]}")
print(f"Test size:  {X_test.shape[0]}")
print(f"Features:   {X_train.shape[1]}")