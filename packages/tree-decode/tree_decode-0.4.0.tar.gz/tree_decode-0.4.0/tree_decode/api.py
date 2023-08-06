from sklearn.preprocessing import normalize as normalize_values
from . import utils

import numpy as np

__all__ = ["get_tree_info", "get_decision_info", "get_tree_at"]

# Surface this function in the API to enable
# ease of accessing trees in an ensemble class.
get_tree_at = utils.get_tree_at


def get_tree_info(model, normalize=True, precision=3, names=None,
                  label_index=None, tab_size=5, filepath_or_buffer=None):
    """
    Print out the structure of the tree(s) of a tree-based model.

    The print-out will consist of each node and either its leaf-node
    scores OR its decision threshold to determine which path it takes
    subsequently from the fork.

    Parameters
    ----------
    model : sklearn.ensemble.forest.BaseForest or
            sklearn.tree.tree.BaseDecisionTree
        The tree-based model that we are to analyze. Can be an individual
        estimator (e.g. DecisionTreeClassifier) or an ensemble model
        (e.g. RandomForestRegressor).
    normalize : bool, default True
        Whether to normalize the label scores at the leaves so that they
        fall into the range [0, 1].
    precision : int or None, default 3
        The decimal precision with which we display our cutoffs and leaf
        scores. If None is passed in, no rounding is performed.
    names : dict, default None
        A mapping from feature indices to string names. By default, when we
        display the non-leaf node forks, we write "go left if feature {i}
        <= {cutoff}," where "i" is an integer. If names are provided, we will
        map "i" to a particular string name and write instead, "go left if
        {feature-name} <= {cutoff}."
    label_index : int, default None
        Whether we want to display the leaf score for a particular output (e.g.
        classification). If an integer is provided, we will index into the
        scores array at each leaf and only display that score. Otherwise, the
        entire scores array will be displayed. Note that labels are 0-indexed.
    tab_size : int, default 5
        The amount of tabbing to be used when displaying indented lines.
    filepath_or_buffer : str or file handle, default None
        The file or buffer to which to write the output. If none is provided,
        we return the string output as given.

    Returns
    -------
    output_or_nothing : If a filepath or buffer was provided, nothing is
                        returned. Otherwise, the string output is returned.

    Raises
    ------
    NotImplementedError : the model is not supported for extracting info.
    IndexError : the label index provided was out of bounds on the array of
                 output scores provided at each node.
    NotFittedError : the model was not properly fitted yet.
    """

    utils.check_model_type(model)
    utils.check_is_fitted(model)

    output = ""
    names = names or {}
    print_tab = utils.get_tab(size=tab_size)
    estimators = utils.get_estimators(model)

    for index, estimator in enumerate(estimators):
        output += "\n\nInfo for Decision Tree {ind}\n\n".format(ind=index)
        tree = estimator.tree_

        n_nodes = tree.node_count
        children_left = tree.children_left
        children_right = tree.children_right

        features = tree.feature
        thresholds = tree.threshold

        node_depths = np.zeros(shape=n_nodes, dtype=np.int64)
        is_leaves = np.zeros(shape=n_nodes, dtype=bool)

        stack = [(0, -1)]

        while len(stack) > 0:
            node_id, parent_depth = stack.pop()
            node_depths[node_id] = parent_depth + 1

            # Check if we are at a leaf or not.
            if children_left[node_id] != children_right[node_id]:
                stack.append((children_left[node_id], parent_depth + 1))
                stack.append((children_right[node_id], parent_depth + 1))
            else:
                is_leaves[node_id] = True

        previous_leaf = False
        previous_depth = -1

        for i in range(n_nodes):
            node_depth = node_depths[i]
            tabbing = node_depth * print_tab

            if is_leaves[i]:
                if previous_leaf:
                    if previous_depth > 0 and previous_depth > node_depth:
                        output += "\n"  # Readability

                probs = tree.value[i][:]

                if normalize:
                    probs = normalize_values(probs, norm="l1")

                probs = utils.maybe_round(probs, precision=precision)

                if label_index is not None:
                    try:
                        prob = probs[0][label_index]
                        score = "score = {score}".format(score=prob)
                    except IndexError:
                        msg = ("Index {label_index} is out of bounds on "
                               "decision tree {ind} with {n} possible outputs")
                        prob_counts = probs.shape[1]

                        raise IndexError(msg.format(n=prob_counts, ind=index,
                                                    label_index=label_index))
                else:
                    score = "scores = {scores}".format(scores=probs)

                leaf_info = "{tabbing}node={label} left node: {score}"
                output += (leaf_info.format(tabbing=tabbing, label=i,
                                            score=score) + "\n")

                previous_depth = node_depth
                previous_leaf = True
            else:
                if previous_leaf:
                    previous_leaf = False
                    output += "\n"  # Readability

                feature = features[i]
                threshold = thresholds[i]
                cutoff = utils.maybe_round(threshold, precision=precision)

                default = "feature {name}".format(name=feature)
                name = names.get(feature, default)

                node_info = ("{tabbing}node={label}: go to node {left} if "
                             "{name} <= {cutoff} else to node {right}.")
                output += (node_info.format(tabbing=tabbing, label=i,
                                            left=children_left[i],
                                            name=name, cutoff=cutoff,
                                            right=children_right[i]) + "\n")

    utils.write_to_buf(output, filepath_or_buffer)
    return output if filepath_or_buffer is None else None


def get_decision_info(model, data, precision=3, names=None,
                      label_index=None, tab_size=5, filepath_or_buffer=None):
    """
    Get the decision process for a tree on a piece of data.

    Parameters
    ----------
    model : sklearn.ensemble.forest.BaseForest or
            sklearn.tree.tree.BaseDecisionTree
        The tree-based model that we are to analyze. Can be an individual
        estimator (e.g. DecisionTreeClassifier) or an ensemble model
        (e.g. RandomForestRegressor).
    data : np.ndarray
        A 2-D array compromising ONE piece of input data.
    precision : int or None, default 3
        The decimal precision with which we display our cutoffs and leaf
        scores. If None is passed in, no rounding is performed.
    names : dict, default None
        A mapping from feature indices to string names. By default, when we
        display the non-leaf node forks, we write something like "Feature {i}
        Score <= {cutoff}," where "i" is an integer. If names are provided,
        we will map "i" to a particular string name and write instead,
        "{feature-name} <= {cutoff}."
    label_index : int, default None
        Whether we want to display the leaf score for a particular output (e.g.
        classification). If an integer is provided, we will index into the
        scores array at each leaf and only display that score. Otherwise, the
        entire scores array will be displayed. Note that labels are 0-indexed.
    tab_size : int, default 5
        The amount of tabbing to be used when displaying indented lines.
    filepath_or_buffer : str or file handle, default None
        The file or buffer to which to write the output. If none is provided,
        we return the string output as given.

    Returns
    -------
    output_or_nothing : If a filepath or buffer was provided, nothing is
                        returned. Otherwise, the string output is returned.

    Raises
    ------
    NotImplementedError : the model is not supported or has a prediction
                          method that could not be recognized.
    IndexError : the label index provided was out of bounds on the array of
                 output scores provided at each node.
    NotFittedError : the model was not properly fitted yet.
    """

    utils.check_model_type(model)
    utils.check_is_fitted(model)

    output = ""
    names = names or {}

    predict_methods = ("predict_proba", "predict")
    predict_method = None

    for possible_method in predict_methods:
        if hasattr(model, possible_method):
            predict_method = possible_method
            break

    if predict_method is None:
        klass = type(model).__name__
        msg = "{klass} has an unrecognizable predict method"
        raise NotImplementedError(msg.format(klass=klass))

    estimators = utils.get_estimators(model)

    for index, estimator in enumerate(estimators):
        node_indicator = estimator.decision_path(data)
        node_index = node_indicator.indices[node_indicator.indptr[0]:
                                            node_indicator.indptr[1]]

        probs = getattr(estimator, predict_method)(data)[0]
        probs = np.atleast_1d(probs)

        if label_index is not None:
            try:
                probs = probs[label_index]
            except IndexError:
                msg = ("Index {label_index} is out of bounds on "
                       "decision tree {ind} with {n} possible outputs")
                prob_counts = probs.shape[0]

                raise IndexError(msg.format(n=prob_counts, ind=index,
                                            label_index=label_index))

        probs = utils.maybe_round(probs, precision=precision)

        tree = estimator.tree_
        features = tree.feature
        thresholds = tree.threshold

        output += "\nDecision Path for Tree {ind}:\n".format(ind=index)
        leaf_id = estimator.apply(data)

        print_tab = utils.get_tab(size=tab_size)

        for node_id in node_index:
            output += print_tab

            if leaf_id[0] != node_id:
                feature = features[node_id]
                feature_score = data[0, feature]
                feature_threshold = thresholds[node_id]

                default = "Feature {name} Score".format(name=feature)
                name = names.get(feature, default)

                if feature_score <= thresholds[node_id]:
                    threshold_sign = "<="
                else:
                    threshold_sign = ">"

                feature_score = utils.maybe_round(feature_score,
                                                  precision=precision)
                feature_threshold = utils.maybe_round(feature_threshold,
                                                      precision=precision)

                output += ("Decision ID Node {node_id} : {name} = "
                           "{score} {sign} {threshold}\n".format(
                            node_id=node_id, score=feature_score, name=name,
                            sign=threshold_sign, threshold=feature_threshold))
            else:
                output += ("Decision ID Node {node_id} : "
                           "Scores = {scores}\n".format(node_id=node_id,
                                                        scores=probs))

    utils.write_to_buf(output, filepath_or_buffer)
    return output if filepath_or_buffer is None else None
