from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from sklearn.model_selection import StratifiedKFold
from flexmatcher.classify import Classifier
from sklearn import linear_model
import numpy as np


class CharDistClassifier(Classifier):

    """Classify the data-point using counts of character types in the data.

    The CharDistClassifier extracts 7 simple features: number of
    white-space, digit, and alphabetical characters as well as their percentage
    and the total number of characters. Then it trains a logistic regression on
    top of these features.

    Attributes:
        labels (ndarray): Vector storing the labels of each data-point.
        features (ndarray): Matrix storing the extracting features.
        clf (LogisticRegression): The classifier instance.
        num_classes (int): Number of classes/columns to match to
        all_classes (ndarray): Sorted array of all possible classes
    """

    def __init__(self):
        """Initializes the classifier."""
        self.clf = linear_model.LogisticRegression(class_weight='balanced')

    def fit(self, data):
        """Extracts features and labels from the data and fits a model.

        Args:
            data (dataframe): Training data (values and their correct column).
        """
        self.labels = np.array(data['class'])
        self.num_classes = len(data['class'].unique())
        self.all_classes = np.sort(np.unique(self.labels))
        # populating the features dataframe
        feat_df = data[['value']].copy()
        feat_df['length'] = feat_df['value'].apply(lambda val: len(val))
        feat_df['digit_frac'] = feat_df['value'].apply(
            lambda val: 0 if len(val) == 0 else
            sum(char.isdigit() for char in val) / len(val))
        feat_df['digit_num'] = feat_df['value'].apply(
            lambda val: sum(char.isdigit() for char in val))
        feat_df['alpha_frac'] = feat_df['value'].apply(
            lambda val: 0 if len(val) == 0 else
            sum(char.isalpha() for char in val) / len(val))
        feat_df['alpha_num'] = feat_df['value'].apply(
            lambda val: sum(char.isalpha() for char in val))
        feat_df['space_frac'] = feat_df['value'].apply(
            lambda val: 0 if len(val) == 0 else
            sum(char.isspace() for char in val) / len(val))
        feat_df['space_num'] = feat_df['value'].apply(
            lambda val: sum(char.isspace() for char in val))
        self.features = feat_df.ix[:, 1:].as_matrix()
        # training the classifier
        self.clf.fit(self.features, self.labels)

    def predict_training(self, folds=5):
        """Do cross-validation and return probabilities for each data-point.

        Args:
            folds (int): Number of folds used for prediction on training data.
        """
        partial_clf = linear_model.LogisticRegression(class_weight='balanced')
        prediction = np.zeros((len(self.features), self.num_classes))
        skf = StratifiedKFold(n_splits=folds)
        for train_index, test_index in skf.split(self.features, self.labels):
            # prepare the training and test data
            training_features = self.features[train_index]
            test_features = self.features[test_index]
            training_labels = self.labels[train_index]
            # fitting the model and predicting
            partial_clf.fit(training_features, training_labels)
            curr_pred = partial_clf.predict_proba(test_features)
            prediction[test_index] = \
                self.predict_proba_ordered(curr_pred, partial_clf.classes_)
        return prediction

    def predict_proba_ordered(self, probs, classes):
        """Fills out the probability matrix with classes that were missing.

        Args:
            probs (list): list of probabilities, output of predict_proba
            classes_ (ndarray): list of classes from clf.classes_
            all_classes (ndarray): list of all possible classes
        """
        proba_ordered = np.zeros((probs.shape[0], self.all_classes.size),
                                 dtype=np.float)
        sorter = np.argsort(self.all_classes)
        idx = sorter[np.searchsorted(self.all_classes, classes, sorter=sorter)]
        proba_ordered[:, idx] = probs
        return proba_ordered

    def predict(self, data):
        """Predict the class for a new given data.

        Args:
            data (dataframe): Dataframe of values to predict the column for.
        """
        feat_df = data[['value']].copy()
        feat_df['length'] = feat_df['value'].apply(lambda val: len(val))
        feat_df['digit_frac'] = feat_df['value'].apply(
            lambda val: 0 if len(val) == 0 else
            sum(char.isdigit() for char in val) / len(val))
        feat_df['digit_num'] = feat_df['value'].apply(
            lambda val: sum(char.isdigit() for char in val))
        feat_df['alpha_frac'] = feat_df['value'].apply(
            lambda val: 0 if len(val) == 0 else
            sum(char.isalpha() for char in val) / len(val))
        feat_df['alpha_num'] = feat_df['value'].apply(
            lambda val: sum(char.isalpha() for char in val))
        feat_df['space_frac'] = feat_df['value'].apply(
            lambda val: 0 if len(val) == 0 else
            sum(char.isspace() for char in val) / len(val))
        feat_df['space_num'] = feat_df['value'].apply(
            lambda val: sum(char.isspace() for char in val))
        features = feat_df.ix[:, 1:].as_matrix()
        return self.clf.predict_proba(features)
