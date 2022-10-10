import pyupbit
import time
import streamlit as st

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


