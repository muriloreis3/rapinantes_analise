import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calc_percentage(df, column, decimals=2):
    """ Returns a series with the percentages of a column"""
    return (df[column].value_counts(normalize=True)).round(decimals).rename('Porcentagem')

print('Hello World')