[![Build Status](https://travis-ci.org/gfyoung/tree-decode.svg?branch=master)](https://travis-ci.org/gfyoung/tree-decode)

# tree-decode

Package for removing the black-box around decision trees.

Inspired by Scikit-Learn's webpage on the matter, which you can find here:

http://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html

The library aims to support all decision tree classes in Scikit-Learn. Currently, we support:

* DecisionTreeClassifier
* DecisionTreeRegressor
* ExtraTreeClassifier
* ExtraTreeRegressor

* RandomForestClassifier
* RandomForestRegressor
* ExtraTreesClassifier
* ExtraTreesRegressor

# Installation

The code is available on PyPI and can be installed via pip:

~~~
pip install tree_decode
~~~

You can install the code from source by downloading the repository and running:

~~~
python setup.py install
~~~

After installation, you can run tests but starting up an interactive Python shell and running:

~~~python
import tree_decode as td
td.test()
~~~

Make sure to have `pytest>=3.0` installed for testing purposes. 

# Demo

To see the code in action, you can find the demo by starting up an interactive Python shell and running:

~~~python
import tree_decode as td
td.demo()
~~~
