import streamlit as st
from sidebar import sidebar


def profile_page(users):
    sidebar()
    if st.button("返回"):
        st.session_state["page"] = "main"
        st.rerun()

    st.title("📅 我")

    user = users[st.session_state["current_user"]]

    age = st.number_input("年龄", 10, 100, user["user_info"]["age"])
    st.radio("性别", ["男", "女"], disabled=True)
    weight = st.number_input("当前体重 (kg)", 30.0, 200.0, user["user_info"]["weight"])
    height = st.number_input("身高 (cm)", 100.0, 220.0, user["user_info"]["height"])
    goal_weight = st.number_input("目标体重 (kg)", 30.0, 200.0, user["target"]["goal_weight"])
    goal_time = st.number_input("周", 4, 48, user["target"]["goal_time"])
    st.selectbox("活动水平", ["久坐", "轻度活动", "中等活动", "高强度活动"])

    if st.button("✨ 保存并更新"):
        users[st.session_state["current_user"]]["user_info"]["age"] = age
        users[st.session_state["current_user"]]["user_info"]["weight"] = weight
        users[st.session_state["current_user"]]["user_info"]["height"] = height
        users[st.session_state["current_user"]]["target"]["goal_weight"] = goal_weight
        users[st.session_state["current_user"]]["target"]["goal_time"] = goal_time

        st.session_state["page"] = "main"
        st.rerun()

    # st.write(users[st.session_state["current_user"]])
