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
