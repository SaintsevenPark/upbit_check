import pyupbit
import time
import streamlit as st

import ss_ta as sta

st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon="",
    layout="wide"
)

coin_list = pyupbit.get_tickers(fiat="KRW")


def coin_check(intervaltime, strategy):
    st.markdown("#### 업비트 코인 체크")
    numbers = st.empty()
    with numbers.container():
        for i in coin_list:
            st.write(f"{i} : {intervaltime}")
            ticker, interval, df = sta.getDf_name(i, intervaltime)
            st.dataframe(df.tail(1))
            time.sleep(0.5)


intervalTime = st.selectbox('기간 선택', ('minute5', 'minute10', 'minute15', 'minute30', 'minute60', 'D'))
strategy = st.selectbox('전략 선택',
                        ('단순이평선교차',
                         'RSI'))
if st.button("시작"):
    coin_check(intervaltime=intervalTime, strategy=strategy)
