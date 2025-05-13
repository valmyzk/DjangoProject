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
from sys import stderr

import polars as pl
import yfinance as yf

# Data export interval.
INTERVAL_START = date(2000, 1, 1)
INTERVAL_END = date(2020, 12, 31)

# Export N top stocks/ETFs from the data.
TOP_K = 100

NASDAQ100_DATA = "http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt"

def parse_nasdaq() -> tuple[pl.DataFrame, dict[str, pl.DataFrame]]:
    # Download NASDAQ-exchanged securities.
    nasdaq = pl.read_csv(NASDAQ100_DATA, separator='|').filter(pl.col('Test Issue') == 'N').select(
        pl.col('NASDAQ Symbol').alias('symbol'), pl.col('Security Name').alias('name'),
        (pl.col('ETF') == 'Y').alias('etf'))

    # Time travel: Shift all market data to the current time.
    time_shift = date.today() - INTERVAL_START

    # Parse data for each stock.
    stock_data = {}
    mean_volume = {}

    for symbol in nasdaq['symbol']:
        # Convert to polars DataFrame.
        pd = yf.download(symbol, period='max')
        pd.columns = pd.columns.droplevel(level=1)

        # Parse historical data
        sdf = pl.from_pandas(pd, include_index=True).filter(
            pl.col('Date').cast(pl.Date).is_between(INTERVAL_START, INTERVAL_END)
        ).select(
            pl.col('Date').cast(pl.Date).alias('date') + time_shift,
            pl.col('Close').alias('close'),
            pl.col('Volume')
        ).sort('date')
        stock_data[symbol] = sdf
        mean_volume[symbol] = sdf.drop_in_place('Volume').mean()

    # Order securities by mean volume over the interval.
    volume_df = pl.DataFrame(mean_volume).transpose(include_header=True, header_name='symbol',
                                                    column_names=['mean_volume']).drop_nulls()

    df = nasdaq.join(volume_df, on='symbol').sort('mean_volume', descending=True).group_by('etf',
                                                                                           maintain_order=True).head(
        TOP_K)

    # Prune stock data of unwanted securities
    secs = set(df['symbol'])
    stock_data = {symbol: data for symbol, data in stock_data.items() if symbol in secs}

    return df.drop_nulls(), stock_data

def main():
    print(f'Parsing NASDAQ100 data...', end='', file=stderr)
    s_symbols, s_data = parse_nasdaq()
    print('done!', file=stderr)

    for etf, symbol, *_ in s_symbols.iter_rows():
        Asset.objects.create(type='ETF' if etf else 'STOCK', symbol=symbol)


if __name__ == "__main__":
    main()
