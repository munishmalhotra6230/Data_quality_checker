import pandas as pd 
import numpy as np
from sklearn.preprocessing import LabelEncoder
class Phase4_Target_Analysis:
    def __init__(self, data, target, problem_type="classification"):
        self.data = data
        self.target = data[target]
        self.problem_type = problem_type
        self.target_col = data[target]
        self.features = data.drop(columns=target)
        self.class_imbalance = {}
        self.target_distribution = {}
        self.feature_target_corr = {}

    def analyze(self):
        if self.problem_type == "classification":
            # Check 1 - Class Imbalance
            valuex = self.target_col.value_counts(normalize=True)
            # expose distribution and imbalance metrics expected by dashboard
            self.class_distribution = valuex.to_dict()
            imbalance = valuex.values
            if valuex.nunique() == 1:
                self.majority_minority = 1
            majority = max(imbalance)
            minority = min(imbalance)
            self.majority_minority = round(minority / majority, 2)  # similarity score
            self.imbalance_ratio = self.majority_minority
            print("Class imbalance extracted")
        elif self.problem_type == "regression":
            # Check 2 - Target Distribution
            self.target_skewness = round(self.target_col.skew(), 4)
            self.target_mean = round(self.target_col.mean(), 4)
            self.target_std = round(self.target_col.std(), 4)
            print("Target distribution extracted")

        # Check 3 - Feature Target Correlation
        numeric_features = self.features.select_dtypes(include=[np.number])
        # For classification, encode target labels to numeric but keep as a pandas Series
        if self.problem_type == "classification":
            encoded = LabelEncoder().fit_transform(self.target_col)
            self.target_col = pd.Series(encoded, index=self.target_col.index, name=self.target_col.name)
        # For regression, assume target_col is already numeric (do not encode)
        for col in numeric_features.columns:
            # both operands are pandas Series so .corr() is available
            corr = abs(self.target_col.corr(self.features[col]))
            self.feature_target_corr[col] = round(corr, 4)
        print("Feature target correlation extracted")

    def scoring_phase4(self):
        score = 100
        issues = {}

        if self.problem_type == "classification":
            # Class Imbalance Scoring
            if self.majority_minority >=0.8:
                issues['class_imbalance'] = "perfect"
            elif self.majority_minority >=0.5 :
                score -= 5
                issues['class_imbalance'] = "Slight_imbalace"
            elif self.majority_minority >=0.3 :
                score -= 15
                issues['class_imbalance'] = "Moderate_imbalace"
            elif self.majority_minority>=0.1:
                issues['class_imbalance'] = "Highly_imbalace"
            elif self.majority_minority<0.1:
                issues['class_imbalance']='Strictly_imbalance'
            else:
                None

        elif self.problem_type == "regression":
            # Target Skewness Scoring
            if abs(self.target_skewness) > 1:
                score -= 20
                issues['target_skewness'] = "critical"
            elif abs(self.target_skewness) > 0.5:
                score -= 10
                issues['target_skewness'] = "moderate"
            else:
                issues['target_skewness'] = "No_skewness"

        # Feature Target Correlation Scoring
        useful_features = [
            col for col, val in self.feature_target_corr.items()
            if val > 0.1
        ]
        useless_features = [
            col for col, val in self.feature_target_corr.items()
            if val <= 0.1
        ]

        if len(useful_features) == 0:
            score -= 30
            issues['feature_correlation'] = "critical_no_useful_features"
        elif len(useless_features) > len(useful_features):
            score -= 15
            issues['feature_correlation'] = "moderate_many_useless_features"
        else:
            issues['feature_correlation'] = "good"

        self.phase4_score = max(0, score)
        self.phase4_issues = issues
        return self.phase4_score, self.phase4_issues
if __name__=='__main__':
    from sklearn.datasets import load_iris
    print("=== Test 1: Classification Balanced ===")
    x, y = load_iris(return_X_y=True, as_frame=True)
    df = x.copy()
    df['target'] = y

    p4 = Phase4_Target_Analysis(df, target='target', problem_type='classification')
    p4.analyze()
    score, issues = p4.scoring_phase4()
    print(f"Score: {score}/100")
    print(f"Imbalance Ratio: {p4.majority_minority}")
    print(issues)    