import pandas as pd 
import numpy as np
class Phase3_analysis:
    
    def __init__(self, data, target=None):
            if target is None:
                self.data = data
            else:
                self.data = data.drop(columns=target)
            
            self.numeric_data = self.data.select_dtypes(include=[np.number]).columns
            self.categorical_data = self.data.select_dtypes(include=['object']).columns
            
            self.constant_columns = []
            self.high_cardinality = {}
            self.high_correlation_pairs = []
    def analyze_phase3(self):
        for col in self.data.columns:
            if self.data[col].nunique()<=1:
                self.constant_columns.append(col)  
            print("constant columns")
        for col in self.categorical_data:
            unique_ratio = self.data[col].nunique() / len(self.data)
            if unique_ratio > 0.9:
                self.high_cardinality[col] = round(unique_ratio, 2)
        print("Cardinality extracted")       
        
        if len(self.numeric_data) >= 2:
            corr_matrix = self.data[self.numeric_data].corr().abs()
            upper = corr_matrix.where(
                np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
            )
            for col in upper.columns:
                for idx in upper.index:
                    val = upper.loc[idx, col]
                    if val > 0.95:
                        self.high_correlation_pairs.append({
                            'feature_1': idx,
                            'feature_2': col,
                            'correlation': round(val, 4)
                        })
        print("Correlation extracted")
    def score_phase3(self):
        score=100
        issues={}
        if len(self.constant_columns) > 0:
            score -= 15
            issues['constant_columns'] = f"found_{len(self.constant_columns)}"
        else:
            issues['constant_columns'] = "none"

        if len(self.high_cardinality) > 3:
                score -= 15
                issues['cardinality'] = "critical"
        elif len(self.high_cardinality) > 0:
            score -= 7
            issues['cardinality'] = "moderate"
        else:
            issues['cardinality'] = "none"
        if len(self.high_correlation_pairs) > 5:
            score -= 20
            issues['correlation'] = "critical"
        elif len(self.high_correlation_pairs) > 0:
            score -= 10
            issues['correlation'] = "moderate"
        else:
            issues['correlation'] = "none"

        self.phase3_score = max(0, score)
        self.phase3_issues = issues
        return self.phase3_score, self.phase3_issues
if __name__=='__main__' :   


    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [1, 1, 1, 1, 1],           # constant
        'C': ['x', 'y', 'z', 'a', 'b'], # high cardinality
        'D': [2, 4, 6, 8, 10]           # correlated with A
    })

    print(len(df['C'].value_counts()))