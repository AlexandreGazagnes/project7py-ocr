"""
Test de la function
"""

import pytest

import logging

from bruteforce import (
    compute_values,
    return_csv_file,
    save_df,
    use_pandas,
    find_best_solution,
    get_combinations,
)


def test_read_csv():

    data = return_csv_file()


def test_use_pandas():

    df = use_pandas()


def test_compute_values():

    df = use_pandas()
    df = compute_values(df)


def test_save_df():

    df = use_pandas()
    df = compute_values(df)
    save_df(df)


def test_find_best_solution():

    df = use_pandas()
    df = compute_values(df)
    solution = find_best_solution(df)


def test_get_combinations():

    li = [
        (["a", "b"], 1, 2),
        (["a", "b"], 2, 1),
        (["a", "b", "c"], 1, 3),
        (["a", "b", "c"], 2, 3),
        (["a", "b", "c"], 3, 1),
    ]

    for p, n, expec in li:
        out = get_combinations(p, n)
        out = list(out)
        print(f"p {p}, n {n}, expec {expec}, out : {out}")
        assert len(out) == expec
