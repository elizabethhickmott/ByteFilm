import pandas as pd

def main_training(df: pd.DataFrame):
    if df == None:
        raise "This file can only be used from main_ml.py after preprocessing"

    pass

if __name__ == "__main__":
    main_training(None)