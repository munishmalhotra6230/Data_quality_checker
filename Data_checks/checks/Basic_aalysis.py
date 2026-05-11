import pandas as pd 
import numpy as np
class Phase1_Data_Analysis:
    def __init__(self,data):
        self.data=data
        self.features=self.data.columns
        self.Dtypes={}# intialize the phase1 analysis 
        self.missing_values={}
    def start_initializing(self):
        self.Shapex=self.data.shape
        print("Shape is Analyzed")
        self.total_sum_nan=self.data.isna().sum().sum()    
        self.duplicates=self.data.duplicated().sum()
        print("Missing and duplicated values are extracted ")
        for column in self.features:
            self.Dtypes[column]=self.data[column].dtype
        print("dtypes are extracted")    
    def scoring(self):
        score=100
        issue={}
        self.total_cells=self.Shapex[0]*self.Shapex[1]
        self.nan_pct=(self.total_sum_nan/self.total_cells)*100
        if self.nan_pct>30:
            score-=30
            issue["NAN_VALUES"]=f" Crtical_high"
        elif self.nan_pct>10:
            score-=15
            issue["NAN_VALUES"]=f"Moderate_high"
        elif self.nan_pct>5:
            score-=5
            issue["NAN_VALUES"]=f"Minor"
        else:
            issue["NAN_VALUES"]="No issue"
        # duplicated analysis 
        self.dupliacted_pct=(self.duplicates/self.Shapex[0])*100
        if self.dupliacted_pct>10:
            score-=20
            issue["Duplicates"]="High_Duplicates"
        elif self.dupliacted_pct>0:
            score-=10
            issue["Duplicates"]="Minor_Duplicates"
        else:
            issue["Duplicates"]="No Duplicates"
        object_cols = [col for col, dtype in self.Dtypes.items() if str(dtype) == 'object']
        object_ratio = len(object_cols) / len(self.features)

        if object_ratio > 0.8:
            score -= 10
            issue["columns"]="High_Obj_features"
        else:
            issue["columns"]="No_issue"
        rows,columns=self.Shapex  
        if rows < 100:
         score -= 10
         issue["Shaping"]="Small_Data"
        elif rows < 1000:
            score -= 5
            issue["Shaping"]="Minor_Data"
        else:
            issue["Shaping"]="Good_Dataset"

        self.phase1_score = max(0, score)
        self.phase1_issues = issue
        return self.phase1_score,self.phase1_issues
# if __name__ =="__main__":

#     df = pd.DataFrame({
#         'A': [1, 2, None, 4, 1],
#         'B': ['x', 'y', 'z', 'x', 'x'],
#         'C': [1, 2, 3, 4, 1]
#     })

#     p1 = Phase1_Data_Analysis(df)
#     p1.start_initializing()
#     score, issues = p1.scoring()

#     print(f"Phase 1 Score: {score}/100")
#     print(issues) 

    



        

