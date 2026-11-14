import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing


def main():
    main_preprocessing()

def analysis():
    df = pd.read_csv("../resources/database/final_database.csv")

    # Observe missing values
    print("Sum of null values:", df.isnull().sum())

    # Describe dataset
    print("Description of dataset:", df.describe())

    # Histogram of y values (box office)
    df_quality = df['worldwide_box_office']
    plt.figure(figsize=(5, 8))
    plt.hist(df_quality, bins=10)
    plt.title("Histogram of worldwide box office quality")
    plt.ylabel("Frequency")
    plt.xlabel("Total box office returns")
    plt.show()
    # Data is not normalized

    return df

def data_cleaning(df : pd.DataFrame):
    # Drop imdb_id and title (not useful to us)
    df = df.drop("imdb_id", axis=1)
    df = df.drop("title", axis=1)

    # Fill missing values with medians (for numeric columns)
    imdb_rating_med = df["imdb_rating"].median()
    df["imdb_rating"] = df["imdb_rating"].fillna(imdb_rating_med)

    metacritic_med = df["metacritic_rating"].median()
    df["metacritic_rating"] = df["metacritic_rating"].fillna(metacritic_med)

    runtime_med = df["runtime"].median()
    df["runtime"] = df["runtime"].fillna(runtime_med)

    rotten_tomatoes_med = df["rotten_tomatoes"].median()
    df["rotten_tomatoes"] = df["rotten_tomatoes"].fillna(rotten_tomatoes_med)

    # Non-numeric columns cleaning
    cols = ["genre", "language", "country", "rated"]

    le = preprocessing.LabelEncoder()

    for col in cols:
        df[col] = df[col].fillna(df[col].mode()[0])
        # Encode non-numeric values
        df[col + "_encoded"] = le.fit_transform(df[col])


    df = df.drop(["genre", "language", "country", "rated"],  axis=1)

    print(df.head().describe())
    print(df.isnull().sum())

    # Remove outliers to minimize noise
    # Remove outliers by first identifying them in every column using the interquartile range formula and saving them in the ranges dictionary
    # The upper and lower ranges are stored in a dictionary where the key is the name of every row and the value is a tuple
    ranges = {}

    # Placeholder variables for Q1 and Q3
    first_quart = 0
    third_quart = 0


    for col_name, col_value in df.describe().items():
        for name, value in col_value.items():
            if name == "25%":
                first_quart = value

            if name == "75%":
                third_quart = value

        IQR = third_quart - first_quart

        lower_bound = first_quart - (IQR * 1.5)
        upper_bound = third_quart + (IQR * 1.5)
        ranges[f'{col_name}'] = (lower_bound, upper_bound)


    for key in ranges.keys():
        df.loc[(df[key] < ranges[key][0]) | (df[key] > ranges[key][1]), key] = df[
            key].median()

    print(df.describe())

    # Scale
    df_scaled = preprocessing.MinMaxScaler().fit_transform(df)

    return df_scaled

def main_preprocessing():
    df = analysis()
    cleaned_df = data_cleaning(df)

    return cleaned_df

if __name__ == "__main__":
    main()