"""A script to process book data."""
from os.path import isfile
import csv
import re

import glob
import pandas as pd


def is_file_we_want() -> list:
    """returns a list of files under a certain naming scheme
    glob glob"""
    return [file for file in glob.glob("data/RAW_DATA*") if isfile(file)]


def csv_files_to_one_list(files: list) -> list:
    """Combines all csv files requested into a single list"""
    df_list = []
    for file in files:

        with open(file, 'r', encoding='utf-8') as f:
            f.readline()
            csv_reader = csv.reader(f)
            for line in csv_reader:
                line[3] = re.sub(r"\(.*\)", '', line[3])[:-1]
                line[6] = float(line[6].replace(',', '.'))
                line[7] = line[7].strip('`')

                df_list.append(line[3:])
    return df_list


def filter_rows(df: pd) -> pd:
    """Filters rows to remove all '' values and nan values"""
    df = df.dropna()
    for column in df.columns.values.tolist():
        df = df.drop(df[df[f'{column}'] == ''].index)
    return df


def format_rows(df: pd, author_df: pd) -> pd:
    """Merges two dataframes, then formats, renames and reorders the columns
       Then sorts teh rows by rating, desc"""
    df['author_id'] = pd.to_numeric(df['author_id'])
    df = pd.merge(df, author_df, on='author_id', how='left')

    df['author_name'] = df['name']
    df = df[['title', 'author_name', 'year', 'rating', 'ratings']]
    df = df.sort_values('rating', ascending=False)
    return df


def transform(list_of_books: list) -> csv:
    """Takes a list, turns it into a dataframe and then formats it correctly
    then writes to csv"""
    author_df = pd.read_csv('data/AUTHORS.csv', index_col='author_id')
    df = pd.DataFrame(list_of_books, columns=[
                      'title', 'author_id', 'year', 'rating', 'ratings'])

    df = filter_rows(df)
    df = format_rows(df, author_df)

    df.to_csv('data/PROCESSED_DATA.csv', index=False)


if __name__ == "__main__":
    list_of_files = is_file_we_want()
    book_list = csv_files_to_one_list(list_of_files)
    transform(book_list)
