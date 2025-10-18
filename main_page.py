from sidebar import sidebar
import streamlit as st


def main_page(users):
    st.session_state["user_data"] = users[st.session_state['current_user']]

    sidebar()

    st.title("🏠 卡路里冒险团 主界面")
    st.markdown("### 👋 欢迎回来，今天继续保持好状态！")
    st.write('''
今天你的总热量差为 +200 kcal，略高于目标缺口 500 kcal。这说明今天的整体能量控制略显不足，可能是餐食中含糖或油脂类食物偏多。
从趋势上看，你已经连续保持了良好的运动习惯，运动消耗依然不错 👍。建议明天适当调整晚餐比例，增加一些高蛋白低脂的食物（如鸡胸肉、豆腐、蔬菜），同时减少碳水和高热量零食。
若明天能保持合理的热量摄入并完成运动任务，将重新进入稳定的减脂节奏。记得保证充足睡眠和水分摄入，避免熬夜导致代谢下降！(Demo Only)
    ''')
    st.markdown("---")

    date_str = st.session_state["simulated_date"].isoformat()
    records = st.session_state["user_data"]["records"].get(date_str,[])
    sport_consumption = 0
    food_intake = 0
    base_consumption = st.session_state['user_data']['user_info']['base_consumption']
    for item in records:
        if item["calorie"] < 0:
            sport_consumption += item["calorie"]
        else:
            food_intake += item["calorie"]
    surplus = food_intake + sport_consumption - base_consumption

    st.write(f"今日热量缺口目标：{st.session_state["user_data"]['target'].get('daily_calorie_deficit', 0)} kcal")
    st.write(f"今日饮食摄入：{food_intake} kcal")
    st.write(f"今日运动消耗：{sport_consumption} kcal")
    st.write(f"每日基础代谢：{-1 * base_consumption} kcal")
    if surplus > 0:
        st.write(f"今日热量盈余：{surplus} kcal")
    else:
        st.write(f"今日热量亏空：{-1 * surplus} kcal")

    if surplus > -1 * st.session_state["user_data"]['target']['daily_calorie_deficit']:
        st.warning("⚠️ 今日热量摄入超标！做些运动吧！")
    else:
        st.success("✅ 今日热量盈亏符合计划")

    if st.button("饮食/运动记录"):
        st.session_state["page"] = "record"
        st.rerun()
    if st.button("数据统计"):
        st.session_state["page"] = "statistics"
        st.rerun()
    if st.button("个人资料"):
        st.session_state["page"] = "profile"
        st.rerun()