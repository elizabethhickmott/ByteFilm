import pandas as pd
import requests
from OMDB_API_KEY import API_KEY

def main():
    #remove_duplicates()
    #remove_tv_series()
    add_box_office()

def add_box_office():
    key = API_KEY

    database_df = pd.read_csv("../resources/database/enhanced_box_office_data(2000-2024)u.csv")

    df_selected = database_df[["Release Group", "$Worldwide", "Year"]]
    df_selected = df_selected.rename(columns={"Release Group": "Title",
                                     "$Worldwide" : "WorldwideBoxOffice"})

    final_df = pd.DataFrame(
        columns=[
            "title",
            "imdb_id",
            "year"
            "worldwide_box_office",
            "imdb_rating",
            "metacritic_rating",
            "language",
            "country",
            "runtime",
            "rotten_tomatoes",
    ])


def remove_tv_series():
    pass

if __name__ == '__main__':
    main()