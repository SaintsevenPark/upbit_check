import pyupbit
import time
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import mplfinance as mpf
import numpy as np
import ss_ta as sta

st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon="",
    layout="wide"
)


@st.cache
def get_coin_list():
    rtn_coin_list = pyupbit.get_tickers(fiat="KRW")
    return rtn_coin_list


@st.cache
def get_coin_data(coin_name, coin_interval):
    rtn_ticker, rtn_interval, rtn_df = sta.getDf_name(coin_name, coin_interval)
    return rtn_df


def draw_chart(df):
    plt.figure(figsize=(20, 5))

    width = 0.035
    width2 = 0.001

    up = df[df.close >= df.open]
    down = df[df.close < df.open]

    col1 = 'red'
    col2 = 'blue'

    plt.bar(up.index, up.close - up.open, width, bottom=up.open, color=col1)
    plt.bar(up.index, up.high - up.close, width2, bottom=up.close, color=col1)
    plt.bar(up.index, up.low - up.open, width2, bottom=up.open, color=col1)

    plt.bar(down.index, down.close - down.open, width, bottom=down.open, color=col2)
    plt.bar(down.index, down.high - down.open, width2, bottom=down.open, color=col2)
    plt.bar(down.index, down.low - down.close, width2, bottom=down.close, color=col2)

    # rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')

    st.pyplot(plt)


def draw_chart_plotly(df):
    candle = go.Candlestick(x=df.index)
    candle = go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'])
    fig = go.Figure(data=candle)
    fig.update_layout(xaxis_autorange=True, yaxis_autorange=True, autosize=True,
                      margin=dict(l=10, r=10, b=50, t=50, pad=1),
                      )
    st.plotly_chart(fig)


def draw_chart_mpl_finance(df):
    # --------------------- 잔선 ----------------------
    st1 = np.where(
        (df['ma5'] > df['ma5'].shift(1))
        & (df['ma5'].shift(1) < df['ma5'].shift(2))
        & (df['ma5'].shift(2) < df['ma5'].shift(3))
        & (df['ma5'] < df['ma20'])
        & (df['ma5'].shift(1) < df['ma20'].shift(1))
        # & (df['mfi'] > df['mfi'].shift(1))
        # & (df['mfi'].shift(1) > df['mfi'].shift(2))
        , 1,
        np.nan
    ) * df['close'] * 1.005

    # cci가 -100을 우상향 돌파할때
    st2 = np.where(
        (df['CCI'] > df['CCI'].shift(1))
        & (df['CCI'].shift(1) > df['CCI'].shift(2))
        # & (df['cci'].shift(2) > df['cci'].shift(3))
        & (df['CCI'] > -100)
        & (df['CCI'].shift(1) < -100)
        , 1,
        np.nan
    ) * df['close'] * 1.005

    # ----------------- 시각화 시작-----------------
    adps = []
    # --------------이동평균선
    adps.append(mpf.make_addplot(df['ma20'], panel=0, type='line', width=0.2, color='b'))
    adps.append(mpf.make_addplot(df['ma5'], panel=0, type='line', width=1.5, color='r'))
    # -------------------MFI
    adps.append(
        mpf.make_addplot(df['MFI14'], panel=1, type='line', width=0.7, ylabel='MFI', color='r'))
    adps.append(
        mpf.make_addplot(np.ones((len(df))) * 20, panel=1, type='line', color='blue', linestyle='dotted',
                         secondary_y=False, width=1))
    adps.append(
        mpf.make_addplot(np.ones((len(df))) * 80, panel=1, type='line', color='blue', linestyle='dotted',
                         secondary_y=False, width=1))

    # -------------------CCI
    adps.append(
        mpf.make_addplot(df['CCI'], panel=2, type='line', width=0.7, ylabel='CCI', color='b'))
    adps.append(
        mpf.make_addplot(np.ones((len(df))) * -100, panel=2, type='line', color='red', linestyle='dotted',
                         secondary_y=False, width=1))
    adps.append(
        mpf.make_addplot(np.ones((len(df))) * 100, panel=2, type='line', color='red', linestyle='dotted',
                         secondary_y=False, width=1))
    # ---------------- 마킹 시작 ---------------------
    adps.append(mpf.make_addplot(st1, scatter=True, markersize=150, marker=r'$\Downarrow$', color='red'))
    adps.append(mpf.make_addplot(st2, scatter=True, markersize=100, marker=r'$\Downarrow$', color='blue'))
    # adps.append(mpf.make_addplot(test, scatter=True, markersize=100, marker='$9$', color='blue'))   #숫자로 할때

    # ---------------- 시각화 시작 ---------------------
    fig, axs = mpf.plot(df,
                        type='candle',
                        tight_layout=True,
                        style='charles',
                        # style='yahoo',
                        figratio=(3.5, 1),
                        figscale=1,
                        # volume=True,
                        addplot=adps,
                        returnfig=True
                        )
    axs[0].set_xlabel('Date')
    axs[0].legend(['MA20', 'MA5'])
    # axs[0].set_title(f"{ticker} -- {interval} -- ( {df['close'][-1]} ) Won")
    axs[2].legend(['MFI'])
    axs[4].legend(['CCI'])

    st.pyplot(fig)


def coin_check(interval_time):
    st.markdown("#### 업비트 코인 체크")
    numbers = st.empty()
    with numbers.container():
        for i in get_coin_list():
            st.write(f"{i} : {interval_time}")
            ticker, interval, df = sta.getDf_name(i, interval_time)
            st.dataframe(df.tail(1))
            time.sleep(0.5)


coin_list = get_coin_list()
coin_number = st.sidebar.number_input('코인넘버', min_value=0, max_value=len(coin_list), step=1)
selected_coin = st.sidebar.selectbox('코인넘버', coin_list, index=coin_number)
intervalTime = st.sidebar.selectbox('기간 선택', ('minute5', 'minute10', 'minute15', 'minute30', 'minute60', 'D'))
strategy = st.sidebar.selectbox('전략 선택',
                                ('단순이평선교차',
                                 'RSI'))

if st.sidebar.button("시작", disabled=True):
    coin_check(interval_time=intervalTime)

coin_data = get_coin_data(selected_coin, intervalTime)
st.subheader(f"{selected_coin}---{intervalTime}---{coin_data[-1:]['close']}")
st.dataframe(coin_data.tail())

# draw_chart(coin_data)
# draw_chart_plotly(coin_data)
draw_chart_mpl_finance(df=coin_data)
