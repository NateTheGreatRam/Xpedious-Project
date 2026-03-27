"""
app.py — Xpedious Entry Point
Run: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Xpedious",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.theme   import inject_theme
from components.sidebar import render_sidebar
from core.state         import init_state, get_page

import pages.dashboard as dashboard
import pages.new_order as new_order
import pages.orders    as orders_page
import pages.billing   as billing
import pages.analytics as analytics

init_state()
inject_theme()
render_sidebar()

page = get_page()

if page == "dashboard":
    dashboard.render()
elif page == "new_order":
    new_order.render()
elif page == "orders":
    orders_page.render()
elif page == "billing":
    billing.render()
elif page == "analytics":
    analytics.render()
else:
    dashboard.render()
