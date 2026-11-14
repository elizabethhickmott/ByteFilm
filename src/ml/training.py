import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder


def main_training(df: pd.DataFrame):
    if df is None:
        raise ValueError("The ML model can only be trained from main_ml.py after preprocessing")

    numerical_columns = ["year", "imdb_rating", "metacritic_rating", "runtime", "rotten_tomatoes"]
    categorical_columns = ["language", "country", "genre", "rated"]

    numeric_pipeline = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", MinMaxScaler())])
    categorical_pipeline = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))])

    preproccesor = ColumnTransformer([("numerical", numeric_pipeline, numerical_columns), ("categorical", categorical_pipeline, categorical_columns)])

    # Separate training and test data
    df_input = df.drop(columns=['worldwide_box_office'])
    df_output = df["worldwide_box_office"]

    x_train, x_test, y_train, y_test = train_test_split(df_input, df_output, test_size=0.3, random_state=1)

    model = Pipeline([("preprocessor", preproccesor), ("regression", LinearRegression())])

    model.fit(x_train, y_train)
    pred = model.predict(x_test)

    joblib.dump(model, '../models/ml_model.pkl')


if __name__ == "__main__":
    main_training(None)