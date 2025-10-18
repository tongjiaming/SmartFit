import streamlit as st
import json
from sidebar import sidebar
import datetime


def save_data(data_file, data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_page(data_file, users):
    sidebar()
    if st.button("⬅️ 返回"):
        st.session_state["page"] = "main"
        st.rerun()

    st.title("🍽️ 饮食/运动记录")
    st.write("记录你的饮食摄入 / 运动消耗（单位 kcal）")

    username = st.session_state["current_user"]
    user = users[username]
    date_str = st.session_state["simulated_date"].isoformat()

    if date_str not in user["records"]:
        user["records"][date_str] = []

    records = user["records"][date_str]


    with st.form("add_record_form"):
        name = st.text_input("项目名称")
        calorie = st.number_input("卡路里增/减 (kcal)", -5000, 5000, 0)
        submitted = st.form_submit_button("➕ 添加记录")
        if submitted:
            if name.strip() == "":
                st.warning("请输入项目名称")
            else:
                records.append({"name": name, "calorie": calorie})
                save_data(data_file, users)
                st.success(f"已添加记录：{name} ({calorie} kcal)")
                st.rerun()

    # demo only
    st.markdown("### 💬 饮食/运动记录(Demo Only)")
    user_input = st.text_area(
        "chat_input",
        placeholder="又吃了什么或是运动了...?",
        height=100,
        label_visibility="collapsed",
        key="chat_input",
    )

    st.subheader(f"📋 {date_str} 的记录")
    if not records:
        st.info("暂无记录，请添加。")
    else:
        for i, r in enumerate(records):
            col1, col2, col3 = st.columns([4, 2, 1])
            col1.write(r["name"])
            col2.write(f"{r['calorie']} kcal")
            if col3.button("🗑️ 删除", key=f"del_{i}"):
                records.pop(i)
                save_data(data_file, users)
                st.warning("记录已删除 ❌")
                st.rerun()
