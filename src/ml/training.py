import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def main_training(df: pd.DataFrame):

    # Separate training and test data
    df_input = df.drop(columns=['worldwide_box_office'])
    df_output = df["worldwide_box_office"]

    x_train, x_test, y_train, y_test = train_test_split(df_input, df_output, test_size=0.3, random_state=1)

    model = LinearRegression()
    model.fit(x_train, y_train)

    pred = model.predict(x_test)


if __name__ == "__main__":
    main_training(None)