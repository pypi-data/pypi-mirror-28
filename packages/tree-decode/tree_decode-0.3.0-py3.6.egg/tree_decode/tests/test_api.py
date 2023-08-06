from tree_decode.tests.utils import load_model, MockBuffer
from sklearn.exceptions import NotFittedError

import tree_decode.api as api
import numpy as np
import pytest
import os


class BaseApiTest(object):

    min_args = ()

    @staticmethod
    def api_call(*args, **kwargs):
        raise NotImplementedError("API calling not implemented for base class")

    @staticmethod
    def load_model(filename):
        directory = os.path.dirname(__file__)
        directory = os.path.join(directory, "models")

        filename = os.path.join(directory, filename)
        return load_model(filename)

    @classmethod
    def setup_class(cls):
        cls.dtc_model = cls.load_model("dtc-model.pickle")
        cls.dtr_model = cls.load_model("dtr-model.pickle")
        cls.etc_model = cls.load_model("etc-model.pickle")
        cls.etr_model = cls.load_model("etr-model.pickle")

    def test_unsupported(self):
        match = "Function support is not implemented for"
        message = "Expected NotImplementedError regarding no support"

        with pytest.raises(NotImplementedError, match=match, message=message):
            self.api_call([], *self.min_args)

    def test_unfitted(self, tree):
        match = "instance is not fitted yet"
        message = "Expected NotFittedError regarding fitting"

        with pytest.raises(NotFittedError, match=match, message=message):
            self.api_call(tree(), *self.min_args)


class TestGetTreeInfo(BaseApiTest):

    min_args = ()

    @staticmethod
    def api_call(*args, **kwargs):
        return api.get_tree_info(*args, **kwargs)

    def test_basic(self):
        result = self.api_call(self.dtc_model)
        expected = """\
node=0: go to node 1 if feature 3 <= 0.8 else to node 2.
     node=1 left node: scores = [[1. 0. 0.]]

     node=2: go to node 3 if feature 2 <= 4.95 else to node 4.
          node=3 left node: scores = [[0.    0.917 0.083]]
          node=4 left node: scores = [[0.    0.026 0.974]]
"""
        assert result == expected

        result = self.api_call(self.dtr_model)
        expected = """\
node=0: go to node 1 if feature 0 <= 3.133 else to node 4.
     node=1: go to node 2 if feature 0 <= 0.514 else to node 3.
          node=2 left node: scores = [[1.]]
          node=3 left node: scores = [[1.]]

     node=4: go to node 5 if feature 0 <= 3.85 else to node 6.
          node=5 left node: scores = [[-1.]]
          node=6 left node: scores = [[-1.]]
"""
        assert result == expected

        result = self.api_call(self.etc_model)
        expected = """\
node=0: go to node 1 if feature 0 <= 5.364 else to node 2.
     node=1 left node: scores = [[0.882 0.088 0.029]]

     node=2: go to node 3 if feature 3 <= 1.922 else to node 4.
          node=3 left node: scores = [[0.132 0.585 0.283]]
          node=4 left node: scores = [[0. 0. 1.]]
"""
        assert result == expected

        result = self.api_call(self.etr_model)
        expected = """\
node=0: go to node 1 if feature 2 <= 2.289 else to node 2.
     node=1 left node: scores = [[0.]]

     node=2: go to node 3 if feature 2 <= 5.029 else to node 4.
          node=3 left node: scores = [[1.]]
          node=4 left node: scores = [[1.]]
"""
        assert result == expected

    def test_names(self):
        names = {0: "Sepal Length", 1: "Sepal Width",
                 2: "Petal Length", 3: "Petal Width"}
        result = self.api_call(self.dtc_model, names=names)
        expected = """\
node=0: go to node 1 if Petal Width <= 0.8 else to node 2.
     node=1 left node: scores = [[1. 0. 0.]]

     node=2: go to node 3 if Petal Length <= 4.95 else to node 4.
          node=3 left node: scores = [[0.    0.917 0.083]]
          node=4 left node: scores = [[0.    0.026 0.974]]
"""
        assert result == expected

    def test_precision(self):
        precision = 2
        result = self.api_call(self.dtc_model, precision=precision)

        expected = """\
node=0: go to node 1 if feature 3 <= 0.8 else to node 2.
     node=1 left node: scores = [[1. 0. 0.]]

     node=2: go to node 3 if feature 2 <= 4.95 else to node 4.
          node=3 left node: scores = [[0.   0.92 0.08]]
          node=4 left node: scores = [[0.   0.03 0.97]]
"""
        assert result == expected

    def test_normalize(self):
        result = self.api_call(self.dtc_model, normalize=True)
        expected = """\
node=0: go to node 1 if feature 3 <= 0.8 else to node 2.
     node=1 left node: scores = [[1. 0. 0.]]

     node=2: go to node 3 if feature 2 <= 4.95 else to node 4.
          node=3 left node: scores = [[0.    0.917 0.083]]
          node=4 left node: scores = [[0.    0.026 0.974]]
"""
        assert result == expected

        result = self.api_call(self.dtc_model, normalize=False)
        expected = """\
node=0: go to node 1 if feature 3 <= 0.8 else to node 2.
     node=1 left node: scores = [[37.  0.  0.]]

     node=2: go to node 3 if feature 2 <= 4.95 else to node 4.
          node=3 left node: scores = [[ 0. 33.  3.]]
          node=4 left node: scores = [[ 0.  1. 38.]]
"""
        assert result == expected

    def test_label_index(self):
        label_index = 2
        result = self.api_call(self.dtc_model, label_index=label_index)

        expected = """\
node=0: go to node 1 if feature 3 <= 0.8 else to node 2.
     node=1 left node: score = 0.0

     node=2: go to node 3 if feature 2 <= 4.95 else to node 4.
          node=3 left node: score = 0.083
          node=4 left node: score = 0.974
"""
        assert result == expected

        label_index = 10

        match = "is out of bounds on a decision tree with"
        message = "Expected NotImplementedError regarding no support"

        with pytest.raises(IndexError, match=match, message=message):
            self.api_call(self.dtc_model, label_index=label_index)

    def test_tab_size(self):
        tab_size = 0
        result = self.api_call(self.dtc_model, tab_size=tab_size)

        expected = """\
node=0: go to node 1 if feature 3 <= 0.8 else to node 2.
node=1 left node: scores = [[1. 0. 0.]]

node=2: go to node 3 if feature 2 <= 4.95 else to node 4.
node=3 left node: scores = [[0.    0.917 0.083]]
node=4 left node: scores = [[0.    0.026 0.974]]
"""
        assert result == expected

        tab_size = 2
        result = self.api_call(self.dtc_model, tab_size=tab_size)

        expected = """\
node=0: go to node 1 if feature 3 <= 0.8 else to node 2.
  node=1 left node: scores = [[1. 0. 0.]]

  node=2: go to node 3 if feature 2 <= 4.95 else to node 4.
    node=3 left node: scores = [[0.    0.917 0.083]]
    node=4 left node: scores = [[0.    0.026 0.974]]
"""
        assert result == expected

    def test_buffer(self):
        buffer = MockBuffer()
        result = self.api_call(self.dtc_model, filepath_or_buffer=buffer)

        expected = """\
node=0: go to node 1 if feature 3 <= 0.8 else to node 2.
     node=1 left node: scores = [[1. 0. 0.]]

     node=2: go to node 3 if feature 2 <= 4.95 else to node 4.
          node=3 left node: scores = [[0.    0.917 0.083]]
          node=4 left node: scores = [[0.    0.026 0.974]]
"""
        # We wrote to a buffer, so the result
        # is not returned to the user.
        assert result is None
        assert buffer.read() == expected


class TestGetDecisionInfo(BaseApiTest):

    min_args = (np.array([]),)

    dtr_data = np.array([[5.8]])
    dtc_data = np.array([[5.8, 2.8, 5.1, 2.4]])

    @staticmethod
    def api_call(*args, **kwargs):
        return api.get_decision_info(*args, **kwargs)

    def test_basic(self):
        result = self.api_call(self.dtc_model, self.dtc_data)
        expected = """\
Decision Path for Tree:
     Decision ID Node 0 : Feature 3 Score = 2.4 > 0.8
     Decision ID Node 2 : Feature 2 Score = 5.1 > 4.95
     Decision ID Node 4 : Scores = [0.    0.026 0.974]
"""
        assert result == expected

        result = self.api_call(self.dtr_model, self.dtr_data)
        expected = """\
Decision Path for Tree:
     Decision ID Node 0 : Feature 0 Score = 5.8 > 3.133
     Decision ID Node 4 : Feature 0 Score = 5.8 > 3.85
     Decision ID Node 6 : Scores = [-0.869]
"""
        assert result == expected

    def test_precision(self):
        precision = 2
        result = self.api_call(self.dtc_model, self.dtc_data,
                               precision=precision)

        expected = """\
Decision Path for Tree:
     Decision ID Node 0 : Feature 3 Score = 2.4 > 0.8
     Decision ID Node 2 : Feature 2 Score = 5.1 > 4.95
     Decision ID Node 4 : Scores = [0.   0.03 0.97]
"""
        assert result == expected

    def test_names(self):
        names = {0: "Sepal Length", 1: "Sepal Width",
                 2: "Petal Length", 3: "Petal Width"}
        result = self.api_call(self.dtc_model, self.dtc_data, names=names)
        expected = """\
Decision Path for Tree:
     Decision ID Node 0 : Petal Width = 2.4 > 0.8
     Decision ID Node 2 : Petal Length = 5.1 > 4.95
     Decision ID Node 4 : Scores = [0.    0.026 0.974]
"""
        assert result == expected

    def test_label_index(self):
        label_index = 2
        result = self.api_call(self.dtc_model, self.dtc_data,
                               label_index=label_index)

        expected = """\
Decision Path for Tree:
     Decision ID Node 0 : Feature 3 Score = 2.4 > 0.8
     Decision ID Node 2 : Feature 2 Score = 5.1 > 4.95
     Decision ID Node 4 : Scores = 0.974
"""
        assert result == expected

    def test_tab_size(self):
        tab_size = 0
        result = self.api_call(self.dtc_model, self.dtc_data,
                               tab_size=tab_size)

        expected = """\
Decision Path for Tree:
Decision ID Node 0 : Feature 3 Score = 2.4 > 0.8
Decision ID Node 2 : Feature 2 Score = 5.1 > 4.95
Decision ID Node 4 : Scores = [0.    0.026 0.974]
"""
        assert result == expected

        tab_size = 2
        result = self.api_call(self.dtc_model, self.dtc_data,
                               tab_size=tab_size)

        expected = """\
Decision Path for Tree:
  Decision ID Node 0 : Feature 3 Score = 2.4 > 0.8
  Decision ID Node 2 : Feature 2 Score = 5.1 > 4.95
  Decision ID Node 4 : Scores = [0.    0.026 0.974]
"""
        assert result == expected

    def test_buffer(self):
        buffer = MockBuffer()
        result = self.api_call(self.dtc_model, self.dtc_data,
                               filepath_or_buffer=buffer)

        expected = """\
Decision Path for Tree:
     Decision ID Node 0 : Feature 3 Score = 2.4 > 0.8
     Decision ID Node 2 : Feature 2 Score = 5.1 > 4.95
     Decision ID Node 4 : Scores = [0.    0.026 0.974]
"""
        # We wrote to a buffer, so the result
        # is not returned to the user.
        assert result is None
        assert buffer.read() == expected
