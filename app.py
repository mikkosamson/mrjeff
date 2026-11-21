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
    "messenger": "https://m.me/mrjeff.qc.erod",
    "sheets_webhook_url": get_webhook_url(),
}

PAGES = [
    "Home",
    "Subscription Plans",
    "Rates & Services",
    "Schedule Pickup",
    "FAQ & Store Info",
]

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


def on_mobile_select():
    st.session_state.active_page = st.session_state.mob_page_selector


# =====================================================================
# FULL-WIDTH STYLING & RESPONSIVE NAVBAR / MOBILE MENU
# =====================================================================
st.markdown(
    """
<style>
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
}
.block-container,
[data-testid="stAppViewBlockContainer"],
[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    width: 100% !important;
    padding-top: 0.6rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
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
    gap: 11px;
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
    white-space: nowrap;
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

/* Desktop Nav Bar */
div[data-testid="stElementContainer"]:has(.desktop-nav-flag) {
    display: none !important;
}
div[data-testid="stHorizontalBlock"]:has(.desktop-nav-flag) {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 8px;
    margin-bottom: 14px;
    align-items: center !important;
}
div[data-testid="stHorizontalBlock"]:has(.desktop-nav-flag) button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    padding: 0.55rem 0.75rem !important;
    width: 100% !important;
    margin: 0 !important;
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

/* Mobile Header & Quick Page Switcher (Hidden on Desktop) */
.mobile-header,
div[data-testid="stElementContainer"]:has(.mobile-nav-flag) {
    display: none !important;
}

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
    .mobile-header {
        display: flex !important;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 12px 14px;
        margin-bottom: 10px;
        gap: 10px;
    }
    .mobile-badge {
        font-size: 11px;
        font-weight: 700;
        color: #0088BD;
        background: #EBF7FD;
        padding: 5px 10px;
        border-radius: 999px;
        white-space: nowrap;
        flex-shrink: 0;
    }
    div[data-testid="stElementContainer"]:has(.mobile-nav-flag) {
        display: block !important;
        margin-bottom: 14px;
    }
    div[data-testid="stElementContainer"]:has(.mobile-nav-flag) div[data-testid="stSelectbox"] > div > div {
        background: #FFFFFF !important;
        border: 1.5px solid #00A8E8 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        color: #1A2530 !important;
    }
    .brand-title { font-size: 16.5px; }
    .brand-sub { font-size: 11px; }
    .hero-box { padding: 20px 18px !important; }
    .hero-title { font-size: 25px !important; }
    .hero-desc { font-size: 14px !important; }
}

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
    f"""
<div class="desktop-header">
<div class="brand-left">
<div class="brand-icon">🧺</div>
<div>
<div class="brand-title">Mr Jeff <span>Laundry</span></div>
<div class="brand-sub">{BRANCH["branch"]}</div>
</div>
</div>
<div class="brand-hours">Mon–Sat &bull; 8:00 AM – 5:00 PM</div>
</div>
""",
    unsafe_allow_html=True,
)

nav_cols = st.columns(len(PAGES), gap="small")
for idx, (col, p_name) in enumerate(zip(nav_cols, PAGES)):
    with col:
        if idx == 0:
            st.markdown(
                """<span class="desktop-nav-flag" style="display:none;"></span>""",
                unsafe_allow_html=True,
            )
        is_active = st.session_state.active_page == p_name
        st.button(
            p_name,
            key=f"desk_nav_{p_name}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
            on_click=go_to,
            args=(p_name,),
        )

# =====================================================================
# 2. MOBILE CLEAN HEADER + INSTANT PAGE SWITCHER
# =====================================================================
st.markdown(
    f"""
<div class="mobile-header">
<div class="brand-left">
<div class="brand-icon" style="width:36px;height:36px;font-size:18px;">🧺</div>
<div>
<div class="brand-title">Mr Jeff <span>Laundry</span></div>
<div class="brand-sub">{BRANCH["branch"]}</div>
</div>
</div>
<div class="mobile-badge">8AM–5PM</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """<span class="mobile-nav-flag" style="display:none;"></span>""",
    unsafe_allow_html=True,
)
st.selectbox(
    "Page",
    PAGES,
    index=PAGES.index(st.session_state.active_page),
    key="mob_page_selector",
    on_change=on_mobile_select,
    label_visibility="collapsed",
)

page = st.session_state.active_page

# =====================================================================
# PAGE 1: HOME
# =====================================================================
if page == "Home":
    st.markdown(
        """
<div class="hero-box">
<div class="eyebrow">Door-to-Door Laundry &amp; Dry Cleaning</div>
<div class="hero-title">The subscription that does the <span>laundry</span> for you</div>
<div class="hero-desc">Monthly laundry plans and per-bag pickup &amp; delivery along E. Rodriguez Sr. Ave. Fresh, neatly folded clothes delivered back to your door 2 days after pickup.</div>
<div class="trust-row">
<span>● 2-Day Standard Delivery</span>
<span>● Same-Day Option (+₱100–₱200)</span>
<span>● Cash, GCash, Maya, BPI &amp; BDO</span>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1.2, 1.2, 1.6])
    with c1:
        st.button(
            "Schedule Pickup →",
            type="primary",
            use_container_width=True,
            on_click=go_to,
            args=("Schedule Pickup", SERVICES[0]),
        )
    with c2:
        st.button(
            "View Subscription Plans",
            use_container_width=True,
            on_click=go_to,
            args=("Subscription Plans",),
        )
    with c3:
        st.button(
            "View Per-Bag & Individual Rates",
            use_container_width=True,
            on_click=go_to,
            args=("Rates & Services",),
        )

    st.markdown("### How It Works")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            """
<div class="ui-card">
<div class="card-tag">Step 1</div>
<div class="card-title">Schedule Pickup</div>
<p style="font-size:13.5px; color:#475569; margin:0;">Choose your plan or per-bag load and submit your pickup date &amp; time window.</p>
</div>
""",
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            """
<div class="ui-card">
<div class="card-tag">Step 2</div>
<div class="card-title">Wash, Iron &amp; Fold</div>
<p style="font-size:13.5px; color:#475569; margin:0;">Washed separately in sanitized machines, carefully pressed or folded, and packed fresh.</p>
</div>
""",
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            """
<div class="ui-card">
<div class="card-tag">Step 3</div>
<div class="card-title">Delivered in 2 Days</div>
<p style="font-size:13.5px; color:#475569; margin:0;">Delivered right to your door 2 days after pickup, or same-day express when needed.</p>
</div>
""",
            unsafe_allow_html=True,
        )

# =====================================================================
# PAGE 2: SUBSCRIPTION PLANS
# =====================================================================
elif page == "Subscription Plans":
    st.markdown("## Monthly Plan Subscriptions")
    st.caption("Bundled bags & ironing packages • Standard 2-day delivery after pickup")

    plans = [
        {
            "tag": "Light Load",
            "name": "Plan Lite",
            "price": "₱1,280",
            "featured": False,
            "features": [
                "Up to 5 kg per bag",
                "Dedicated hygienic machine wash",
                "Neatly folded & packed",
                "2-day delivery after pickup",
            ],
            "service_key": "Plan Lite (Up to 5 kg) — ₱1,280",
        },
        {
            "tag": "Full Load",
            "name": "Plan Max",
            "price": "₱1,680",
            "featured": True,
            "features": [
                "4 large bags (up to 8–9 kg each)",
                "Dedicated hygienic machine wash",
                "Neatly folded & moisture-sealed",
                "2-day delivery after pickup",
            ],
            "service_key": "Plan Max — 4 Large Bags (up to 8–9 kg each) — ₱1,680",
        },
        {
            "tag": "Pressing Bundle",
            "name": "Plan Iron",
            "price": "₱2,480",
            "featured": False,
            "features": [
                "4 small bags (up to 5 kg each)",
                "Includes 24 pcs iron service",
                "Crisp ready-to-wear pressing",
                "2-day delivery after pickup",
            ],
            "service_key": "Plan Iron — 4 Small Bags (up to 5 kg each) + 24 pcs Iron — ₱2,480",
        },
        {
            "tag": "All-In-One Care",
            "name": "Plan Wash & Iron",
            "price": "₱2,880",
            "featured": False,
            "features": [
                "4 large bags (up to 8–9 kg each)",
                "Includes 24 pcs iron service",
                "Folded & pressed neatly",
                "2-day delivery after pickup",
            ],
            "service_key": "Plan Wash & Iron — 4 Large Bags (8–9 kg each) + 24 pcs Iron — ₱2,880",
        },
    ]

    cols = st.columns(4)
    for col, p in zip(cols, plans):
        with col:
            card_cls = "ui-card featured" if p["featured"] else "ui-card"
            badge_html = '<div class="pop-pill">Most Popular</div>' if p["featured"] else ""
            feats_html = "".join(f"<li>{item}</li>" for item in p["features"])
            card_html = f"""
<div class="{card_cls}">
{badge_html}
<div class="card-tag">{p["tag"]}</div>
<div class="card-title">{p["name"]}</div>
<div class="card-price">{p["price"]} <span>/ plan</span></div>
<ul class="feat-list">{feats_html}</ul>
</div>
"""
            st.markdown(card_html, unsafe_allow_html=True)
            st.button(
                f"Select {p['name']}",
                key=f"btn_{p['name']}",
                type="primary" if p["featured"] else "secondary",
                use_container_width=True,
                on_click=go_to,
                args=("Schedule Pickup", p["service_key"]),
            )

# =====================================================================
# PAGE 3: RATES & SERVICES
# =====================================================================
elif page == "Rates & Services":
    st.markdown("## Per-Bag, Specialty & Individual Rates")
    st.caption("Pay-as-you-go pricing • No subscription required")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
<div class="ui-card">
<div class="card-title">Regular Wash &amp; Fold</div>
<p style="font-size:12.5px; color:#64748B; margin-bottom:12px;">Everyday clothes, shirts, shorts, towels &amp; bedsheets</p>
<div class="rate-row"><div><strong>1 Large Bag</strong><small>6–9 kg capacity</small></div><div class="rate-price">₱450</div></div>
<div class="rate-row" style="margin-bottom:0;"><div><strong>1 Small Bag</strong><small>1–5 kg capacity</small></div><div class="rate-price">₱350</div></div>
</div>
<div class="ui-card">
<div class="card-title">Handwash &amp; Bulky Items</div>
<p style="font-size:12.5px; color:#64748B; margin-bottom:12px;">Gentle manual care &amp; oversized household items</p>
<div class="rate-row"><div><strong>Handwash</strong><small>Delicate garments (per kg)</small></div><div class="rate-price">₱120 / kg</div></div>
<div class="rate-row"><div><strong>Comforters</strong><small>Depends on size &amp; thickness</small></div><div class="rate-price">₱450–₱550</div></div>
<div class="rate-row"><div><strong>Rugs</strong><small>Deep clean (per kg)</small></div><div class="rate-price">₱120 / kg</div></div>
<div class="rate-row" style="margin-bottom:0;"><div><strong>Stuffed Toys</strong><small>Depends on size</small></div><div class="rate-price">₱250–₱450</div></div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
<div class="ui-card">
<div class="card-title">Heavywash</div>
<p style="font-size:12.5px; color:#64748B; margin-bottom:12px;">Deep wash for denim, thick towels, uniforms &amp; heavy fabrics</p>
<div class="rate-row"><div><strong>1 Large Bag</strong><small>6–8 kg capacity</small></div><div class="rate-price">₱600</div></div>
<div class="rate-row" style="margin-bottom:0;"><div><strong>1 Small Bag</strong><small>1–5 kg capacity</small></div><div class="rate-price">₱400</div></div>
</div>
<div class="ui-card">
<div class="card-title">Iron Services &amp; Dry Cleaning</div>
<p style="font-size:12.5px; color:#64748B; margin-bottom:12px;">Crisp pressing &amp; specialized garment care</p>
<div class="rate-row"><div><strong>Iron Services</strong><small>Per piece pressing</small></div><div class="rate-price">₱70 / pc</div></div>
<div class="rate-row" style="margin-bottom:0;"><div><strong>Dry Cleaning</strong><small>Price depends on item &amp; material</small></div><div class="rate-price">Custom Quote</div></div>
</div>
<div class="ui-card" style="background:#F4F8FB;">
<div class="card-title" style="font-size:16px;">Delivery &amp; Accepted Payments</div>
<p style="font-size:13px; color:#475569; margin-bottom:8px;">Standard delivery is <strong>2 days after pickup</strong>. Same-day delivery is available for an additional <strong>₱100–₱200</strong>.</p>
<div>
<span class="pay-chip">Cash</span>
<span class="pay-chip">GCash</span>
<span class="pay-chip">Maya</span>
<span class="pay-chip">BPI</span>
<span class="pay-chip">BDO</span>
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.button(
        "Schedule a Pickup →",
        type="primary",
        use_container_width=True,
        on_click=go_to,
        args=("Schedule Pickup",),
    )

# =====================================================================
# PAGE 4: SCHEDULE PICKUP (Interactive Booking)
# =====================================================================
elif page == "Schedule Pickup":
    st.markdown("## Schedule Your Laundry Pickup")
    st.caption(f"{BRANCH['address']} • {BRANCH['hours']}")

    b1, b2, b3 = st.columns(3)
    with b1:
        st.link_button(
            f"Chat on Viber ({BRANCH['viber']})",
            f"viber://chat?number={urllib.parse.quote(BRANCH['viber'])}",
            use_container_width=True,
        )
    with b2:
        st.link_button(
            "Facebook Messenger",
            BRANCH["messenger"],
            use_container_width=True,
        )
    with b3:
        st.link_button(
            f"Call Mobile ({BRANCH['mobile']})",
            f"tel:{BRANCH['mobile']}",
            use_container_width=True,
        )

    st.markdown("---")

    with st.form("pickup_booking_form"):
        selected_srv = st.selectbox(
            "Service or Subscription Plan",
            SERVICES,
            key="selected_service",
        )

        f1, f2 = st.columns(2)
        with f1:
            cust_name = st.text_input("Full Name *", placeholder="Juan Dela Cruz")
            pickup_date = st.date_input(
                "Preferred Pickup Date (Mon–Sat)",
                min_value=datetime.date.today(),
            )
            delivery_speed = st.selectbox(
                "Delivery Turnaround",
                [
                    "Standard Delivery (2 days after pickup)",
                    "Same-Day Delivery (+₱100–₱200 fee)",
                ],
            )
        with f2:
            cust_phone = st.text_input("Mobile / Viber Number *", placeholder="0917 123 4567")
            pickup_slot = st.selectbox(
                "Preferred Time Window (8AM–5PM)",
                [
                    "Morning (8:00 AM – 12:00 PM)",
                    "Afternoon (1:00 PM – 5:00 PM)",
                ],
            )
            payment_method = st.selectbox(
                "Preferred Payment Method",
                ["GCash", "Maya", "Cash", "Bank Transfer — BPI", "Bank Transfer — BDO"],
            )

        cust_address = st.text_input(
            "Complete Pickup Address *",
            placeholder="Unit / House No., Street, Barangay, Quezon City",
        )
        notes = st.text_input(
            "Special Instructions (Optional)",
            placeholder="e.g., Gate code, landmark, or estimated kg/pieces",
        )

        submitted = st.form_submit_button(
            "Generate Booking Summary",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not cust_name.strip() or not cust_phone.strip() or not cust_address.strip():
            st.error("Please fill in your Name, Mobile/Viber Number, and Pickup Address.")
        else:
            order_summary = (
                f"Hi Mr Jeff Laundry ({BRANCH['branch']})! I'd like to schedule a pickup:\n"
                f"• Service/Plan: {selected_srv}\n"
                f"• Name: {cust_name.strip()}\n"
                f"• Mobile: {cust_phone.strip()}\n"
                f"• Address: {cust_address.strip()}\n"
                f"• Pickup Date: {pickup_date.strftime('%Y-%m-%d')}\n"
                f"• Time Slot: {pickup_slot}\n"
                f"• Delivery: {delivery_speed}\n"
                f"• Payment Method: {payment_method}"
            )
            if notes.strip():
                order_summary += f"\n• Notes: {notes.strip()}"

            if BRANCH["sheets_webhook_url"]:
                try:
                    requests.post(
                        BRANCH["sheets_webhook_url"],
                        json={
                            "timestamp": datetime.datetime.now().isoformat(),
                            "service": selected_srv,
                            "name": cust_name.strip(),
                            "phone": cust_phone.strip(),
                            "address": cust_address.strip(),
                            "pickup_date": str(pickup_date),
                            "time_slot": pickup_slot,
                            "delivery": delivery_speed,
                            "payment": payment_method,
                            "notes": notes.strip(),
                        },
                        timeout=5,
                    )
                except Exception:
                    pass

            st.success(
                "Your pickup summary is ready! Tap the copy icon at the top-right of the box below, then send it via Viber or Messenger."
            )
            st.code(order_summary, language=None)

            a1, a2 = st.columns(2)
            with a1:
                st.link_button(
                    "Open Viber & Paste Order →",
                    f"viber://chat?number={urllib.parse.quote(BRANCH['viber'])}",
                    type="primary",
                    use_container_width=True,
                )
            with a2:
                st.link_button(
                    "Open Facebook Messenger →",
                    BRANCH["messenger"],
                    use_container_width=True,
                )

# =====================================================================
# PAGE 5: FAQ & STORE INFO
# =====================================================================
elif page == "FAQ & Store Info":
    left, right = st.columns([1.15, 0.85])

    with left:
        st.markdown("## Frequently Asked Questions")
        with st.expander("When will my laundry be delivered after pickup?", expanded=True):
            st.write(
                "We usually deliver your clean, folded laundry **2 days after pickup**. "
                "If you need your clothes back on the same day, we offer **same-day delivery** "
                "for an additional fee of **₱100–₱200**."
            )
        with st.expander("What are your accepted payment methods?"):
            st.write(
                "You can pay via **Cash**, **GCash**, **Maya**, or **Bank Transfer (BPI or BDO)**."
            )
        with st.expander("What is the difference between a Small Bag and a Large Bag?"):
            st.write(
                "A **Small Bag** fits **1–5 kg** (₱350 Regular / ₱400 Heavywash), while a **Large Bag** "
                "fits **6–9 kg** for Regular Wash & Fold (₱450) or **6–8 kg** for Heavywash (₱600)."
            )
        with st.expander("How is Dry Cleaning priced?"):
            st.write(
                "Dry cleaning rates depend on the specific garment type and fabric material "
                "(such as barong, suits, gowns, or delicate coats). Message us a photo on Viber "
                "or Facebook Messenger for an exact quote."
            )

    with right:
        st.markdown("## Branch & Contact Details")
        st.markdown(
            f"""
<div class="ui-card">
<div class="card-tag">Branch Location</div>
<div class="card-title">{BRANCH["branch"]}</div>
<p style="font-size:13.5px; color:#334155; margin-bottom:12px;">{BRANCH["address"]}</p>
<p style="font-size:13.5px; margin-bottom:6px;"><strong>Hours:</strong> {BRANCH["hours"]}</p>
<p style="font-size:13.5px; margin-bottom:6px;"><strong>Viber / Mobile:</strong> <a href="tel:{BRANCH["mobile"]}" style="color:#0088BD; text-decoration:none; font-weight:700;">{BRANCH["mobile"]}</a></p>
<p style="font-size:13.5px; margin-bottom:6px;"><strong>Landline:</strong> <a href="tel:{BRANCH["landline"]}" style="color:#0088BD; text-decoration:none; font-weight:700;">{BRANCH["landline"]}</a></p>
<p style="font-size:13.5px; margin-bottom:12px;"><strong>Facebook:</strong> <a href="{BRANCH["facebook"]}" target="_blank" style="color:#0088BD; text-decoration:none; font-weight:700;">facebook.com/mrjeff.qc.erod</a></p>
<div>
<span class="pay-chip">Cash</span>
<span class="pay-chip">GCash</span>
<span class="pay-chip">Maya</span>
<span class="pay-chip">BPI</span>
<span class="pay-chip">BDO</span>
</div>
</div>
""",
            unsafe_allow_html=True,
        )
