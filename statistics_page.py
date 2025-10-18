import pandas as pd
import streamlit as st
from sidebar import sidebar
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def statistics_page(data_file, users):
    st.title("数据统计")

    sidebar()
    if st.button("返回"):
        st.session_state["page"] = "main"
        st.rerun()

    st.write('''
这个月你的健康管理总体表现出色！
在过去的 30 天中，你保持了 良好的饮食纪律 和 较高的运动频率，平均每日热量摄入与目标缺口接近理想值。体重趋势稳定下降，说明你的计划正在有效发挥作用。
特别值得肯定的是，你在工作日的作息与运动执行度都明显提升，这让代谢效率保持在较高水平。不过，周末的饮食波动略大，可能会轻微影响整体进度。
建议你在接下来的一周中，继续保持平日的节奏，同时为周末制定简单的餐饮计划，避免“放松过头”。
按照目前的状态推算，你将在下月达到 阶段性目标 —— 更健康、更轻盈的自己，继续加油！💪 (Demo Only)
    ''')
    st.markdown("---")

    user = users[st.session_state["current_user"]]
    today = st.session_state["simulated_date"]
    start_date = today - datetime.timedelta(days=29)
    dates = [start_date + datetime.timedelta(days=i) for i in range(30)]
    date_strs = [d.isoformat() for d in dates]

    diet_list = []
    exercise_list = []
    diff_list = []
    target_list = []
    has_data_list = []

    daily_target = user["target"]["daily_calorie_deficit"]
    base_consumption = user["user_info"]["base_consumption"]

    for d in date_strs:
        records = user["records"].get(d, [])
        has_data = len(records) > 0
        diet_cal = sum(r["calorie"] for r in records if r["calorie"] > 0)
        exercise_cal = -sum(r["calorie"] for r in records if r["calorie"] < 0)
        diff = base_consumption + exercise_cal - diet_cal if has_data else None
        diet_list.append(diet_cal)
        exercise_list.append(exercise_cal)
        diff_list.append(diff)
        target_list.append(diff >= daily_target if has_data else None)
        has_data_list.append(has_data)

    df = pd.DataFrame({
        "日期": date_strs,
        "饮食摄入": diet_list,
        "运动消耗": exercise_list,
        "热量差": diff_list,
        "目标达成": target_list,
        "has_data": has_data_list
    })

    streak = []
    count = 0
    for reached in df["目标达成"]:
        if reached:
            count += 1
        else:
            count = 0
        streak.append(count)
    df["连续达成天数"] = streak

    diet_y = [val if has else None for val, has in zip(diet_list, has_data_list)]
    exercise_y = [val if has else None for val, has in zip(exercise_list, has_data_list)]
    diff_y = [val if has else None for val, has in zip(diff_list, has_data_list)]
    streak_y = [val if has else None for val, has in zip(streak, has_data_list)]

    fig = make_subplots(rows=2, cols=2, subplot_titles=("🍽️ 饮食摄入", "🏃 运动消耗", "🔥 热量差", "📅 目标达成streak"))

    # 饮食摄入折线图
    fig.add_trace(go.Scatter(
        x=date_strs,
        y=diet_y,
        mode="lines+markers",
        line=dict(color="blue"),
        name="饮食摄入"
    ), row=1, col=1)
    fig.update_yaxes(title_text="kcal", row=1, col=1, range=[500, max(df["饮食摄入"].max() or 2000, 2000)])

    # 运动消耗折线图
    fig.add_trace(go.Scatter(
        x=date_strs,
        y=exercise_y,
        mode="lines+markers",
        line=dict(color="green"),
        name="运动消耗"
    ), row=1, col=2)
    fig.update_yaxes(title_text="kcal", row=1, col=2, range=[0, max(df["运动消耗"].max() or 1000, 1000)])

    # 热量差折线图
    fig.add_trace(go.Scatter(
        x=date_strs,
        y=diff_y,
        mode="lines+markers",
        line=dict(color="orange"),
        name="热量差"
    ), row=2, col=1)
    fig.update_yaxes(title_text="kcal", row=2, col=1, range=[min(df["热量差"].min() or -1000, -1000), max(df["热量差"].max() or 1000, 1000)])
    # 添加横虚线表示每日热量缺口目标
    daily_target = user["target"]["daily_calorie_deficit"]
    fig.add_hline(
        y=daily_target,
        line_dash="dash",  # 虚线
        line_color="grey",
        row=2,
        col=1,
        annotation_text=f"目标: {daily_target} kcal",
        annotation_position="top left",
        annotation_font_color="grey"
    )

    # 日历散点图
    fig.add_trace(go.Scatter(
        x=date_strs,
        y=streak_y,
        mode="lines+markers",
        line=dict(color="red"),
        name="目标达成streak"
    ), row=2, col=2)
    fig.update_yaxes(title_text="天数", row=2, col=2, range=[0, max(df["连续达成天数"].max() or 0, 10)])
    fig.update_layout(height=800, width=1000, title_text="📊 用户近30天统计", showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
