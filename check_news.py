from data_cleaning import clean_words
import joblib

class Check():
    def __init__(self):
        self.lr_pipe = joblib.load('trained_models/logistic_regression_fnd.pkl')
        self.dtc_pipe = joblib.load('trained_models/decision_tree_classifier_fnd.pkl')
        self.gdc_pipe = joblib.load('trained_models/gradient_boosting_classifier_fnd.pkl')
        self.rfc_pipe = joblib.load('trained_models/random_forest_classifier_fnd.pkl')

    def lr(self,cleaned_news):
        result = self.lr_pipe.predict([cleaned_news])
        return result[0]

    def dtc(self,cleaned_news):
        result = self.dtc_pipe.predict([cleaned_news])
        return result[0]

    def gbc(self,cleaned_news):
        result = self.gdc_pipe.predict([cleaned_news])
        return result[0]

    def rfc(self,cleaned_news):
        result = self.rfc_pipe.predict([cleaned_news])
        return result[0]
