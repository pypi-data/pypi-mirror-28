import numpy as np

from ConfigSpace.configuration_space import ConfigurationSpace
from ConfigSpace.hyperparameters import UniformFloatHyperparameter, \
    UniformIntegerHyperparameter, CategoricalHyperparameter, \
    UnParametrizedHyperparameter, Constant

from autosklearn.pipeline.components.base import \
    AutoSklearnRegressionAlgorithm
from autosklearn.pipeline.constants import *


class DecisionTree(AutoSklearnRegressionAlgorithm):
    def __init__(self, criterion, max_features, max_depth,
                 min_samples_split, min_samples_leaf, min_weight_fraction_leaf,
                 max_leaf_nodes, min_impurity_decrease, random_state=None):
        self.criterion = criterion
        self.max_features = max_features
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_leaf_nodes = max_leaf_nodes
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.min_impurity_decrease = min_impurity_decrease
        self.random_state = random_state
        self.estimator = None

    def fit(self, X, y, sample_weight=None):
        from sklearn.tree import DecisionTreeRegressor

        self.max_features = float(self.max_features)
        if self.max_depth == "None" or self.max_depth is None:
            max_depth = self.max_depth = None
        else:
            num_features = X.shape[1]
            self.max_depth = int(self.max_depth)
            max_depth = max(1, int(np.round(self.max_depth * num_features, 0)))
        self.min_samples_split = int(self.min_samples_split)
        self.min_samples_leaf = int(self.min_samples_leaf)
        if self.max_leaf_nodes == "None" or self.max_leaf_nodes is None:
            self.max_leaf_nodes = None
        else:
            self.max_leaf_nodes = int(self.max_leaf_nodes)
        self.min_weight_fraction_leaf = float(self.min_weight_fraction_leaf)
        self.min_impurity_decrease = float(self.min_impurity_decrease)

        self.estimator = DecisionTreeRegressor(
            criterion=self.criterion,
            max_depth=max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            max_leaf_nodes=self.max_leaf_nodes,
            min_weight_fraction_leaf=self.min_weight_fraction_leaf,
            min_impurity_decrease=self.min_impurity_decrease,
            random_state=self.random_state)
        self.estimator.fit(X, y, sample_weight=sample_weight)
        return self

    def predict(self, X):
        if self.estimator is None:
            raise NotImplementedError
        return self.estimator.predict(X)

    @staticmethod
    def get_properties(dataset_properties=None):
        return {'shortname': 'DT',
                'name': 'Decision Tree Classifier',
                'handles_regression': True,
                'handles_classification': False,
                'handles_multiclass': False,
                'handles_multilabel': False,
                'is_deterministic': False,
                'input': (DENSE, SPARSE, UNSIGNED_DATA),
                'output': (PREDICTIONS,)}

    @staticmethod
    def get_hyperparameter_search_space(dataset_properties=None):
        cs = ConfigurationSpace()

        criterion = CategoricalHyperparameter('criterion',
                                              ['mse', 'friedman_mse', 'mae'])
        max_features = Constant('max_features', 1.0)
        max_depth = UniformFloatHyperparameter(
            'max_depth', 0., 2., default_value=0.5)
        min_samples_split = UniformIntegerHyperparameter(
            "min_samples_split", 2, 20, default_value=2)
        min_samples_leaf = UniformIntegerHyperparameter(
            "min_samples_leaf", 1, 20, default_value=1)
        min_weight_fraction_leaf = Constant("min_weight_fraction_leaf", 0.0)
        max_leaf_nodes = UnParametrizedHyperparameter("max_leaf_nodes", "None")
        min_impurity_decrease = UnParametrizedHyperparameter(
            'min_impurity_decrease', 0.0)

        cs.add_hyperparameters([criterion, max_features, max_depth,
                                min_samples_split, min_samples_leaf,
                                min_weight_fraction_leaf, max_leaf_nodes,
                                min_impurity_decrease])

        return cs
