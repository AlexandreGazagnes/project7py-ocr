"""
Main File
"""

import csv
from itertools import combinations
import logging
import sys
from random import *

import pandas as pd


def find_best_solution_1_action(df, maximum=500.00):

    # oN VA TESTER DE FAIRE DES PORTEFEUILLES QUE DE 1 ACTION

    all_candidats = list(df.action_name.values)

    # filtrer par 500

    candidats_inf_500 = list()
    for name in all_candidats:
        val = df.loc[df.action_name == name, "value"].iloc[0]
        # logging.warning(val)
        if val <= maximum:
            candidats_inf_500.append(name)

    logging.warning(f"candidats_inf_500 is {candidats_inf_500}")

    # Tri par gain
    _df = df.sort_values("new_value", ascending=False)

    # filtre les 500 Max par gain
    _df = _df.loc[df.action_name.isin(candidats_inf_500)]

    return _df.iloc[0].action_name, _df.iloc[0].new_value


def find_best_solution_n_action(df,n,maximum=500.00):
    # ON VA TESTER DE FAIRE DES PORTEFEUILLES QUE DE N ACTIONS
    
    all_candidats = list(df.action_name.values)

    list_portefeuilles = sorted(combinations(all_candidats, n))

    portefeuilles_sous_500 = list()
    valeur_totale = 0

    # teste les combinaisons
    for combo in list_portefeuilles:
        for action in combo:
            valeur_totale += df.loc[df.action_name == action, "value"].iloc[0]
            if valeur_totale <= maximum:
                portefeuilles_sous_500.append(combo)
                valeur_totale = 0

    portefeuilles_gains = list()
    # calcul le gain
    for combo in portefeuilles_sous_500:
        gain_total = 0
        gain_total += df.loc[df.action_name == action, "new_value"].iloc[0]
        portefeuilles_gains.append((combo, gain_total))
    # tri
    portefeuilles_gains = sorted(portefeuilles_gains, key=lambda x: x[1], reverse=True)
    return portefeuilles_gains[:n]


def return_csv_file():
    """Load a csv file"""

    # load the file
    with open("data/originalfile.csv", "r", newline="") as csvf:

        # read file
        file_ = csv.reader(csvf, delimiter=",")

    # parse the file
    li = []
    for i, data in enumerate(file_):

        if not i:
            continue

        # logging
        # logging.warning(data)
        # logging.warning(type(data))

        # add to li
        li.append((data[0], float(data[1]), float(data[2])))

    return li


def use_pandas():
    """Laod a cvs file with pandas"""

    df = pd.read_csv("data/originalfile.csv")

    logging.warning(df)

    return df


def compute_values(df):
    """ """

    df["gain"] = round(df.value * df.delta / 100, 4)

    df["new_value"] = df.value + df.gain

    return df


def save_df(df):
    """ """

    df.to_csv("test.csv", index=False)


def main():
    """Main function"""

    df = use_pandas()
    df = compute_values(df)
    solution = find_best_solution_n_action(df,20)
    print(f"$$$$$$$$$$$$$$$$$$$$ {solution} $$$$$$$$$$$$$$$$$$$$$$")


if __name__ == "__main__":
    main()
