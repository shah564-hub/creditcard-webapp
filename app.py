import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

from db import (
    init_db,
    add_customer,
    get_customers,
    delete_customer,
    add_card,
    get_cards,
    delete_card,
    add_transaction,
    get_transactions,
)

from utils import luhn_check, clean_card_number, now_ts


# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="CreditPay - Payment Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

NAV_ORDER = ["Dashboard", "Customers", "Cards", "Payments", "History", "Reports", "About"]

# =========================================
# SESSION STATE
# =========================================
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "splash_done" not in st.session_state:
    st.session_state.splash_done = False


# =========================================
# NAV HELPERS
# =========================================
def set_page(page_name: str):
    st.session_state.page = page_name


def go_next():
    i = NAV_ORDER.index(st.session_state.page)
    if i < len(NAV_ORDER) - 1:
        st.session_state.page = NAV_ORDER[i + 1]


def go_back():
    i = NAV_ORDER.index(st.session_state.page)
    if i > 0:
        st.session_state.page = NAV_ORDER[i - 1]


# =========================================
# PREMIUM CSS (NO HTML CODE VISIBLE ✅)
# =========================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap');
* { font-family:'Poppins', sans-serif; }

.stApp{
    background:
      radial-gradient(circle at 15% 20%, rgba(99,102,241,.20), transparent 45%),
      radial-gradient(circle at 85% 30%, rgba(168,85,247,.22), transparent 55%),
      radial-gradient(circle at 60% 90%, rgba(59,130,246,.15), transparent 40%),
      linear-gradient(135deg, #f8fbff, #eef6ff, #fbf1ff);
}

/* Layout padding */
.block-container{
    padding-top: 40px !important;   /* ✅ Fix title cut */
    padding-bottom: 95px !important;
}

}

/* Sidebar */
/* ✅ SIDEBAR FIX (text invisible issue) */
/* ✅ FORCE DARK SIDEBAR (100% FIX) */
section[data-testid="stSidebar"] {
    background: #050b1a !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] > div {
    background: #050b1a !important;
    opacity: 1 !important;
}

/* ✅ Force text bright */
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* ✅ Fix radio circles + labels */
section[data-testid="stSidebar"] label {
    color: #ffffff !important;
}

/* ✅ Selected radio item highlight */
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-testid="stMarkdownContainer"] {
    color: #ffffff !important;
}

/* ✅ Hover effect */
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
}

/* ✅ Remove that grey washed overlay */
section[data-testid="stSidebar"]::before {
    background: none !important;
    content: "" !important;
}

/* Header */
.app-header{
    text-align:center;
    margin: 6px 0 14px 0;
    animation: fadeIn .6s ease;
    padding-top: 10px;
}
.app-title{
    font-size: 46px;
    font-weight: 700;              /* less bold */
    letter-spacing: 1px;           /* stylish spacing */
    background: linear-gradient(90deg,#6366f1,#a855f7,#3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


}
.app-subtitle{
    font-size: 14px;
    opacity: .75;
    margin-top: 6px;
}
.app-bar{
    height: 12px;
    width: 72%;
    margin: 12px auto 0;
    border-radius: 999px;
    background: linear-gradient(90deg,#6366f1,#a855f7,#3b82f6);
    box-shadow: 0px 14px 30px rgba(99,102,241,.20);
}

/* Card container */
.card{
    background: rgba(255,255,255,.88);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0px 24px 70px rgba(0,0,0,.10);
    border: 1px solid rgba(0,0,0,.05);
    animation: slideUp .5s ease;
}

/* KPI Cards */
.kpi{
    background: linear-gradient(120deg,rgba(99,102,241,.18),rgba(168,85,247,.12));
    border-radius: 18px;
    padding: 16px;
    border: 1px solid rgba(0,0,0,.05);
}
.kpi-title{
    font-size: 13px;
    opacity: .78;
    font-weight: 700;
}
.kpi-value{
    font-size: 30px;
    font-weight: 900;
    margin-top: 6px;
}

/* Buttons */
.stButton>button{
    border-radius: 16px !important;
    font-weight: 800 !important;
    border: none !important;
    padding: 10px 18px !important;
    background: linear-gradient(90deg,#6366f1,#a855f7) !important;
    color: white !important;
    box-shadow: 0px 18px 40px rgba(99,102,241,.25);
    transition: .2s ease;
}
.stButton>button:hover{
    transform: translateY(-2px);
}

/* Next Back buttons */
.nav-btns{
    margin: 10px 0 10px 0;
}
.nav-box{
    background: rgba(255,255,255,.65);
    border: 1px solid rgba(0,0,0,.06);
    padding: 12px;
    border-radius: 18px;
    box-shadow: 0px 12px 40px rgba(0,0,0,.08);
}

/* Splash */
.splash-wrap{
    display:flex;
    justify-content:center;
    align-items:center;
    min-height: 80vh;
    animation: fadeIn .6s ease;
}
.splash-box{
    width:min(740px,95%);
    background: rgba(255,255,255,.92);
    padding: 34px;
    border-radius: 28px;
    text-align:center;
    box-shadow: 0px 30px 90px rgba(0,0,0,.14);
    border: 1px solid rgba(0,0,0,.05);
}
.splash-icon{
    width: 92px;
    height: 92px;
    border-radius: 26px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin: 0 auto 12px auto;
    font-size: 44px;
    background: linear-gradient(120deg,#6366f1,#a855f7,#3b82f6);
    box-shadow: 0px 18px 50px rgba(99,102,241,.30);
}
.loader{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: 6px solid rgba(0,0,0,.10);
    border-top: 6px solid #6366f1;
    margin: 18px auto;
    animation: spin 1s linear infinite;
}
@keyframes spin{100%{transform:rotate(360deg)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes slideUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}

/* Bottom nav */
/* ✅ GPay-style Bottom Nav + Active Glow (UI only) */
.bottom-nav{
    position: fixed;
    left: 12px;
    right: 12px;
    bottom: 12px;
    height: 74px;
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 22px;
    box-shadow: 0px 25px 70px rgba(0,0,0,0.15);
    display: flex;
    justify-content: space-around;
    align-items: center;
    z-index: 9999;
}

/* Bottom nav buttons smaller + cleaner */
.bottom-nav .stButton > button{
    width: 100% !important;
    border-radius: 18px !important;
    padding: 10px 10px !important;
    font-size: 12px !important;
    font-weight: 800 !important;
    background: rgba(99,102,241,0.10) !important;
    color: #111827 !important;
    border: 1px solid rgba(99,102,241,0.15) !important;
    box-shadow: none !important;
    transition: 0.2s ease !important;
}

/* Hover effect */
.bottom-nav .stButton > button:hover{
    transform: translateY(-2px) scale(1.02);
    background: rgba(99,102,241,0.18) !important;
}

/* ✅ ACTIVE GLOW (works when clicked by user visually) */
.bottom-nav .stButton > button:focus{
    outline: none !important;
    background: linear-gradient(90deg,#6366f1,#a855f7) !important;
    color: white !important;
    box-shadow: 0px 14px 35px rgba(99,102,241,0.30) !important;
}

/* Mobile padding improvements */
@media(max-width:850px){
    .block-container{
        padding-left: 14px !important;
        padding-right: 14px !important;
    }
}


/* Mobile fixes */
@media(max-width:850px){
    section[data-testid="stSidebar"]{ display:none !important; }
    .app-title{ font-size: 34px; }
    .app-bar{ width: 92%; }
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================
# SPLASH SCREEN ✅
# =========================================
if not st.session_state.splash_done:
    st.markdown(
        """
        <div class="splash-wrap">
            <div class="splash-box">
                <div class="splash-icon">💳</div>
                <h1 style="margin:0;font-weight:900;">CreditPay</h1>
                <p style="margin:6px 0 0;opacity:.75;font-weight:600;">
                    Payments • Customers • Reports • Secure UI
                </p>
                <div class="loader"></div>
                <p style="font-weight:800;margin-top:6px;">Loading your dashboard...</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(2)
    st.session_state.splash_done = True
    st.rerun()

# =========================================
# SIDEBAR NAV (DESKTOP)
# =========================================
with st.sidebar:
    st.markdown("## 💳 Control Panel")
    st.caption("Premium UI • Smooth Flow • Mobile Ready")
    selected = st.radio("Navigation", NAV_ORDER, index=NAV_ORDER.index(st.session_state.page))
    st.session_state.page = selected

page = st.session_state.page

# =========================================
# HEADER
# =========================================
st.markdown(
    """
    <div class="app-header">
        <div class="app-title">CreditPay</div>
        <div class="app-subtitle">Fast • Secure • Modern • Streamlit + SQLite</div>
        <div class="app-bar"></div>
    </div>
""",
    unsafe_allow_html=True,
)

# =========================================
# TOP NAV BUTTONS (BACK / NEXT)
# =========================================
st.markdown("<div class='nav-box nav-btns'>", unsafe_allow_html=True)
cL, cR = st.columns([1, 1])
with cL:
    st.button("⬅ Back", on_click=go_back)
with cR:
    st.button("Next ➡", on_click=go_next)
st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# DATA HELPERS
# =========================================
def df_customers_safe(rows):
    return pd.DataFrame(rows, columns=["ID", "Name", "Email"]) if rows else pd.DataFrame(columns=["ID", "Name", "Email"])


def df_cards_safe(rows):
    return pd.DataFrame(rows, columns=["CardID", "Last4", "Brand", "Expiry"]) if rows else pd.DataFrame(columns=["CardID", "Last4", "Brand", "Expiry"])


def df_txns_safe(rows):
    return pd.DataFrame(rows, columns=["TxnID", "Amount", "Status", "Message", "Time"]) if rows else pd.DataFrame(columns=["TxnID", "Amount", "Status", "Message", "Time"])


def format_card_input(raw):
    digits = "".join(c for c in raw if c.isdigit())
    grouped = " ".join(digits[i:i+4] for i in range(0, len(digits), 4))
    return grouped[:19]


def format_expiry(raw):
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) <= 2:
        return digits
    return digits[:2] + "/" + digits[2:4]


def generate_pdf_report(customer_name, customer_email, df_txn):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(0, 10, "CreditPay - Transaction Report", ln=True, align="C")
    pdf.ln(4)

    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Customer: {customer_name}", ln=True)
    pdf.cell(0, 8, f"Email: {customer_email}", ln=True)
    pdf.cell(0, 8, f"Generated: {now_ts()}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    pdf.cell(20, 8, "TxnID", 1)
    pdf.cell(30, 8, "Amount", 1)
    pdf.cell(30, 8, "Status", 1)
    pdf.cell(110, 8, "Time", 1)
    pdf.ln()

    for _, row in df_txn.iterrows():
        pdf.cell(20, 8, str(row["TxnID"]), 1)
        pdf.cell(30, 8, f"{row['Amount']}", 1)
        pdf.cell(30, 8, str(row["Status"]), 1)
        pdf.cell(110, 8, str(row["Time"])[:19], 1)
        pdf.ln()

    filename = "transaction_report.pdf"
    pdf.output(filename)
    return filename


# =========================================
# LOAD DB
# =========================================
customers = get_customers()
df_customers = df_customers_safe(customers)

# =========================================
# PAGES
# =========================================
if page == "Dashboard":
    total_customers = len(customers)

    all_txns = []
    total_amount = 0.0
    for c in customers:
        txs = get_transactions(c[0])
        all_txns.extend(txs)
        for t in txs:
            total_amount += float(t[1])

    df_all = df_txns_safe(all_txns)

    success_rate = 0
    if not df_all.empty:
        success_rate = (df_all["Status"].eq("SUCCESS").sum() / len(df_all)) * 100

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"<div class='kpi'><div class='kpi-title'>👤 Customers</div><div class='kpi-value'>{total_customers}</div></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='kpi'><div class='kpi-title'>🧾 Transactions</div><div class='kpi-value'>{len(df_all)}</div></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='kpi'><div class='kpi-title'>💰 Total Amount</div><div class='kpi-value'>₹{total_amount:,.0f}</div></div>", unsafe_allow_html=True)
    with k4:
        st.markdown(f"<div class='kpi'><div class='kpi-title'>✅ Success Rate</div><div class='kpi-value'>{success_rate:.1f}%</div></div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='card'><h3>📌 Quick Summary</h3><p>Welcome to CreditPay. Manage customers, cards, payments & reports like a real payment app.</p></div>", unsafe_allow_html=True)

elif page == "Customers":
    st.markdown("<div class='card'><h2>👤 Customer Management</h2><p>Add & manage customers</p></div>", unsafe_allow_html=True)
    st.write("")

    with st.form("add_customer_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Customer Name", placeholder="e.g., Rahul Sharma")
        with c2:
            email = st.text_input("Customer Email", placeholder="e.g., rahul@gmail.com")
        add_btn = st.form_submit_button("✅ Add Customer")

    if add_btn:
        if name.strip() and email.strip():
            add_customer(name.strip(), email.strip())
            st.success("Customer Added ✅")
            st.rerun()
        else:
            st.error("Enter both Name and Email")

    st.write("")
    customers = get_customers()
    df_customers = df_customers_safe(customers)
    st.dataframe(df_customers, use_container_width=True)

    if not df_customers.empty:
        st.write("")
        del_id = st.selectbox("Select customer ID to delete", df_customers["ID"].tolist())
        if st.button("❌ Delete Customer"):
            delete_customer(del_id)
            st.success("Deleted ✅")
            st.rerun()

elif page == "Cards":
    st.markdown("<div class='card'><h2>💳 Cards</h2><p>Secure Card Save • Stores only last 4 digits • Luhn validation ✅</p></div>", unsafe_allow_html=True)
    st.write("")

    if df_customers.empty:
        st.warning("Add customers first.")
    else:
        cid = st.selectbox("Select Customer ID", df_customers["ID"].tolist())

        with st.form("add_card_form"):
            cc1, cc2 = st.columns(2)
            with cc1:
                card_number_raw = st.text_input("Card Number", placeholder="4532 0151 1283 0366")
                expiry_raw = st.text_input("Expiry (MM/YYYY)", placeholder="09/2000")
            with cc2:
                brand = st.selectbox("Brand", ["Visa", "MasterCard", "RuPay", "Amex"])
            save = st.form_submit_button("✅ Save Card")

        if save:
            formatted_card = format_card_input(card_number_raw)
            digits = clean_card_number(formatted_card)

            if not digits or len(digits) < 12:
                st.error("Enter valid card number")
            elif not luhn_check(digits):
                st.error("❌ Invalid card (Luhn failed)")
            else:
                add_card(cid, digits[-4:], brand, format_expiry(expiry_raw))
                st.success("Card Saved ✅")
                st.rerun()

        st.write("")
        cards = get_cards(cid)
        df_cards = df_cards_safe(cards)
        st.dataframe(df_cards, use_container_width=True)

        if not df_cards.empty:
            st.write("")
            del_card_id = st.selectbox("Select CardID to delete", df_cards["CardID"].tolist())
            if st.button("❌ Delete Card"):
                delete_card(del_card_id)
                st.success("Card Deleted ✅")
                st.rerun()

elif page == "Payments":
    st.markdown("<div class='card'><h2>💰 Payments</h2><p>Process payments with success/fail scenarios</p></div>", unsafe_allow_html=True)
    st.write("")

    if df_customers.empty:
        st.warning("Add customers first.")
    else:
        cid = st.selectbox("Select Customer ID", df_customers["ID"].tolist())
        amount = st.number_input("Amount (₹)", min_value=0.0, value=500.0, step=100.0)

        if st.button("🚀 Process Payment"):
            if amount <= 0:
                status, msg = "FAILED", "Amount must be greater than 0"
            elif amount > 50000:
                status, msg = "FAILED", "Limit exceeded (₹50,000)"
            else:
                status, msg = "SUCCESS", "Payment processed successfully ✅"

            add_transaction(cid, amount, status, msg, now_ts())

            if status == "SUCCESS":
                st.success(msg)
            else:
                st.error(msg)

            st.rerun()

elif page == "History":
    st.markdown("<div class='card'><h2>📜 Transaction History</h2><p>View all transaction logs</p></div>", unsafe_allow_html=True)
    st.write("")

    if df_customers.empty:
        st.info("No customers found.")
    else:
        cid = st.selectbox("Select Customer ID", df_customers["ID"].tolist())
        txns = get_transactions(cid)
        df_txn = df_txns_safe(txns)

        if df_txn.empty:
            st.info("No transactions yet.")
        else:
            st.dataframe(df_txn, use_container_width=True)

elif page == "Reports":
    st.markdown("<div class='card'><h2>📤 Reports</h2><p>Download CSV + PDF</p></div>", unsafe_allow_html=True)
    st.write("")

    if df_customers.empty:
        st.info("No customers available.")
    else:
        st.subheader("✅ Customers CSV")
        st.dataframe(df_customers, use_container_width=True)

        csv_data = df_customers.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Customers CSV", csv_data, "customers.csv", "text/csv")

        st.write("")
        st.subheader("✅ Transactions Report")
        cid = st.selectbox("Select Customer ID", df_customers["ID"].tolist())

        txns = get_transactions(cid)
        df_txn = df_txns_safe(txns)
        st.dataframe(df_txn, use_container_width=True)

        tx_csv = df_txn.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Transactions CSV", tx_csv, f"transactions_customer_{cid}.csv", "text/csv")

        selected_customer = df_customers[df_customers["ID"] == cid].iloc[0]
        if st.button("📄 Generate PDF Report"):
            pdf_file = generate_pdf_report(selected_customer["Name"], selected_customer["Email"], df_txn)
            with open(pdf_file, "rb") as f:
                st.download_button("⬇️ Download PDF", f, file_name=pdf_file)

elif page == "About":
    st.markdown(
        """
        <div class="card">
            <h2>🌟 About CreditPay</h2>
            <p>✅ Built using <b>Streamlit + SQLite</b></p>
            <p>✅ Customer Management, Cards (Luhn), Payments, History & Reports</p>
            <p>✅ Premium Responsive UI (Desktop + Mobile)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================
# BOTTOM NAV (MOBILE)
# =========================================
st.markdown("<div class='bottom-nav'>", unsafe_allow_html=True)
b1, b2, b3, b4 = st.columns(4)

with b1:
    st.button("🏠 Home", on_click=set_page, args=("Dashboard",))
with b2:
    st.button("👤 Users", on_click=set_page, args=("Customers",))
with b3:
    st.button("💰 Pay", on_click=set_page, args=("Payments",))
with b4:
    st.button("📤 Reports", on_click=set_page, args=("Reports",))

st.markdown("</div>", unsafe_allow_html=True)
