import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import pyupbit

def getDf_name(tick, interval):
    df = pyupbit.get_ohlcv(tick, interval=interval)

    # 볼린저 밴드 및 이동평균선
    df['ma5'] = df['close'].rolling(window=5).mean()  # 5일 이동평균
    df['ma10'] = df['close'].rolling(window=10).mean()  # 5일 이동평균
    df['ma20'] = df['close'].rolling(window=20).mean()  # 20일 이동평균
    df['ma60'] = df['close'].rolling(window=60).mean()  # 20일 이동평균
    df['ma120'] = df['close'].rolling(window=120).mean()  # 5일 이동평균
    df['stddev'] = df['close'].rolling(window=20).std()  # 20일 이동평균치
    df['bbupper'] = df['ma20'] + 2 * df['stddev']
    df['bblower'] = df['ma20'] - 2 * df['stddev']

    # MACD
    df['ma12'] = df['close'].rolling(window=12).mean()  # 12일 이동평균
    df['ma26'] = df['close'].rolling(window=26).mean()  # 26일 이동평균
    df['MACD'] = df['ma12'] - df['ma26']  # MACD
    df['MACD_Signal'] = df['MACD'].rolling(window=9).mean()  # MACD Signal(MACD 9일 이동평균)
    df['MACD_Oscil'] = df['MACD'] - df['MACD_Signal']  # MACD 오실레이터

    # Stochastic
    df['ndays_high'] = df['high'].rolling(window=14, min_periods=1).max()  # 14일 중 최고가
    df['ndays_low'] = df['low'].rolling(window=14, min_periods=1).min()  # 14일 중 최저가
    df['fast_k'] = (df['close'] - df['ndays_low']) / (df['ndays_high'] - df['ndays_low']) * 100  # Fast %K 구하기
    df['slow_d'] = df['fast_k'].rolling(window=3).mean()  # Slow %D 구하기

    # MFI
    df['PB'] = (df['close'] - df['bblower']) / (df['bbupper'] - df['bblower'])
    df['TP'] = (df['high'] + df['low'] + df['close']) / 3
    df['PMF'] = 0
    df['NMF'] = 0
    for i in range(len(df.close) - 1):
        if df.TP.values[i] < df.TP.values[i + 1]:
            df.PMF.values[i + 1] = df.TP.values[i + 1] * df.volume.values[i + 1]
            df.NMF.values[i + 1] = 0
        else:
            df.NMF.values[i + 1] = df.TP.values[i + 1] * df.volume.values[i + 1]
            df.PMF.values[i + 1] = 0
    df['MFR'] = (df.PMF.rolling(window=14).sum() /
                 df.NMF.rolling(window=14).sum())
    df['MFI14'] = 100 - 100 / (1 + df['MFR'])

    # IIP
    df['II'] = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    df['IIP21'] = df['II'].rolling(window=21).sum() / df['volume'].rolling(window=21).sum() * 100

    # RSI
    U = np.where(df['close'].diff(1) > 0, df['close'].diff(1), 0)
    D = np.where(df['close'].diff(1) < 0, df['close'].diff(1) * (-1), 0)
    AU = pd.DataFrame(U, index=df.index).rolling(window=14).mean()
    AD = pd.DataFrame(D, index=df.index).rolling(window=14).mean()
    RSI = AU / (AD + AU) * 100
    df['RSI'] = RSI

    # CCI
    pt = (df['high'] + df['low'] + df['close']) / 3
    sma = pt.rolling(14).mean()
    mad = pt.rolling(14).apply(lambda x: pd.Series(x).mad())
    df['CCI'] = (pt - sma) / (0.015 * mad)

    return (tick, interval, df)


def getDf(tick, interval):
    tickers = pyupbit.get_tickers(fiat='KRW')
    # flow 97번째
    ticker = tickers[tick]
    # interval = 'minute60'

    df = pyupbit.get_ohlcv(ticker, interval=interval)

    # 볼린저 밴드 및 이동평균선
    df['ma5'] = df['close'].rolling(window=5).mean()  # 5일 이동평균
    df['ma10'] = df['close'].rolling(window=10).mean()  # 5일 이동평균
    df['ma20'] = df['close'].rolling(window=20).mean()  # 20일 이동평균
    df['ma60'] = df['close'].rolling(window=60).mean()  # 20일 이동평균
    df['ma120'] = df['close'].rolling(window=120).mean()  # 5일 이동평균
    df['stddev'] = df['close'].rolling(window=20).std()  # 20일 이동평균치
    df['bbupper'] = df['ma20'] + 2 * df['stddev']
    df['bblower'] = df['ma20'] - 2 * df['stddev']

    # MACD
    df['ma12'] = df['close'].rolling(window=12).mean()  # 12일 이동평균
    df['ma26'] = df['close'].rolling(window=26).mean()  # 26일 이동평균
    df['MACD'] = df['ma12'] - df['ma26']  # MACD
    df['MACD_Signal'] = df['MACD'].rolling(window=9).mean()  # MACD Signal(MACD 9일 이동평균)
    df['MACD_Oscil'] = df['MACD'] - df['MACD_Signal']  # MACD 오실레이터

    # Stochastic
    df['ndays_high'] = df['high'].rolling(window=14, min_periods=1).max()  # 14일 중 최고가
    df['ndays_low'] = df['low'].rolling(window=14, min_periods=1).min()  # 14일 중 최저가
    df['fast_k'] = (df['close'] - df['ndays_low']) / (df['ndays_high'] - df['ndays_low']) * 100  # Fast %K 구하기
    df['slow_d'] = df['fast_k'].rolling(window=3).mean()  # Slow %D 구하기

    # MFI
    df['PB'] = (df['close'] - df['bblower']) / (df['bbupper'] - df['bblower'])
    df['TP'] = (df['high'] + df['low'] + df['close']) / 3
    df['PMF'] = 0
    df['NMF'] = 0
    for i in range(len(df.close) - 1):
        if df.TP.values[i] < df.TP.values[i + 1]:
            df.PMF.values[i + 1] = df.TP.values[i + 1] * df.volume.values[i + 1]
            df.NMF.values[i + 1] = 0
        else:
            df.NMF.values[i + 1] = df.TP.values[i + 1] * df.volume.values[i + 1]
            df.PMF.values[i + 1] = 0
    df['MFR'] = (df.PMF.rolling(window=14).sum() /
                 df.NMF.rolling(window=14).sum())
    df['MFI14'] = 100 - 100 / (1 + df['MFR'])

    # IIP
    df['II'] = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    df['IIP21'] = df['II'].rolling(window=21).sum() / df['volume'].rolling(window=21).sum() * 100

    # RSI
    U = np.where(df['close'].diff(1) > 0, df['close'].diff(1), 0)
    D = np.where(df['close'].diff(1) < 0, df['close'].diff(1) * (-1), 0)
    AU = pd.DataFrame(U, index=df.index).rolling(window=14).mean()
    AD = pd.DataFrame(D, index=df.index).rolling(window=14).mean()
    RSI = AU / (AD + AU) * 100
    df['RSI'] = RSI

    # CCI
    pt = (df['high'] + df['low'] + df['close']) / 3
    sma = pt.rolling(14).mean()
    mad = pt.rolling(14).apply(lambda x: pd.Series(x).mad())
    df['CCI'] = (pt - sma) / (0.015 * mad)

    return (ticker, interval, df)
