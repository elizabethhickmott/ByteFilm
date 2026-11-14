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
    # Drop imdb_id and title (not useful to us)
    df = df.drop("imdb_id", axis=1)
    df = df.drop("title", axis=1)

    return df

def main_preprocessing():
    df = analysis()
    cleaned_df = data_cleaning(df)

    return cleaned_df

if __name__ == "__main__":
    main()