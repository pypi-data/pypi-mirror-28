# arboreal

Python package to modularly create decision trees.
`arboreal` uses `pandas` extensively to build decision trees.

Some notable features of `arboreal`:

1. **First-class missing value support.** Each decision tree node splits three ways:
left, right, and missing. You don't have to impute the missing values. Missing values are handled
in first class.

2. **First-class categorical feature support.** Categorical features are not converted into
one-hot encoding. `arboreal` splits a tree node by treating categorical features as-is.
You don't need to convert categorical features to a one-hot feature set.

3. **Modular tree building.** You can build your own tree manually, if you wish. You can build
a part of the tree automatically using data and build the another part of the tree manually
be specifying feature and split points to split on.

This is a work in progress. Stay tuned!

## Installation

`arboreal` can be installed using pip

```bash
pip install --upgrade arboreal
```

## Try it out

```python
import numpy as np
import pandas as pd
from arboreal import Node, Tree, split_ordered_manual

# Build a small example dataset
data = pd.DataFrame({'feature1': [1, np.nan, 3, 4], 'feature2': ['a', 'b', 'c', 'd'],
                     'class': [True, False, False, False]})

# Initialize a tree
t = Tree(data=data, features=['feature1', 'feature2'], label='class', name='example')
print(t.root)
print(t.root.children())  # no children yet


# Manually create a split for 'feature1' at split_point = 3
split = split_ordered_manual(data=t.root.data, feature='feature1', label='class', split_point=3)
t.root.perform_split(split)

# Check the result
print(t.root.children())  # had three children: left, right, and missing

# Predict at any node
print(t.root.predict())
print(t.root.left.predict())
print(t.root.right.predict())
print(t.root.missing.predict())
```

