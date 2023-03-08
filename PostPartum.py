import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn import preprocessing
import pickle
import glob, os, sys


def main(input_dir, output_dir):
    data = glob.glob(f"{input_dir}/*csv")[0]

    print("Loading Dataset")
    df = pd.read_csv(data, date_parser="Timestamp")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    print("Preprocessing Dataset")
    new_df = preprocessing(df)
    X = new_df.drop("Feeling anxious", axis=1)
    print(X.shape)
    print(X.columns)

    y = new_df.loc[:, "Feeling anxious"]

    print("Training Model")
    rf = RandomForestClassifier()
    rf.fit(X, y)

    print("Saving Model")
    pickle.dump(rf, open(f"{output_dir}/rf.pkl", "wb"))


def preprocessing(df):

    categorical_columns = [
        "Feeling sad or Tearful",
        "Irritable towards baby & partner",
        "Trouble sleeping at night",
        "Problems concentrating or making decision",
        "Overeating or loss of appetite",
        "Feeling anxious",
        "Feeling of guilt",
        "Problems of bonding with baby",
        "Suicide attempt",
    ]

    mapper = {"No": 0, "Yes": 1, "Maybe": 3, "Sometimes": 4}

    df_copy = df.copy()
    # Numericalize all categorical columns
    for x in df_copy[categorical_columns]:
        df_copy[x] = df_copy[x].str.capitalize().str.strip(" ")
        df_copy[x] = df_copy[x].map(mapper)

    # Age column feature engineering
    df_copy["Max Age"] = df_copy["Age"].str[:2].astype("int")
    df_copy["Min Age"] = df_copy["Age"].str[3:].astype("int")
    df_copy["Age"] = (df_copy["Max Age"] + df_copy["Min Age"]) / 2

    df_copy.fillna(0, inplace=True)

    # Remove Unnecessary features
    df_copy = df_copy.drop(["Timestamp", "Max Age", "Min Age"], axis=1)

    return df_copy


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Must pass arguments. Format: [command] input_dir output_dir")
        sys.exit()
    main(sys.argv[1], sys.argv[2])


# bacalhau docker run --input-urls https://storage.googleapis.com/kagglesdsdata/datasets/2830731/4881865/post%20natal%20data.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20230213%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230213T090747Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=6ea7673699ed740d9063ecafd753b74349c862156f5ecfff8f9812ae2764d6fab39e8491756f078535ed93e2a61e361130ae2e9dfd6c3e21f393efc62aed43afbec35bcdfe321369b77e6a57cb01a5629134dab55dd13a72ef62d8c81edd76748a71dfc90c7073daed89578d331cee94875f2ee697edaba9153498280ed4e5efea758d18901a74062001915949fa7d156dc7c4ce52effc7116eecffbcce5db1c94425d30a1bc83c00d62b53374188469ec91ab84b0ceb5faa6a81874c8cee68a785d83def90cf4ba1141ed40a4c13253c121cf7c8b7cc02a18f32e8bf8ff858d47c99f1d1f7a3fb502779eef05bbdd3e272e0e248bc532b6a363fe0ea004a814:/inputs/ hakymulla/postpartum:ml

# bacalhau docker run \
# --input-volumes QmWhrRgSA8iHpVSFKUaBe5Azp69VUWp5kudYXp7YCpYmw1:/inputs/ \
# hakymulla/postpartum:ml



# docker buildx build --platform linux/amd64 --push -t hakymulla/postpartum:predict .
# bacalhau docker run --id-only --cpu 1 hakymulla/postpartum:predict -- python PostPartumInference.py  
# bacalhau get e1cbe78a-a0f3-4639-a82e-8795718665a2