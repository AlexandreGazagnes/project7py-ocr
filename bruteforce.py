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
    """test for jsut 1 action in portfolio"""

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


def get_combinations(df, n):
    """compute all combinations"""

    if isinstance(df, pd.DataFrame):
        action_list = df["action_name"].unique().tolist()
    else:
        action_list = list(df)

    return list(combinations(action_list, n))


def find_best_solution_n_action(df, n, maximum=500.00):
    """ """
    # attention Jo, ici c'est pas la new value qu'il faut prendre, c'est bien la valeur
    # initiale de l'action

    ###### ICI C'est pas  new_value qu'il faut prendre cest le prix de l'acion
    data = {row["action_name"]: row["new_value"] for _, row in df.iterrows()}

    # ok
    combinations = get_combinations(df, n)

    # ok
    filtered_combinations = list()

    # ok
    for combo in combinations:

        # j'ai changé le le  nom de la variable pour t'aider
        total_depense_achat_des_actions = 0

        # OUI OK, MAIS Attention on break si et seulement la somme des valeurs d'acahts >500
        for action in combo:
            total_depense_achat_des_actions += data[action]
            print(total_depense_achat_des_actions)
            if total_depense_achat_des_actions > maximum:
                # on ne garde pas ce portefeuille
                break
            else:
                filtered_combinations.append(combo)

    # filtered_combinations c'est la liste des action qu'on a le droit d'acheter

    # ENSUITE ICI il FAUT FAIRE +/- la meme chose MAIS... pour la somme des valuers qu'on a gagén
    # TU PEUX COPIER / COLLER LE CODE MAIS Pour l'argent des actions qu'on a gagné

    top_combo = sorted(filtered_combinations, key=lambda x: x[1], reverse=True)

    # OK
    return top_combo[0]


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
    solution = find_best_solution_n_action(df, 20)
    print(f"$$$$$$$$$$$$$$$$$$$$ {solution} $$$$$$$$$$$$$$$$$$$$$$$")


if __name__ == "__main__":
    main()
