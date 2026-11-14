from sklearn import preprocessing

# The pre-processing before it was all moved to  sklearn

def preprocess(df):
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

    df = df.drop(["genre", "language", "country", "rated"], axis=1)

    print(df.head().describe())
    print(df.isnull().sum())

    # Scale
    scaler = preprocessing.MinMaxScaler()
    df_scaled = df.copy()
    df_scaled[df.columns] = scaler.fit_transform(df)