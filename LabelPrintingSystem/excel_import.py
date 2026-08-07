import pandas as pd


def import_excel(file_path):

    df = pd.read_excel(file_path,header=0)

    df = df.fillna("")

    return df.values.tolist()