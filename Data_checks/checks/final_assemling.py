from checks.Basic_aalysis import Phase1_Data_Analysis
from checks.Distribution_analysis import Phase2_Analysis
from checks.feature_analysis import Phase3_analysis
from checks.class_imalance import Phase4_Target_Analysis
class Phase5_Overall_Score:
    def __init__(self, data , target=None,problem="classification"):
        self.phase1 = Phase1_Data_Analysis(data)
        self.phase1.start_initializing()
        self.phase2 = Phase2_Analysis(data)
        self.phase2.analyze()
        self.phase3 = Phase3_analysis(data)
        self.phase3.analyze_phase3()
        if target is None:
            self.phase4=None
        else:    
         self.phase4 = Phase4_Target_Analysis(data,target,problem_type=problem)
         self.phase4.analyze()
    def calculate(self):
        self.scores_phase1,self.issue1=self.phase1.scoring()
        self.scores_phase2,self.issue2=self.phase2.scoring_phase2()
        self.scores_phase3,self.issue3=self.phase3.score_phase3()
        if self.phase4 is None:
            self.scores_phase4="Not added the target variable"
            self.issue4=None
        else:    
            self.scores_phase4,self.issue4=self.phase4.scoring_phase4()
        if self.phase4:
            self.final_score = round(
                (self.scores_phase1 * 0.25) +
                (self.scores_phase2 * 0.25) +
                (self.scores_phase3 * 0.25) +
                (self.scores_phase4* 0.25), 2
            )
        else:
            # Target column nahi diya toh phase4 skip
            self.final_score = round(
                (self.scores_phase1* 0.35) +
                (self.scores_phase2* 0.35) +
                (self.scores_phase3 * 0.30), 2)

        return self.final_score

    def grade(self):
        if self.final_score >= 90:
            return "A — Excellent Quality ✅"
        elif self.final_score >= 75:
            return "B — Good Quality ✅"
        elif self.final_score >= 60:
            return "C — Average Quality ⚠️"
        elif self.final_score >= 40:
            return "D — Poor Quality ❌"
        else:
            return "F — Critical Issues ❌"

    def report(self, p1_issues, p2_issues, p3_issues, p4_issues=None):
        print(f"\n{'='*50}")
        print(f"  FINAL DATA QUALITY SCORE: {self.final_score}/100")
        print(f"  GRADE: {self.grade()}")
        print(f"{'='*50}")
        print(f"\n📋 Phase 1 — Basic Health: {self.scores_phase1}/100")
        for k, v in p1_issues.items():
            print(f"   {k}: {v}")
        print(f"\n📋 Phase 2 — Distribution: {self.scores_phase2}/100")
        for k, v in p2_issues.items():
            print(f"   {k}: {v}")
        print(f"\n📋 Phase 3 — Feature Analysis: {self.scores_phase3}/100")
        for k, v in p3_issues.items():
            print(f"   {k}: {v}")
        if p4_issues:
            print(f"\n📋 Phase 4 — Target Analysis: {self.scores_phase4}/100")
            for k, v in p4_issues.items():
                print(f"   {k}: {v}")
        print(f"\n{'='*50}\n")
    def run(self):
        self.calculate()
        print(self.final_score)
        self.report(self.issue1,self.issue2,self.issue3,self.issue4)
# if __name__=='__main__':
#     from sklearn.datasets import load_diabetes
#     x, y = load_diabetes(return_X_y=True, as_frame=True)
#     df = x.copy()
#     df['target'] = y
#     score=Phase5_Overall_Score(df,problem="regression")
#     score.run()
