import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
from sklearn import ensemble
import sys

class Prediction:
    def __init__(self, path):
        self.dataset = pd.read_csv(path)
        self.features = []

    def trainSet(self):
        for lab in self.dataset:
            if lab == "17/18 goals":
                continue
            self.features.append(lab)

        train1 = self.dataset.sort_values('16/17 goals', ascending=False)
        print(train1.head(n=4))
        train1 = self.dataset.drop(['17/18 goals', 'name'], axis=1)

        labels = self.dataset['17/18 goals']
        # print (labels)

        x_train, x_test, y_train, y_test = train_test_split(train1, labels, test_size=0.10, random_state=2)
        x_train = x_train.fillna(0)
        # print (x_train)
        y_train = y_train.fillna(0)
        x_test = x_test.fillna(0)
        y_test = y_test.fillna(0)

        print(train1.head())

        return x_train, y_train, x_test, y_test


    def cleanCSV(self):
        conv_pos = [1 if values == 'W' else 0 for values in self.dataset.position]
        self.dataset['position'] = conv_pos

        conv_foot = []
        for values in self.dataset.foot:
            if values == 'right':
                conv_foot.append(0)
            elif values == 'left':
                conv_foot.append(1)
            else:
                conv_foot.append(2)
        self.dataset['foot'] = conv_foot

    def trainGBR(self, x_train, y_train):
        clf = ensemble.GradientBoostingRegressor(n_estimators=400, max_depth=2, min_samples_split=2,
                                                 learning_rate=0.1, loss='ls')

        clf.fit(x_train, y_train)
        joblib.dump(clf, 'GBR.pkl')
        return clf

    def predictGoalsbyName(self, name, clf):
        new = self.dataset.set_index(['name'])
        df = new.loc[name].to_frame()
        # df = df.drop(['17/18 minutes'])
        actual = df.iloc[4][0]

        df = df.drop(['17/18 goals'])
        df = df.transpose()
        print(df)
        predicted = str(clf.predict(df))
        print("\nPredicted goals for {0} in 2017/18: {1}".format(name, predicted))
        print("Actual: ", actual)
        return predicted

def Main():
    laLiga = Prediction('Strikers_Cleaned.csv')

    laLiga.cleanCSV()

    x_train, y_train, x_test, y_test = laLiga.trainSet()

    # reg = LinearRegression()
    # reg.fit(x_train, y_train)
    # print("Score: ", reg.score(x_test, y_test))
    # player_name = sys.argv[1]
    # print("input ", player_name)
    # laLiga.trainGBR(x_train, y_train)

    clf = joblib.load('GBR.pkl')
    print(type(clf))
    gbr = clf.score(x_test, y_test)

    pred_goals = []
    for name in laLiga.dataset['name']:
        print(str(name))

    predicted = laLiga.predictGoalsbyName("Isaac Success", clf)
    laLiga.predictGoalsbyName("Harry Kane", clf)
    laLiga.predictGoalsbyName("Marcus Rashford", clf)

    print("\nGBR score: ", gbr)

if __name__ == '__main__' :
    Main()