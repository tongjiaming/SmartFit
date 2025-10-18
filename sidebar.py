import streamlit as st
import datetime


def sidebar():
    st.sidebar.title(f"👤 当前用户：{st.session_state['current_user']}")
    st.sidebar.divider()

    if "simulated_date" not in st.session_state:
        st.session_state["simulated_date"] = datetime.date.today()
    st.sidebar.date_input(
        "调试用：选择系统日期",
        value=st.session_state["simulated_date"],
        key="date_selector",
        on_change=lambda: st.session_state.update({"simulated_date": st.session_state["date_selector"]})
    )
    st.sidebar.divider()

    if st.sidebar.button("🚪 退出登录"):
        st.session_state.clear()
        st.rerun()