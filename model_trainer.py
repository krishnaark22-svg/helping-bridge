import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import os
class GestureManager:
    def __init__(self,data_file='gesture_data.csv'):
        self.data_file=data_file
        self.model=None
        self.load_data_and_train()
    def load_data_and_train(self):
        if not os.path.exists(self.data_file):
            df=pd.DataFrame(columns=['label']+[f'lm_{i}' for i in range(63)])
            df.to_csv(self.data_file,index=False)
            self.model=None
            return
        try:
            df=pd.read_csv(self.data_file)
            if len(df)<5:
                self.model=None
                return
            x=df.iloc[:,1:].values
            y=df.iloc[:,0].values
            self.model=KNeighborsClassifier(n_neighbors=3)
            self.model.fit(x,y)
            print(f"Model Updated with {len(df)} samples")
        except Exception as e:
            print(f"Error:{e}")
            self.model=None
    def add_data(self,label,landmarks):
        new_rows=[]
        for frame in landmarks:
            row=[label]+list(frame)
            new_rows.append(row)
        df=pd.DataFrame(new_rows,columns=['label']+[f'lm_{i}'for i in range(63)])
        df.to_csv(self.data_file,mode='a',header=not os.path.exists(self.data_file),index=False)
        self.load_data_and_train()
    def reset_data(self):
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        self.model=None
        self.load_data_and_train()
        print("Model Reset: Memory Wiped")
    def predict(self,landmarks):
        if self.model is None:
            return "Waiting for training..."
        try:
            landmarks=np.array(landmarks).reshape(1,-1)
            pred=self.model.predict(landmarks)[0]
            prob=self.model.predict_proba(landmarks).max()
            if prob>0.7:
                return pred
            return "Unknown"
        except:
            return "Processing"