import streamlit as st
import pymysql
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@st.cache_resource
def connect_db():
    return pymysql.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="4V44XYoMA7okY9v.root",
        password="IPDxDlc6fXH0d2G0",
        database="mymdb",
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )