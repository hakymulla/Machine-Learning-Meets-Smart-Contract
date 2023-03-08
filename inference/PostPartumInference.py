import argparse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn import preprocessing
import pickle
import os


def preprocessing(inputs):

    df = create_df(inputs)

    categorical_columns = [
        "Feeling sad or Tearful",
        "Irritable towards baby & partner",
        "Trouble sleeping at night",
        "Problems concentrating or making decision",
        "Overeating or loss of appetite",
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

    df_copy.fillna(0, inplace=True)

    return df_copy


def create_df(arguments):
    columns = [
        "Age",
        "Feeling sad or Tearful",
        "Irritable towards baby & partner",
        "Trouble sleeping at night",
        "Problems concentrating or making decision",
        "Overeating or loss of appetite",
        "Feeling of guilt",
        "Problems of bonding with baby",
        "Suicide attempt",
    ]

    zipped = dict(zip(columns, arguments))
    pred_df = pd.DataFrame.from_dict(zipped)
    return pred_df


parser = argparse.ArgumentParser(description="Post Partum")
parser.add_argument(
    "--ag", dest="age", type=str, help="Feeling sad or Tearful", default=30
)
parser.add_argument(
    "--t", dest="tearful", type=str, help="Feeling sad or Tearful", default="Yes"
)
parser.add_argument(
    "--i",
    dest="irritated",
    type=str,
    help="Irritable towards baby & partner",
    default="Yes",
)
parser.add_argument(
    "--n", dest="night", type=str, help="Trouble sleeping at night", default="Yes"
)
parser.add_argument(
    "--c",
    dest="concentrate",
    type=str,
    help="Problems concentrating or making decision",
    default="Yes",
)
parser.add_argument(
    "--l", dest="loss", type=str, help="Overeating or loss of appetite", default="Yes"
)

parser.add_argument(
    "--g", dest="guilt", type=str, help="Feeling of guilt", default="Yes"
)
parser.add_argument(
    "--b", dest="baby", type=str, help="Problems of bonding with baby", default="Yes"
)
parser.add_argument(
    "--s", dest="suicide", type=str, help="Suicide attempt", default="Yes"
)


args = parser.parse_args()
age = args.age
tearful = args.tearful
irritated = args.irritated
night = args.night
concentrate = args.concentrate
loss = args.loss
guilt = args.guilt
baby = args.baby
suicide = args.suicide

# model = pickle.load(
#     open(
#         "../job-00d0ff00/raw/QmSH37kDf4k6f7FkbGi5k5MwkX3qkbhghySifhkv9xb5tv/outputs/rf.pkl",
#         "rb",
#     )
# )


inputs = [
    [age],
    [tearful],
    [irritated],
    [night],
    [concentrate],
    [loss],
    [guilt],
    [baby],
    [suicide],
]

model = pickle.load(open("rf.pkl", "rb",))
prediction_data = preprocessing(inputs=inputs)
mapper = {0: "No", 1: "Yes"}
result = model.predict(prediction_data)


print(f"Post Partum Depression? {mapper[result[0]]}.")