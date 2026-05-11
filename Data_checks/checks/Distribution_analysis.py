import pandas as pd 
import numpy as np 
from scipy import stats
class Phase2_Analysis():
    def __init__(self,data,target=None):
        if target is  None:
            self.data=data
        else: self.data=data.drop(columns=target)   
        self.numeric_data=self.data.select_dtypes(include=[np.number]).columns

        self.basic_stats = {}
        self.skewness = {}
        self.outliers = []
        self.zero_variance = []
    def analyze(self):
        for column in self.numeric_data:
            self.skewness[column]=self.data[column].skew()
        print("skewness extracted")
        for columns in self.numeric_data:
            q1=self.data[columns].quantile(0.25)
            q3=self.data[columns].quantile(0.75)
            iqr=q3-q1
            lower_bound=q1-1.5*iqr
            upper_bound=q3+1.5*iqr
            outlier=len(self.data[(self.data[columns]<lower_bound)|(self.data[columns]>upper_bound)])
            self.outliers.append(outlier)
        self.total_outliers=np.sum(self.outliers)
        self.outliers_pct=(self.total_outliers/len(self.data)   )*100 
        for col in self.numeric_data:
            if self.data[col].nunique() <= 1:
                self.zero_variance.append(col)
                print("Column with zero variance")
    def scoring_phase2(self):
        score=100
        issue={
        }  
        highly_skewed = [
            col for col, val in self.skewness.items()
            if abs(val) > 1
        ]
        moderately_skewed = [
            col for col, val in self.skewness.items()
            if 0.5 < abs(val) <= 1
        ]
        self.skew_ratio=(len(highly_skewed)/len(self.numeric_data))*100
        if self.skew_ratio>0.5:
            score-=20
            issue["skewness"]="Critical_skewness"
        elif len(moderately_skewed)>0:
            score-=10
            issue['skewness']="moderate_skewness"
        else:
            issue["skewness"]="no_skewess"

        # outlier detection
        if self.outliers_pct>15:
            score-=20
            issue["outlier"]="high"
        elif self.outliers_pct>5:
            score-=10
            issue["outlier"]="moderate" 
        else:
            issue["outlier"]="None"
        if len(self.zero_variance)>0:
            score-=10
            issue["zero_variance"] ="Yes"
        else:
            issue["zero_variance"]="no_column"
        self.phase2_score = max(0, score)
        self.phase2_issues = issue
        return self.phase2_score, self.phase2_issues                      

if __name__=="__main__":

    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 1000],   # outlier hai
        'B': [1, 1, 1, 1, 1],       # zero variance
        'C': np.random.exponential(2, 5)  # skewed
    })

    p2 = Phase2_Analysis(df)
    p2.analyze()
    score, issues = p2.scoring_phase2()

    print(f"Phase 2 Score: {score}/100")
    print(issues)