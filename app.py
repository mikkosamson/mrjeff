import datetime
import urllib.parse
import requests
import streamlit as st

st.set_page_config(
    page_title="Mr Jeff Laundry — E. Rodriguez Sr. Ave.",
    page_icon="🧺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def get_webhook_url() -> str:
    try:
        return st.secrets.get("SHEETS_WEBHOOK_URL", "")
    except Exception:
        return ""


# =====================================================================
# BRANCH SETTINGS
# =====================================================================
BRANCH = {
    "name": "Mr Jeff Laundry",
    "branch": "E. Rodriguez Sr. Ave.",
    "address": "1365 E Rodriguez Sr. Ave, Quezon City, 1112 Metro Manila",
    "hours": "Monday - Saturday 8AM - 5PM",
    "viber": "+639772432513",
    "mobile": "+639772432513",
    "landline": "+63270899423",
    "facebook": "https://www.facebook.com/mrjeff.qc.erod",
    "messenger": "https://www.facebook.com/mrjeff.qc.erod",
    "sheets_webhook_url": st.secrets.get("SHEETS_WEBHOOK_URL", ""),
}

PAGES = ["Home", "Subscription Plans", "Rates & Services", "Schedule Pickup", "FAQ & Store Info"]

SERVICES = [
    "Plan Max — 4 Large Bags (up to 8–9 kg each) — ₱1,680",
    "Plan Lite (Up to 5 kg) — ₱1,280",
    "Plan Wash & Iron — 4 Large Bags (8–9 kg each) + 24 pcs Iron — ₱2,880",
    "Plan Iron — 4 Small Bags (up to 5 kg each) + 24 pcs Iron — ₱2,480",
    "Regular Wash & Fold — 1 Large Bag (6–9 kg) — ₱450",
    "Regular Wash & Fold — 1 Small Bag (1–5 kg) — ₱350",
    "Heavywash — 1 Large Bag (6–8 kg) — ₱600",
    "Heavywash — 1 Small Bag (1–5 kg) — ₱400",
    "Handwash — ₱120 / kg",
    "Comforters — ₱450–₱550",
    "Rugs — ₱120 / kg",
    "Stuffed Toys — ₱250–₱450",
    "Iron Services — ₱70 / piece",
    "Dry Cleaning (Price depends on item & material)",
]

# =====================================================================
# SESSION STATE & NAVIGATION CALLBACKS
# =====================================================================
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"
if "selected_service" not in st.session_state:
    st.session_state.selected_service = SERVICES[0]


def go_to(page: str, service: str | None = None):
    if service and service in SERVICES:
        st.session_state.selected_service = service
    st.session_state.active_page = page


# =====================================================================
# FULL-WIDTH STYLING & RESPONSIVE NAVBAR / MOBILE BURGER MENU
# =====================================================================
st.markdown(
    """
<style>
/* Hide Streamlit default chrome */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
}

/* Full-width container (removes large left/right side margins) */
.block-container,
[data-testid="stAppViewBlockContainer"],
[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    width: 100% !important;
    padding-top: 0.6rem !important;
    padding-bottom: 3rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Desktop Brand Header */
.desktop-header {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 14px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}
.brand-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.brand-icon {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    background: #00A8E8;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(0, 168, 232, 0.25);
}
.brand-title {
    font-size: 20px;
    font-weight: 800;
    color: #1A2530;
    line-height: 1.15;
}
.brand-title span { color: #00A8E8; }
.brand-sub {
    font-size: 12px;
    font-weight: 600;
    color: #64748B;
}
.brand-hours {
    font-size: 12.5px;
    font-weight: 700;
    color: #0088BD;
    background: #EBF7FD;
    padding: 6px 14px;
    border-radius: 999px;
    white-space: nowrap;
}

/* Full-width Desktop Navigation Bar */
div[data-testid="stHorizontalBlock"]:has(.desktop-nav-flag) {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 8px;
    margin-bottom: 14px;
}
div[data-testid="stHorizontalBlock"]:has(.desktop-nav-flag) button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    padding: 0.55rem 0.75rem !important;
    width: 100% !important;
}
div[data-testid="stHorizontalBlock"]:has(.desktop-nav-flag) button[kind="secondary"] {
    background: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    color: #334155 !important;
}
div[data-testid="stHorizontalBlock"]:has(.desktop-nav-flag) button[kind="secondary"]:hover {
    background: #EBF7FD !important;
    border-color: #00A8E8 !important;
    color: #0088BD !important;
}

/* Hide mobile burger row on desktop */
@media (min-width: 769px) {
    div[data-testid="stHorizontalBlock"]:has(.mobile-burger-flag) {
        display: none !important;
    }
}

/* Mobile Responsive Rules (Burger Menu + Tight Padding) */
@media (max-width: 768px) {
    .block-container,
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stMainBlockContainer"] {
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
    }
    .desktop-header,
    div[data-testid="stHorizontalBlock"]:has(.desktop-nav-flag) {
        display: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.mobile-burger-flag) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 8px 12px;
        margin-bottom: 12px;
        gap: 8px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.mobile-burger-flag) > div:first-child {
        flex: 1 1 auto !important;
        width: auto !important;
        min-width: 0 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.mobile-burger-flag) > div:last-child {
        flex: 0 0 auto !important;
        width: auto !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.mobile-burger-flag) [data-testid="stPopover"] button {
        border-radius: 10px !important;
        padding: 0.45rem 0.85rem !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        background: #EBF7FD !important;
        color: #0088BD !important;
        border: 1px solid #BAE6FD !important;
    }
    .brand-title { font-size: 16.5px; }
    .brand-sub { font-size: 11px; }
    .hero-title { font-size: 25px !important; }
}

/* Hero & Content Cards */
.hero-box {
    background: linear-gradient(135deg, #FFFFFF 0%, #E8F6FD 100%);
    border: 1px solid #D4ECF9;
    border-radius: 22px;
    padding: 30px 26px;
    margin-bottom: 16px;
}
.eyebrow {
    display: inline-block;
    background: #EBF7FD;
    color: #0088BD;
    font-size: 12px;
    font-weight: 700;
    padding: 5px 13px;
    border-radius: 999px;
    margin-bottom: 12px;
}
.hero-title {
    font-size: 34px;
    font-weight: 800;
    line-height: 1.18;
    color: #1A2530;
    margin-bottom: 10px;
}
.hero-title span { color: #00A8E8; }
.hero-desc {
    font-size: 15.5px;
    color: #475569;
    line-height: 1.55;
    margin-bottom: 14px;
    max-width: 780px;
}
.trust-row {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    font-size: 13px;
    font-weight: 600;
    color: #334155;
}
.ui-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 20px 18px;
    margin-bottom: 10px;
    box-shadow: 0 4px 14px rgba(26, 37, 48, 0.03);
}
.ui-card.featured {
    border: 2px solid #00A8E8;
    background: linear-gradient(180deg, #F4FBFF 0%, #FFFFFF 35%);
}
.pop-pill {
    display: inline-block;
    background: #00A8E8;
    color: #FFFFFF;
    font-size: 10.5px;
    font-weight: 800;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 999px;
    margin-bottom: 6px;
}
.card-tag {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    color: #00A8E8;
    margin-bottom: 2px;
}
.card-title {
    font-size: 19px;
    font-weight: 800;
    color: #1A2530;
    margin-bottom: 6px;
}
.card-price {
    font-size: 26px;
    font-weight: 800;
    color: #1A2530;
    padding: 8px 0;
    margin: 8px 0 10px;
    border-top: 1px solid #F1F5F9;
    border-bottom: 1px solid #F1F5F9;
}
.card-price span { font-size: 13px; font-weight: 500; color: #64748B; }
.feat-list {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 13.5px;
    color: #334155;
    line-height: 1.75;
}
.feat-list li::before {
    content: "✓ ";
    color: #00A8E8;
    font-weight: 800;
}
.rate-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 12px;
    background: #F8FAFC;
    border: 1px solid #F1F5F9;
    border-radius: 12px;
    margin-bottom: 8px;
}
.rate-row strong { display: block; font-size: 14px; color: #1A2530; }
.rate-row small { font-size: 12px; color: #64748B; }
.rate-price { font-size: 15px; font-weight: 800; color: #0088BD; white-space: nowrap; }
.pay-chip {
    display: inline-block;
    background: #EBF7FD;
    color: #0088BD;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 11px;
    border-radius: 999px;
    margin: 3px 4px 3px 0;
}
div.stButton > button {
    border-radius: 999px !important;
    font-weight: 700 !important;
    padding: 0.5rem 1.2rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================================
# 1. DESKTOP FULL-WIDTH HEADER + FULL-WIDTH NAVIGATION BAR
# =====================================================================
st.markdown(
    f'<div class="desktop-header">'
    f'<div class="brand-left">'
    f'<div class="brand-icon">🧺</div>'
    f'<div><div class="brand-title">Mr Jeff <span>Laundry</span></div>'
    f'<div class="brand-sub">{BRANCH["branch"]}</div></div>'
    f'</div>'
    f'<div class="brand-hours">Mon–Sat &bull; 8:00 AM – 5:00 PM</div>'
    f'</div>',
    unsafe_allow_html=True,
)

nav_cols = st.columns(len(PAGES), gap="small")
for idx, (col, p_name) in enumerate(zip(nav_cols, PAGES)):
    with col:
        if idx == 0:
            st.markdown('<span class="desktop
