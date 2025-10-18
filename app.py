import streamlit as st
import json
from login_page import login_page
from init_page import init_page
from main_page import main_page
from record_page import record_page
from statistics_page import statistics_page
from profile_page import profile_page


def page_router():
    if "current_user" not in st.session_state:
        login_page(DATA_FILE, USERS)
    elif not st.session_state["setup_done"]:
        init_page(DATA_FILE, USERS)
    elif st.session_state["page"] == "main":
        main_page(USERS)
    elif st.session_state["page"] == "record":
        record_page(DATA_FILE, USERS)
    elif st.session_state["page"] == "statistics":
        statistics_page(DATA_FILE, USERS)
    elif st.session_state["page"] == "profile":
        profile_page(USERS)
    else:
        main_page(USERS)


if __name__ == "__main__":
    DATA_FILE = "user_data.json"
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        USERS = json.load(f)

    if "page" not in st.session_state:
        st.session_state["page"] = "main"

    page_router()
