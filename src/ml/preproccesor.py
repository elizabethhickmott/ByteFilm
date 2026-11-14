import pandas as pd
import matplotlib.pyplot as plt

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
    # Drop imdb_id (not useful to us)
    df = df.drop("imdb_id", axis=1)

    # Fill missing values with medians (for numeric columns)
    imdb_rating_med = df["imdb_rating"].median()
    df["imdb_rating"] = df["imdb_rating"].fillna(imdb_rating_med)

    metacritic_med = df["metacritic_rating"].median()
    df["metacritic_rating"] = df["metacritic_rating"].filla(metacritic_med)

    runtime_med = df["runtime"].median()
    df["runtime"] = df["runtime"].fillna(runtime_med)

    rotten_tomatoes_med = df["rotten_tomatoes"].median()
    df["rotten_tomatoes"] = df["rotten_tomatoes"].fillna(rotten_tomatoes_med)

    # Non-numeric columns cleaning
    cols = ["genre", "language", "country"]

    for col in cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Remove outliers to minimize noise
    

    return df

def main_preprocessing():
    df = analysis()
    cleaned_df = data_cleaning(df)

    return cleaned_df

if __name__ == "__main__":
    main()