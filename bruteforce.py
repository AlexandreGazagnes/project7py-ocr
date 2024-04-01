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
    

    #Action A
    print("\n Action A \n")
    resultat = 0
    i=0
    while i != range(len(df)) and resultat < maximum and df["value"][i] < 110:
        print(f"{df["action_name"][i]} {df["value"][i]} {df["delta"][i]}")
        resultat += df["value"][i]
        print(resultat)
        i += 1
    print("\nLa solution n°1 est la suivante : Le résultat doit être inférieure à 500 euros et la valeur doit être inférieure à 110 euros.\n")
    print(f"Le resultat de cette solution est de {resultat}")
    
    solution = ["action_A", "action_B", "action_C"]

    logging.critical("solution " + str(solution))

    return solution


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
            logging.warning(data)
            logging.warning(type(data))

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


if __name__ == "__main__":
    main()
