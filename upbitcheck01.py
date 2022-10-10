import pyupbit
import time
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objs as go

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
    st.plotly_chart(fig)



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
st.subheader(f"{selected_coin} {intervalTime}")
st.dataframe(coin_data.tail())
draw_chart(coin_data)
draw_chart_plotly(coin_data)
