# `pipesnake`

*a pandas sklearn-inspired pipeline data processor*

`pipesnake` is a data processing pipeline able to handle Pandas Dataframes. In many cases
Dataframes are used to clean-up data, pre-processing it and to perform feature engineering, 
`pipesnake` tries to simplify these steps, creating complex pipelines.

[documentation](docs/source/index.rst); [examples](examples/README.md);

## Why?

Two easy reasons:
* in many cases Pandas DataFrame is super easy to build _feature extractor_ or _data preocessors_
* in many cases it is useful to have a pipeline that can process both `x` and `y` at the same time

# How can you use `pipesnake` ?

## Install

The easy way:

`pip install --upgrade https://github.com/pierluigi-failla/pipesnake/tarball/master`

to get the latest version available on GitHub, or:

`pip install pipesnake` 

to install the latest stable version on [PyPi](https://pypi.python.org).

## Coding

You can build your own pipelines combining `SeriesPipe` and `ParallelPipe`, both of them can handle list 
of `Transformer`. 

An inherited `Transformer` object is a class which implements the abstract 
`base.Transformer` methods:

```python
from pipesnake.base import Transformer

class MyTransformer(Transformer):
    def __init__(self, name=None, <your params>):
        Transformer.__init__(self, name=name, ...)

    def fit_x(self, x):
        <your implementation>

    def fit_y(self, y):
        <your implementation>

    def transform_x(self, x):
        <your implementation>

    def transform_y(self, y):
        <your implementation>

    def inverse_transform_x(self, x):
        <your implementation>

    def inverse_transform_y(self, y):
        <your implementation>
```

You can find some `Transformers` already implemented in `pipesnake.transformers`. 

Once you have all the needed `Transformers` you can create pipelines for feature engineering or data 
processing using `SeriesPipe` or `ParallelPipe`:

```python
from pipesnake.pipe import ParallelPipe
from pipesnake.pipe import SeriesPipe

pipe = SeriesPipe(transformers=[
    ParallelPipe(transformers=[
        MyTransformer1(<params>),
        MyTransformer2(<params>),
    ]),
    MyTransformer3(<params>),
])
```

More info in the [documentation]() and in the [examples](examples/README.md).

# Batteries included

`pipesnake` comes with several transformers included:

Module | Name | Short Description
--- | --- | ---
`pipenskae.transformers.combiner` | `Combiner` | Apply user function to a column or a set of columns
`pipenskae.transformers.combiner` | `Roller` | Apply the provided function rolling within a given window
`pipenskae.transformers.converter` | `Category2Number` | Convert categorical to number
`pipenskae.transformers.deeplearning` | `LSTMPacker` | Pack rows in order to be used as input for LSTM networks
`pipenskae.transformers.dropper` | `DropDuplicates` | Drop duplicated rows and/or cols
`pipenskae.transformers.dropper` | `DropNanCols` | Drop cols with nans
`pipenskae.transformers.dropper` | `DropNanRows` | Drop rows with nans
`pipenskae.transformers.financial` | `ToReturn` | Convert columns to `financial return`: r_t = (x_t - x_{t-1}) / x_{t-1}
`pipenskae.transformers.imputer` | `ReplaceImputer` | Impute NaNs replacing them
`pipenskae.transformers.imputer` | `KnnImputer` | Impute NaNs using K-nearest neighbors
`pipenskae.transformers.misc` | `ToNumpy` | Convert `x` and `y` to a particular numpy type
`pipenskae.transformers.misc` | `ColumnRenamer` | Rename `x` and `y` columns
`pipenskae.transformers.misc` | `Copycat` | Copy the datasets forward
`pipenskae.transformers.scaler` | `MinMaxScaler` | Min max scaler
`pipenskae.transformers.scaler` | `StdScaler` | Standard deviation scaler
`pipenskae.transformers.scaler` | `MadScaler` | Median absolute deviation scaler
`pipenskae.transformers.scaler` | `UnitLenghtScaler` | Scale the feature vector to have norm 1.0
`pipenskae.transformers.selector` | `ColumnSelector` | Select a given list of column names to keep
`pipenskae.transformers.stats` | `ToSymbolProbability` | Convert values in columns to their probabilities

# How can you contribute to `pipesnake` ?

First of all grab a copy of the repository: 

`git clone https://github.com/scikit-learn/scikit-learn.git`

you can run tests just running `run_tests.py`. 

There is a bunch of things you can contribute as far as `pipesnake` is at its early stages:

* **improvements**: make the library bugfixed, faster, parallel, nicer, cleaner...;
* **documentation**: this library uses Sphinx to generate documentation, so feel free to enrich it;
* **samples**: create examples about using the library;
* **transformers**: develop new-general-purpose transformers to share with the community;
* **tests**: code better tests to extend the coverage and reduce code regression;

or whatever you may thing is relevant to make `pipesnake` better.


