"""
components/theme.py — All CSS in one place.
"""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #060911 !important;
    color: #dde3f0 !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 70% 50% at 20% -5%,  #0a1f3d 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 80% 100%, #0d1a30 0%, transparent 60%),
        #060911 !important;
}

#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
header { background: transparent !important; }

[data-testid="stSidebar"] {
    background: #080b13 !important;
    border-right: 1px solid #131929 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebarContent"] { padding: 0 !important; }

.block-container { max-width: 1140px !important; padding: 36px 40px 100px !important; }

.sb-logo { padding: 26px 22px 18px; border-bottom: 1px solid #131929; margin-bottom: 6px; }
.sb-logo-mark { font-family: 'Syne', sans-serif; font-size: 21px; font-weight: 800; letter-spacing: -0.5px; color: #fff; }
.sb-logo-mark em { color: #3b82f6; font-style: normal; }
.sb-tagline { font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; color: #374151; margin-top: 3px; }
.sb-section { font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; color: #1f2d42; padding: 16px 22px 6px; }
.sb-stats { padding: 14px 22px; border-top: 1px solid #0d1422; }
.sb-stat-row { display: flex; justify-content: space-between; padding: 5px 0; font-size: 11px; }
.sb-stat-label { color: #2d3d52; }
.sb-stat-val { color: #8096b5; font-weight: 500; }

.page-hdr { margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid #0f1520; }
.page-eyebrow { font-size: 9px; letter-spacing: 3px; text-transform: uppercase; color: #3b82f6; margin-bottom: 8px; }
.page-title { font-family: 'Syne', sans-serif; font-size: 30px; font-weight: 800; color: #fff; letter-spacing: -0.8px; line-height: 1.1; }
.page-title em { color: #3b82f6; font-style: normal; }
.page-sub { margin-top: 6px; font-size: 11px; color: #374151; letter-spacing: 0.3px; }

.sec-label { font-size: 9px; letter-spacing: 3px; text-transform: uppercase; color: #3b82f6; margin: 28px 0 14px; font-weight: 500; display: flex; align-items: center; gap: 8px; }
.sec-label::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, #131929, transparent); }

.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
.stat-card { background: #0a0e18; border: 1px solid #131929; border-radius: 14px; padding: 18px 20px; position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, #3b82f620, transparent); }
.stat-icon { font-size: 18px; margin-bottom: 10px; }
.stat-val { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 800; color: #fff; letter-spacing: -0.8px; }
.stat-val.accent { color: #3b82f6; }
.stat-val.green  { color: #34d399; }
.stat-val.amber  { color: #fbbf24; }
.stat-val.red    { color: #f87171; }
.stat-lbl { font-size: 10px; color: #1f2d42; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 3px; }

.input-panel { background: #0a0e18; border: 1px solid #131929; border-radius: 16px; padding: 26px 30px; margin-bottom: 28px; position: relative; overflow: hidden; }
.input-panel::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, #3b82f640, transparent); }

[data-testid="stTextInput"] > div > div > input,
[data-testid="stTextArea"] > div > div > textarea {
    background: #060911 !important; border: 1px solid #1a2535 !important;
    border-radius: 10px !important; color: #c8d5e8 !important;
    font-family: 'DM Mono', monospace !important; font-size: 13px !important; padding: 11px 15px !important;
}
[data-testid="stTextInput"] > div > div > input:focus,
[data-testid="stTextArea"] > div > div > textarea:focus {
    border-color: #3b82f6 !important; box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}
[data-testid="stTextInput"] label, [data-testid="stTextArea"] label, [data-testid="stSelectbox"] label {
    font-family: 'DM Mono', monospace !important; font-size: 10px !important;
    color: #374151 !important; letter-spacing: 1.5px; text-transform: uppercase;
}
[data-testid="stSelectbox"] > div > div {
    background: #060911 !important; border: 1px solid #1a2535 !important;
    border-radius: 10px !important; color: #c8d5e8 !important;
    font-family: 'DM Mono', monospace !important; font-size: 12px !important;
}

[data-testid="stButton"] > button {
    background: #3b82f6 !important; color: #fff !important; border: none !important;
    border-radius: 10px !important; padding: 9px 22px !important;
    font-family: 'DM Mono', monospace !important; font-size: 11px !important;
    font-weight: 500 !important; letter-spacing: 1.5px !important; text-transform: uppercase !important;
    box-shadow: 0 4px 18px rgba(59,130,246,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    background: #5b9af8 !important; box-shadow: 0 6px 24px rgba(59,130,246,0.38) !important; transform: translateY(-1px) !important;
}

.order-card { background: #0a0e18; border: 1px solid #131929; border-radius: 18px; margin-bottom: 16px; overflow: hidden; position: relative; }
.order-card:hover { border-color: #1e2d45; }
.order-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, #3b82f625, transparent); }
.order-hdr { display: flex; align-items: center; justify-content: space-between; padding: 16px 24px; border-bottom: 1px solid #0d1422; flex-wrap: wrap; gap: 10px; }
.oid { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: #fff; }
.ots { font-size: 10px; color: #1f2d42; margin-top: 2px; }
.order-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }

.badge { display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px; border-radius: 20px; font-size: 9px; font-weight: 500; letter-spacing: 1.2px; text-transform: uppercase; }
.badge-pending    { background: rgba(156,163,175,0.08); color: #9ca3af; border: 1px solid rgba(156,163,175,0.15); }
.badge-processing { background: rgba(251,191,36,0.08);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.18); }
.badge-sourced    { background: rgba(96,165,250,0.08);  color: #60a5fa; border: 1px solid rgba(96,165,250,0.18); }
.badge-dispatched { background: rgba(167,139,250,0.08); color: #a78bfa; border: 1px solid rgba(167,139,250,0.18); }
.badge-delivered  { background: rgba(52,211,153,0.08);  color: #34d399; border: 1px solid rgba(52,211,153,0.18); }
.badge-cancelled  { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.18); }
.badge-unpaid     { background: rgba(251,191,36,0.08);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.18); }
.badge-paid       { background: rgba(52,211,153,0.08);  color: #34d399; border: 1px solid rgba(52,211,153,0.18); }
.badge-overdue    { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.18); }
.badge-sms        { background: rgba(59,130,246,0.08);  color: #3b82f6; border: 1px solid rgba(59,130,246,0.18); }

.mod-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; }
.mod-cell { padding: 18px 24px; border-right: 1px solid #0d1422; border-bottom: 1px solid #0d1422; }
.mod-cell:nth-child(3n) { border-right: none; }
.mod-cell-no-border-b { border-bottom: none !important; }
.mod-label { font-size: 8px; letter-spacing: 2.5px; text-transform: uppercase; color: #1f2d42; margin-bottom: 10px; display: flex; align-items: center; gap: 5px; }
.mod-dot { width: 3px; height: 3px; border-radius: 50%; background: #3b82f6; flex-shrink: 0; }

.item-pill { display: inline-flex; align-items: center; gap: 5px; background: #0d1220; border: 1px solid #1a2535; border-radius: 7px; padding: 5px 11px; font-size: 11px; color: #6b7f9a; margin: 2px 3px 2px 0; }
.item-qty { color: #3b82f6; font-weight: 500; }

.vrow { display: flex; justify-content: space-between; align-items: center; padding: 7px 0; border-bottom: 1px solid #0b1018; font-size: 11px; color: #4b5a72; }
.vrow:last-child { border-bottom: none; }
.vrow.best { color: #c8d5e8; }
.vprice { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 600; }
.vrow.best .vprice { color: #3b82f6; }
.vtag { font-size: 7px; letter-spacing: 1.5px; text-transform: uppercase; color: #3b82f6; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); border-radius: 4px; padding: 2px 6px; }
.vstock-no { font-size: 9px; color: #f87171; }

.proc-winner { display: flex; align-items: center; gap: 12px; }
.proc-icon { width: 34px; height: 34px; border-radius: 10px; background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.2); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.proc-name { font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: #fff; }
.proc-sub { font-size: 10px; color: #2d3d52; margin-top: 2px; }

.del-status { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; margin-bottom: 3px; }
.del-eta { font-size: 10px; color: #374151; }
.del-track { font-size: 10px; color: #1f2d42; margin-top: 4px; }

.inv-amount { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; color: #fff; letter-spacing: -0.8px; }
.inv-sub { font-size: 10px; color: #1f2d42; margin-top: 2px; }

.empty { text-align: center; padding: 70px 40px; }
.empty-icon { font-size: 40px; opacity: 0.2; margin-bottom: 14px; }
.empty-title { font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700; color: #1f2d42; margin-bottom: 6px; }
.empty-sub { font-size: 11px; color: #131929; }

[data-testid="stExpander"] { background: #0a0e18 !important; border: 1px solid #131929 !important; border-radius: 12px !important; }
[data-testid="stExpander"] summary { color: #4b5a72 !important; font-size: 12px !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1a2535; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3b82f6; }
</style>
"""

def inject_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
