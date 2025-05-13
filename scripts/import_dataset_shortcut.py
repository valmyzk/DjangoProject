"""
Script that downloads, processes and imports the required datasets into the project's DB.

Datasets used:
    - "Stock Market Dataset" by Oleh Onyschak
"""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from WebProject.models import Asset

from datetime import date
from io import BytesIO
from sys import stderr
from typing import Callable
from zipfile import ZipFile

import polars as pl
import requests
from dotenv import load_dotenv

load_dotenv()

STOCK_DATASET = "https://www.kaggle.com/api/v1/datasets/download/jacksoncrow/stock-market-dataset"


# Data export interval.
INTERVAL_START = date(2000, 1, 1)
INTERVAL_END = date(2020, 12, 31)

# Export N top stocks/ETFs from the data.
TOP_K = 100


def parse_meta_df(df: pl.DataFrame, zip: ZipFile) -> tuple[pl.DataFrame, dict[str, pl.DataFrame]]:
    # Only keep Symbol, Security name and ETF flag.
    df = df.select(pl.col('NASDAQ Symbol').alias('symbol'), pl.col('Security Name').alias('name'),
                   (pl.col('ETF') == 'Y').alias('etf'))

    # Time travel: Shift all market data to the current time.
    time_shift = date.today() - INTERVAL_START

    # Parse data for each stock.
    stock_data = {}
    mean_volume = {}

    for symbol, _, etf in df.iter_rows():
        path = f'etfs/{symbol}.csv' if etf else f'stocks/{symbol}.csv'
        with zip.open(path, 'r') as f:
            # Parse security DataFrame
            sdf = pl.read_csv(f).filter(
                pl.col('Date').cast(pl.Date).is_between(INTERVAL_START, INTERVAL_END)
            ).select(
                pl.col('Close').alias('close'),
                pl.col('Date').cast(pl.Date).alias('date') + time_shift,
                pl.col('Volume')
            ).sort('date')
            stock_data[symbol] = sdf
            mean_volume[symbol] = sdf.drop_in_place('Volume').mean()

    # Order securities by mean volume over the interval.
    volume_df = pl.DataFrame(mean_volume).transpose(include_header=True, header_name='symbol',
                                                    column_names=['mean_volume'])

    df = df.join(volume_df, on='symbol').sort('mean_volume', descending=True).drop_nulls().group_by('etf', maintain_order=True).head(
        TOP_K)

    # Prune stock data of unwanted securities
    secs = set(df['symbol'])
    stock_data = {symbol: data for symbol, data in stock_data.items() if symbol in secs}

    return df, stock_data


def parse_meta(zip: ZipFile) -> tuple[pl.DataFrame, dict[str, pl.DataFrame]]:
    with zip.open('symbols_valid_meta.csv', 'r') as meta:
        return parse_meta_df(pl.read_csv(meta), zip)


def progress[T](msg: str, f: Callable[..., T], *args, **kwargs) -> T:
    print(f'{msg}...', file=stderr, end='')
    ret = f(*args, **kwargs)
    print('done!', file=stderr)
    return ret


def main():
    req = progress('Downloading dataset', lambda: requests.get(STOCK_DATASET).content)
    zip = ZipFile(BytesIO(req))
    print(f'Downloaded {len(zip.namelist())} files', file=stderr)

    s_symbols, s_data = progress('Processing files', lambda: parse_meta(zip))
    print(f'Exported {len(s_data)} securities!', file=stderr)

    for etf, symbol, name, *_ in s_symbols.iter_rows():
        Asset.objects.create(type='ETF' if etf else 'STOCK', symbol=symbol, name=name)

if __name__ == "__main__":
    main()
