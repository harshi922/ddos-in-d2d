import sys
import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif, chi2
from sklearn.feature_selection import SelectKBest, SelectPercentile
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor




class DoubleFilter:

    def __init__(self,cor_thresh=0.8,select_k=10):
        self.cor_thresh = cor_thresh
        self.select_k = select_k
    
    # find the correlated features with a correlation greater than cor_value
    def correlation_elimination(self,X, flag=0):

        correlated_features = set()
        correlation_matrix = X.corr()
        for i in range(len(correlation_matrix .columns)):
            for j in range(i):
                if abs(correlation_matrix.iloc[i, j]) > self.cor_thresh:
                    colname = correlation_matrix.columns[i]
                    correlated_features.add(colname)

        if flag==1:
            print(correlated_features)
            save = int(input("Enter 1 to commit the results and return modified dataset and 0 to exit\n"))
            if save==1:
                global output_path 
                X.drop(labels=correlated_features, axis=1, inplace=True)
                y = pd.DataFrame(y, columns=[' Label'])
                df = pd.concat([X,y],axis=1)
                df.to_csv(output_path, index=False)
        
        else:
            X.drop(labels=correlated_features, axis=1, inplace=True)
            return X

    
    # create the SelectKBest with the mutual info strategy.
    def mutual_info_selection(self, X, y, flag = 0):

        # get only the numerical features.
        numerical_x_train = X[X.select_dtypes([np.number]).columns]
        selection = SelectKBest(mutual_info_classif, k=self.select_k).fit(numerical_x_train, y)
        features = X.columns[selection.get_support()]


        if flag==1:
            print(features)
            save= int(input("Enter 1 to commit the results and return modified dataset and 0 to exit\n"))
            if save==1:
                output_path = input("Enter the output path:\n ")
                X = X[list(features)]
                y = pd.DataFrame(y, columns=[' Label'])
                df = pd.concat([X,y],axis=1)
                df.to_csv(output_path, index=False)
        
        else:
            X = X[list(features)]
            return X
    

    def combined_filters(self,X,y):
        global output_path
        X = self.correlation_elimination(X)
        X = self.mutual_info_selection(X,y)
        y = pd.DataFrame(y, columns=[' Label'])
        df = pd.concat([X,y],axis=1)
        df.to_csv(output_path, index=False)


def main():

    df = sys.argv[2]
    output_path = sys.argv[3]
    if len(sys.argv) > 4:
        cor_thresh = sys.argv[4]
        if len(sys.argv) > 5:
            select_k = sys.arg[5]

    #Delete columns with object type data
    obj_cols = df.select_dtypes(include='object').columns.tolist()
    df = df.drop(columns=obj_cols)

    # split into features and label
    X = df.drop([' Label'], axis=1)
    y = df[' Label']
    selector = DoubleFilter()

    if sys.argv[1] == '-cor':
        selector.correlation_elimination(X,y,flag=1)
    elif sys.argv[1] == '-mi':
        selector.mutual_info_selection(X,y,flag=1)
    elif sys.argv[1] == '-dd':
        selector.combined_filters(X,y,flag=1)

if __name__ == '__main__':
    main()





