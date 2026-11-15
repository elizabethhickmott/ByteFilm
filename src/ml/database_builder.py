import pandas as pd
import requests
from frontend.OMDB_API_KEY import API_KEY


def main():
    df = add_box_office()
    df.to_csv("../resources/database/final_database.csv", index=False)


def add_box_office():
    BASE_URL = f"http://www.omdbapi.com/"

    database_df = pd.read_csv("../resources/database/enhanced_box_office_data(2000-2024)u.csv")

    df_selected = database_df[["Release Group", "$Worldwide", "Year"]]
    df_selected = df_selected.rename(columns={"Release Group": "title",
                                              "$Worldwide": "worldwide_box_office",
                                              "Year": "year"})
    final_columns = [
        "title",  # handled by previous database
        "imdb_id",
        "rated",
        "year",  # handled by previous database
        "genre",
        "worldwide_box_office",  # handled by previous database
        "imdb_rating",
        "metacritic_rating",
        "language",
        "country",
        "runtime",
        "rotten_tomatoes",
    ]

    final_df = df_selected.reindex(columns=final_columns)
    final_df = final_df.astype({"imdb_id": "string", "rated": "string", "genre": "string", "imdb_rating": "float64",
                                "metacritic_rating": "float64", "language": "string", "country": "string",
                                "runtime": "float64", "rotten_tomatoes": "float64"})

    for index, row in final_df.iterrows():
        movie_title = row["title"]
        year = row["year"]
        request = requests.get(BASE_URL, params={"apikey": API_KEY, "t": movie_title, "y": year}, timeout=15)
        data = request.json()

        request.raise_for_status()

        if not data.get("Response"):
            continue

        final_df.at[index, "imdb_id"] = data.get("imdbID")
        final_df.at[index, "genre"] = data.get("Genre")

        final_df.at[index, "language"] = data.get("Language")
        final_df.at[index, "rated"] = data.get("Rated")
        final_df.at[index, "country"] = data.get("Country")
        runtime = data.get("Runtime")
        runtime_str = ""


        if runtime is not None:
            for char in runtime:
                if char.isdigit():
                    runtime_str += char

        final_df.at[index, "runtime"] = pd.to_numeric(runtime_str, errors="coerce")
        final_df.at[index, "metacritic_rating"] = pd.to_numeric(data.get("Metascore"), errors="coerce")
        final_df.at[index, "imdb_rating"] = pd.to_numeric(data.get("imdbRating"), errors="coerce")

        ratings = data.get("Ratings", [])

        for rating in ratings:
            if rating.get("Source") == "Rotten Tomatoes":
                final_df.at[index, "rotten_tomatoes"] = pd.to_numeric(rating["Value"][:-1], errors="coerce")
    return final_df


if __name__ == '__main__':
    main()
