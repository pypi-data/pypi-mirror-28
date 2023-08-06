import pandas as pd
import pytest

from vega_datasets import data
from vega_datasets.core import Dataset


@pytest.mark.parametrize('name', Dataset.list_local_datasets())
def test_load_local_dataset(name):
    loader = getattr(data, name.replace('-', '_'))

    df1 = data(name)
    df2 = loader()  # equivalent to data.dataset_name()
    assert df1.equals(df2)

    raw = loader.raw()
    assert type(raw) is bytes


def test_iris_column_names():
    iris = data.iris()
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')

    iris = data.iris.raw()
    assert type(iris) is bytes


def test_stocks_column_names():
    stocks = data.stocks()
    assert type(stocks) is pd.DataFrame
    assert tuple(stocks.columns) == ('symbol', 'date', 'price')

    stocks = data.stocks.raw()
    assert type(stocks) is bytes


def test_cars_column_names():
    cars = data.cars()
    assert type(cars) is pd.DataFrame
    assert tuple(cars.columns) == ('Acceleration', 'Cylinders', 'Displacement',
                                   'Horsepower', 'Miles_per_Gallon', 'Name',
                                   'Origin', 'Weight_in_lbs', 'Year')

    cars = data.cars.raw()
    assert type(cars) is bytes
