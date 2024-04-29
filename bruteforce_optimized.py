"""
Main File
"""

import csv
from itertools import combinations
import logging
import time
from random import *

import pandas as pd


def get_combinations(df, n):
    """compute all combinations"""

    if isinstance(df, pd.DataFrame):
        action_list = df["action_name"].unique().tolist()
    else:
        action_list = list(df)

    return list(combinations(action_list, n))


def find_best_solution_n_action(df, n, max_obseverd_value, maximum=500.00):

    t_0 = time.time()

    top_combo = ""
    cost = -1
    max_revenu = -1

    # liste des actions
    all_candidats = list(df.action_name.values)

    # si pas n : on met par defualt la liste des actions entiere (on prends toute les actions)
    if not n:
        n = len(all_candidats)

    # tous les combos à n actions
    combinations = get_combinations(all_candidats, n)

    print(f"finding best portoflio for {n} actions soit {len(combinations) } com")

    # liste des combinaisons filtrées
    filtered_combinations = list()

    # iterer sur toutes les combinaisons
    # On va mettre de coté les combos trop cher
    for combo in combinations:

        ############################################
        # ON ne calcule pas les combos qui sont d'office trop cher
        ############################################

        _df = df.loc[df.action_name.isin(combo)]
        _min = _df.value.min()
        _min_theorique_valeur_d_achat = n * _min
        # ca veut dire pas besoinde chercher dans tous les combos, ceux qui seraient trop cher
        # il le sont tous !!!!
        if _min_theorique_valeur_d_achat > maximum:
            # print(f"Pas besoin de chercher ce combo à {n} actions, tous trop cher !!! ")
            # return [f"que des combos trop cher pour {n} actions", -1]
            continue

        # j'ai changé le le  nom de la variable pour t'aider
        total_depense_achat_des_actions = 0

        # OUI OK, MAIS Attention on break si et seulement la somme des valeurs d'acahts >500
        for action in combo:
            total_depense_achat_des_actions += df.loc[
                df.action_name == action, "value"
            ].iloc[0]

        # la on a caclulé la valeur d'achat du combo
        # et on va filter pour savoir si > 500
        if total_depense_achat_des_actions > maximum:
            # on ne garde pas ce portefeuille
            pass
        else:
            filtered_combinations.append(combo)

    # filtered_combinations c'est la liste des action qu'on a le droit d'acheter

    #####################################################
    # total_revenus
    #####################################################

    # ENSUITE ICI il FAUT FAIRE +/- la meme chose MAIS... pour la somme des valuers qu'on a gagén
    # TU PEUX COPIER / COLLER LE CODE MAIS Pour l'argent des actions qu'on a gagné

    for combo in filtered_combinations:

        ############################################
        # on ne calcule pas d'office les combos qui ne sont pas rentables
        ############################################

        _max = df.value.max()
        _max_theorique_valeur_gagnee = n * _max
        if _max_theorique_valeur_gagnee < max_obseverd_value:
            # print(
            #     f"Pas besoin de chercher les combos à {n} actions, moins rentanble que ce qu'on a deja trouvé !!! "
            # )
            # return [f"que des combos pas assez rentables {n} actions", -1]
            continue

        total_value = 0
        # OUI OK, MAIS Attention on break si et seulement la somme des valeurs d'acahts >500
        for action in combo:
            total_value += df.loc[df.action_name == action, "new_value"].iloc[0]

        # la on a caclulé la valeur d'achat du combo
        # et on va filter pour savoir si > 500
        if total_value > max_revenu:
            # on ne garde pas ce portefeuille
            max_revenu = total_value
            top_combo = combo

    # OK
    if top_combo:
        cost = df.loc[df.action_name.isin(top_combo), "value"].sum()

    return n, top_combo, cost, max_revenu, round(time.time() - t_0, 2)


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

    print(df)

    all_candidats = list(df.action_name.values)

    n_candidates = len(all_candidats)

    old_best_revnue = 0
    li = []

    # on teste tous les portefeuilles à 1, action, à 2 action à 3 actions etc etc etc
    for i in range(n_candidates - 1, 1, -1):

        # on part DESORMAIS du plus grand nombre de combo et on va à a 1
        # si un combo est d'office trop cher // pas évalué => nombre actions * valeur Min d'une action du portefeuille
        # si un combo a 0% de chances de pas faire mieux => pas évalueée si notre max_value par ex 600 = > il suffit de prendre
        # le max téhorique et de l'evaluer
        # ansi on gagne en rapidité en virant d'office tous les combos trop cher / pas assez gagnants
        # soit 90% des combos!

        n, combo, cost, new_possible_best_revenue, duration = (
            find_best_solution_n_action(
                df,
                i,
                old_best_revnue,
                500.00,
            )
        )

        li.append([n, combo, cost, new_possible_best_revenue, duration])

        if new_possible_best_revenue > old_best_revnue:
            old_best_revnue = new_possible_best_revenue

    # on tri notre liste finale
    li = sorted(li, key=lambda i: i[2], reverse=True)

    # on prend le dernier
    final_i, final_combo, final_best_revenue = li[0]

    print(
        f"\n\n\n$$$$$$$$$ n_action {final_i }, combo{ final_combo} => revenue {final_best_revenue} $$$$$$$$\n\n\n"
    )

    print(f"3 best combos : {li[:3]}")


if __name__ == "__main__":
    main()
