import numpy as np


class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def is_leaf_node(self):
        return self.value is not None


class DecisionTree:
    def __init__(self, min_samples_split=2, max_depth=100, n_features=None):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.root = None

    def fit(self, X, y):
        self.n_features = X.shape[1] if not self.n_features else min(X.shape[1], self.n_features)
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_features = np.shape(X)
        n_labels = len(np.unique(y))

        if n_samples <= self.min_samples_split or depth >= self.max_depth or n_labels == 1:
            Y = list(y)
            leaf_value = max(Y, key=Y.count)
            return Node(value=leaf_value)

        feat_idxs = np.random.choice(n_features, self.n_features, replace=False)

        best_feat, best_thresh = self._best_split(X, y, feat_idxs)

        left_indices, right_indices = self._split(X[:, best_feat], best_thresh)
        left_subtree = self._grow_tree(X[left_indices, :], y[left_indices], depth + 1)
        right_subtree = self._grow_tree(X[right_indices, :], y[right_indices], depth + 1)

        return Node(feature=best_feat, threshold=best_thresh, left=left_subtree, right=right_subtree)

    def _best_split(self, X, y, feat_idxs):
        best_gain = -1
        best_idx, best_threshold = None, None

        for feat_idx in feat_idxs:
            X_column = X[:, feat_idx]
            thresholds = np.unique(X_column)

            for threshold in thresholds:
                gain = self._information_gain(y, X_column, threshold)

                if gain > best_gain:
                    best_gain = gain
                    best_idx = feat_idx
                    best_threshold = threshold

        return best_idx, best_threshold

    def _information_gain(self, y, X_column, threshold):
        parent_entropy = self._entropy(y)

        left_indices, right_indices = self._split(X_column, threshold)

        if len(left_indices) == 0 or len(right_indices) == 0:
            return 0

        n = len(y)
        n_left, n_right = len(left_indices), len(right_indices)
        entropy_left = self._entropy(y[left_indices])
        entropy_right = self._entropy(y[right_indices])
        child_entropy = (n_left / n) * entropy_left + (n_right / n) * entropy_right

        information_gain = parent_entropy - child_entropy
        return information_gain

    def _split(self, X_column, split_thresh):
        left_indices = np.where(X_column <= split_thresh)[0]
        right_indices = np.where(X_column > split_thresh)[0]
        return left_indices, right_indices

    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log(p) for p in ps if p > 0])

    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value

        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        else:
            return self._traverse_tree(x, node.right)

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])
