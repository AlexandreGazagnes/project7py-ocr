"""
Main File
"""

import csv
from itertools import combinations
import logging
import sys
from random import *

import pandas as pd


def find_best_solution(df, maximum=500.00):

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

    # ON VA TESTER DE FAIRE TOUS LES PORTEFEUILLES DE 2 ACTIONS...

    list_actions= []
    for i in range(len(_df)):
        for j in range(i+1, len(_df)):
            list_actions.append([_df.iloc[i].action_name, _df.iloc[j].action_name])


    # oN VA TESETER DE FAIRE TOUS LES PORTEUEILLES DE 3 ACTIONS ...

    # ETC ETC

    # ON VA TESTER DE PRENDRE TOUTES LES ACTIONS

    # #Action A
    # print("\n Action A \n")
    # resultat = 0
    # i=0
    # while i != range(len(df)) and resultat < maximum and df["value"][i] < 110:
    #     print(f"Investir {df["value"][i]} dans {df["action_name"][i]}")
    #     resultat += df["value"][i]
    #     print(resultat)
    #     i += 1
    # print("\nLa solution n°1 est la suivante : Le résultat doit être inférieure à 500 euros et la valeur doit être inférieure à 110 euros.\n")
    # print(f"Total de l'investissement: {resultat}")

    # solution = ["action_A", "action_B", "action_C"]

    # logging.critical("solution " + str(solution))

    # return solution


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
    solution = find_best_solution(df)

    print(f"$$$$$$$$$$$$$$$$$$$$ {solution} $$$$$$$$$$$$$$$$$$f")


if __name__ == "__main__":
    main()
