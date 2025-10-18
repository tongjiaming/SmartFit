import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------
# Streamlit 页面配置
# -----------------------------
st.set_page_config(page_title="FitMind", page_icon="💪", layout="wide")
st.title("🏋️ AI减脂助手-Demo")

# -----------------------------
# 初始化状态
# -----------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = False

if "user_info" not in st.session_state:
    st.session_state.user_info = {}

if "records" not in st.session_state:
    st.session_state.records = []

# -----------------------------
# 首次引导页
# -----------------------------
def show_onboarding():
    st.subheader("👋 欢迎来到 FitMind！先设置你的个人信息和减脂目标")
    with st.form("onboarding_form"):
        name = st.text_input("你的名字")
        gender = st.selectbox("性别", ["男", "女"])
        age = st.number_input("年龄", 10, 100)
        height = st.number_input("身高 (cm)", 100, 250)
        weight = st.number_input("当前体重 (kg)", 30.0, 200.0)
        activity = st.selectbox("活动水平", ["久坐", "轻度活动", "中等活动", "高强度活动"])
        target_weight = st.number_input("目标体重 (kg)", 30.0, 200.0)
        deadline = st.date_input("希望达成的日期", value=date.today())

        submitted = st.form_submit_button("✅ 开始我的减脂计划！")
        if submitted:
            # 保存信息
            st.session_state.initialized = True
            st.session_state.user_info = {
                "name": name,
                "gender": gender,
                "age": age,
                "height": height,
                "weight": weight,
                "activity": activity,
                "target_weight": target_weight,
                "deadline": str(deadline)
            }
            st.success("信息已保存！")
            # 直接显示主界面
            show_main_interface()

# -----------------------------
# 主界面
# -----------------------------
def show_main_interface():
    user = st.session_state.user_info
    st.sidebar.success(f"欢迎回来，{user['name']} 💪")
    tab = st.sidebar.radio("功能导航", [
        "📖 饮食记录",
        "🏃 运动记录",
        "🍽️ AI推荐",
        "📅 每日打卡"
    ])

    # ===== 计算每日热量目标 =====
    BMR = 10*user["weight"] + 6.25*user["height"] - 5*user["age"] + (5 if user["gender"]=="男" else -161)
    activity_factor = {"久坐":1.2,"轻度活动":1.375,"中等活动":1.55,"高强度活动":1.725}
    TDEE = BMR * activity_factor[user["activity"]]

    total_deficit = (user["weight"] - user["target_weight"]) * 7700
    days_left = max((pd.to_datetime(user["deadline"]) - pd.Timestamp.today()).days,1)
    daily_deficit = total_deficit / days_left
    daily_target_cal = TDEE - daily_deficit

    # ==========================
    # 饮食记录
    # ==========================
    if tab == "📖 饮食记录":
        st.header("🍎 今日饮食记录")
        with st.form("diet_form"):
            calories_eaten = st.number_input("今日摄入热量（kcal）", 0, 10000, 2000)
            submitted = st.form_submit_button("💾 保存今日饮食记录")
            if submitted:
                st.session_state.records.append({
                    "日期": date.today(),
                    "类型": "饮食",
                    "摄入": calories_eaten,
                    "消耗": 0
                })
                st.success("✅ 今日饮食记录已保存")

    # ==========================
    # 运动记录
    # ==========================
    elif tab == "🏃 运动记录":
        st.header("🏋️ 今日运动记录")
        with st.form("exercise_form"):
            calories_burned = st.number_input("今日运动消耗热量（kcal）", 0, 2000, 300)
            submitted = st.form_submit_button("💾 保存今日运动记录")
            if submitted:
                st.session_state.records.append({
                    "日期": date.today(),
                    "类型": "运动",
                    "摄入": 0,
                    "消耗": calories_burned
                })
                st.success("✅ 今日运动记录已保存")

    # ==========================
    # AI推荐（写死内容替代）
    # ==========================
    elif tab == "🍽️ AI推荐":
        st.header("💡 今日饮食/运动建议（示例）")
        if st.button("✨ 生成今日建议"):
            # 写死示例数据
            advice = """
**饮食建议**：多摄入蔬菜和高蛋白食物，控制碳水摄入在50克以内。  
**运动推荐**：快走30分钟+哑铃力量训练20分钟。  
**激励语**：坚持就是胜利，你离目标越来越近！💪
"""
            st.success("✅ 建议生成成功！")
            st.markdown(advice)

    # ==========================
    # 每日打卡
    # ==========================
    elif tab == "📅 每日打卡":
        st.header("📊 今日热量达标情况")

        today_records = [r for r in st.session_state.records if r["日期"]==date.today()]
        calories_eaten = sum([r["摄入"] for r in today_records])
        calories_burned = sum([r["消耗"] for r in today_records])
        net_cal = calories_eaten - calories_burned

        st.metric("今日净热量目标", f"{daily_target_cal:.0f} kcal")
        st.metric("今日净热量实际", f"{net_cal:.0f} kcal")

        if net_cal <= daily_target_cal:
            st.success(f"🎉 今日达标！净热量: {net_cal:.0f} kcal ✅")
        else:
            st.warning(f"⚠️ 今日未达标！净热量: {net_cal:.0f} kcal ❌")

        # 折线图显示净热量 vs 目标
        if st.session_state.records:
            df = pd.DataFrame(st.session_state.records)
            df_agg = df.groupby("日期").agg({"摄入":"sum","消耗":"sum"}).reset_index()
            df_agg["净热量"] = df_agg["摄入"] - df_agg["消耗"]
            df_agg["目标"] = daily_target_cal
            st.line_chart(df_agg.set_index("日期")[["净热量","目标"]])

# -----------------------------
# 主流程
# -----------------------------
if not st.session_state.initialized:
    show_onboarding()
else:
    show_main_interface()
