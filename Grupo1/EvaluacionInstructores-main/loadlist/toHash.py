import hashlib
import pandas as pd
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import numpy as np


def toHash(dataframe):
    """
    Returns a hash of the dataframe.
    """
    # print(hashlib.algorithms_available)

    for i, row in dataframe.iterrows():
        val = row['NUMERO_DE_DOCUMENTO'] + row['NOMBRE'] + row['APELLIDOS']

        dataframe.at[i, 'HASH'] = hashlib.md5(val.encode()).hexdigest()

    return dataframe

def toHashCoord(dfcoord):
    """
    Returns a hash of the dataframe.
    """
    # print(hashlib.algorithms_available)

    return dfcoord
        