import streamlit as st
from save_user_data import save_user_data


def login_page(data_file, users):
    st.title("🔐 卡路里冒险团 登录")

    username = st.text_input("请输入用户名：", key="login_name")
    if st.button("登录"):
        if username.strip() == "":
            st.warning("请输入有效的用户名")
            return

        st.session_state["current_user"] = username

        if username not in users:
            users[username] = {
                "setup_done": False,
                "user_info": {},
                "target": {}
            }
            save_user_data(data_file, users)
        st.session_state["setup_done"] = users[username]["setup_done"]
        st.rerun()