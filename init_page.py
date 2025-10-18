import time

import streamlit as st
from save_user_data import save_user_data
# from llm import set_goal
from llm import set_goal_demo


def init_page(data_file, users):
    st.title("👋 欢迎来到 FitMind！")
    st.write(f"{st.session_state["current_user"]}，让我们一起定制你的健康减脂计划 💪")

    age = st.number_input("年龄", 10, 100, 25)
    gender = st.radio("性别", ["男", "女"])
    weight = st.number_input("当前体重 (kg)", 30.0, 200.0, 70.0)
    height = st.number_input("身高 (cm)", 100.0, 220.0, 170.0)
    goal_weight = st.number_input("目标体重 (kg)", 30.0, 200.0, 65.0)
    goal_time = st.number_input("周", 4, 48, 24)
    activity = st.selectbox("活动水平", ["久坐", "轻度活动", "中等活动", "高强度活动"])

    if st.button("✨ 生成我的计划"):
        # base_consumption, target_deficit, report = set_goal(age, gender, weight, height, activity, goal_time, goal_weight)
        base_consumption, target_deficit, report = set_goal_demo(age, gender, weight, height, activity, goal_time, goal_weight)

        users[st.session_state["current_user"]] = {
            "setup_done": True,
            "user_info": {
                "age": age,
                "gender": gender,
                "weight": weight,
                "height": height,
                "activity": activity,
                "base_consumption": base_consumption,
            },
            "target": {
                "goal_weight": goal_weight,
                "goal_time": goal_time,
                "daily_calorie_deficit": target_deficit,
                "total_calorie_deficit": target_deficit * goal_time * 7,
                "report": report,
            },
            "records": {
            }
        }
        save_user_data(data_file, users)
        st.session_state["setup_done"] = True

        st.markdown("### ⏳ 加载中...")

        progress_bar = st.progress(0)
        status_text = st.empty()

        for percent in range(101):
            progress_bar.progress(percent)
            status_text.text(f"进度：{percent}%")
            time.sleep(0.01)  # 100 × 0.01s = 1秒

        st.write(report)
        if st.button("✨ Get Started"):
            st.rerun()