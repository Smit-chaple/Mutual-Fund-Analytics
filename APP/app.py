import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Mutual Fund Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Find database automatically
possible_db_paths = [
    BASE_DIR / "SQL" / "bluestoke_mf.db",
    BASE_DIR / "SQL" / "bluestock_mf.db",
    BASE_DIR / "sql" / "bluestoke_mf.db",
    BASE_DIR / "sql" / "bluestock_mf.db",
    BASE_DIR / "bluestoke_mf.db",
    BASE_DIR / "bluestock_mf.db"
]

DB_PATH = next(
    (path for path in possible_db_paths if path.is_file()),
    None
)

if DB_PATH is None:
    st.error("❌ SQLite database file not found.")
    st.stop()

# ============================================================
# DATABASE HELPER
# ============================================================

def get_connection():
    return sqlite3.connect(str(DB_PATH))

# ============================================================
# LOAD SMALL / DIMENSION TABLES
# ============================================================

@st.cache_data(ttl=300)
def load_funds():

    con = get_connection()

    try:
        return pd.read_sql_query(
            "SELECT * FROM dim_fund",
            con
        )
    finally:
        con.close()


# ============================================================
# LOAD TABLE ONLY WHEN REQUIRED
# ============================================================

@st.cache_data(ttl=300)
def load_aum():

    con = get_connection()

    try:
        return pd.read_sql_query(
            "SELECT * FROM fact_aum",
            con
        )
    finally:
        con.close()


@st.cache_data(ttl=300)
def load_performance():

    con = get_connection()

    try:
        return pd.read_sql_query(
            "SELECT * FROM fact_performance",
            con
        )
    finally:
        con.close()


@st.cache_data(ttl=300)
def load_transactions():

    con = get_connection()

    try:
        return pd.read_sql_query(
            "SELECT * FROM fact_transactions",
            con
        )
    finally:
        con.close()


@st.cache_data(ttl=300)
def load_sip():

    con = get_connection()

    try:
        return pd.read_sql_query(
            "SELECT * FROM fact_sip",
            con
        )
    finally:
        con.close()


# ============================================================
# NAV LOADER
# IMPORTANT:
# Load only required NAV records.
# ============================================================

@st.cache_data(ttl=300)
def load_nav():

    con = get_connection()

    try:

        return pd.read_sql_query(
            """
            SELECT
                amfi_code,
                date,
                nav
            FROM fact_nav
            """,
            con
        )

    finally:
        con.close()


# ============================================================
# LOAD FUND MASTER
# ============================================================

try:

    funds = load_funds()

except Exception as e:

    st.error(
        f"❌ Unable to load fund master: {e}"
    )

    st.stop()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(df, possible_columns):

    for column in possible_columns:

        if column in df.columns:
            return column

    return None


def convert_date(df, possible_columns):

    df = df.copy()

    column = find_column(
        df,
        possible_columns
    )

    if column:

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df, column


# ============================================================
# HEADER
# ============================================================

st.title(
    "📊 Mutual Fund Analytics Dashboard"
)

st.caption(
    "ETL Pipeline • SQLite • Live NAV • Performance Analytics • Investor Analytics"
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("📌 Dashboard")

page = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Industry Overview",
        "📈 Fund Performance",
        "👥 Investor Analytics",
        "💰 SIP & Market Trends"
    ]
)

# ============================================================
# DATABASE STATUS
# ============================================================

with st.sidebar.expander("🗄️ Database Status"):

    st.success("Database connected")

    st.caption(
        f"Database: {DB_PATH.name}"
    )

    st.write(
        f"Funds: **{len(funds):,}**"
    )


# ============================================================
# GLOBAL FILTERS
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("🔎 Filters")

fund_house_column = find_column(
    funds,
    ["fund_house"]
)

category_column = find_column(
    funds,
    ["category"]
)

amfi_column = find_column(
    funds,
    ["amfi_code"]
)

scheme_column = find_column(
    funds,
    ["scheme_name"]
)


if fund_house_column:

    fund_houses = sorted(
        funds[fund_house_column]
        .dropna()
        .unique()
        .tolist()
    )

else:

    fund_houses = []


if category_column:

    categories = sorted(
        funds[category_column]
        .dropna()
        .unique()
        .tolist()
    )

else:

    categories = []


selected_house = st.sidebar.selectbox(
    "Fund House",
    ["All"] + fund_houses
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + categories
)


filtered_funds = funds.copy()


if (
    selected_house != "All"
    and fund_house_column
):

    filtered_funds = filtered_funds[
        filtered_funds[fund_house_column]
        == selected_house
    ]


if (
    selected_category != "All"
    and category_column
):

    filtered_funds = filtered_funds[
        filtered_funds[category_column]
        == selected_category
    ]


if amfi_column:

    selected_codes = (
        filtered_funds[amfi_column]
        .dropna()
        .tolist()
    )

else:

    selected_codes = []


# ============================================================
# PAGE 1 — INDUSTRY OVERVIEW
# ============================================================

if page == "🏠 Industry Overview":

    st.header(
        "🏠 Industry Overview"
    )

    # Load AUM only on this page
    try:

        aum = load_aum()

    except Exception as e:

        st.error(
            f"Unable to load AUM data: {e}"
        )

        aum = pd.DataFrame()


    aum_column = find_column(
        aum,
        [
            "aum_crore",
            "aum_lakh_crore",
            "aum"
        ]
    )


    aum, aum_date = convert_date(
        aum,
        ["date", "month"]
    )


    if (
        aum_column
        and not aum.empty
    ):

        total_aum = aum[
            aum_column
        ].sum()

    else:

        total_aum = None


    # ========================================================
    # KPI
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Funds",
        f"{len(filtered_funds):,}"
    )


    col2.metric(
        "Fund Houses",
        (
            f"{filtered_funds[fund_house_column].nunique():,}"
            if fund_house_column
            else "—"
        )
    )


    col3.metric(
        "Categories",
        (
            f"{filtered_funds[category_column].nunique():,}"
            if category_column
            else "—"
        )
    )


    col4.metric(
        "Total AUM",
        (
            f"{total_aum:,.2f}"
            if total_aum is not None
            else "—"
        )
    )


    st.divider()


    # ========================================================
    # AUM TREND
    # ========================================================

    if (
        not aum.empty
        and aum_column
        and aum_date
    ):

        st.subheader(
            "📈 AUM Trend"
        )


        aum_trend = (
            aum
            .dropna(
                subset=[aum_date]
            )
            .groupby(aum_date)[aum_column]
            .sum()
            .sort_index()
        )


        st.line_chart(
            aum_trend,
            use_container_width=True
        )


    # ========================================================
    # AUM BY FUND HOUSE
    # ========================================================

    if (
        not aum.empty
        and aum_column
        and "fund_house" in aum.columns
    ):

        st.subheader(
            "🏦 AUM by Fund House"
        )


        house_aum = (
            aum
            .groupby(
                "fund_house"
            )[aum_column]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
        )


        st.bar_chart(
            house_aum,
            use_container_width=True
        )


    # ========================================================
    # FUND EXPLORER
    # ========================================================

    st.subheader(
        "📋 Fund Explorer"
    )


    st.write(
        f"Showing **{len(filtered_funds):,}** funds"
    )


    st.dataframe(
        filtered_funds,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 2 — FUND PERFORMANCE
# ============================================================

elif page == "📈 Fund Performance":

    st.header(
        "📈 Fund Performance"
    )

    # Load performance only on this page
    try:

        performance = load_performance()

    except Exception as e:

        st.error(
            f"Unable to load performance data: {e}"
        )

        performance = pd.DataFrame()


    # Filter performance
    if (
        amfi_column
        and "amfi_code" in performance.columns
    ):

        filtered_performance = performance[
            performance["amfi_code"].isin(
                selected_codes
            )
        ].copy()

    else:

        filtered_performance = performance.copy()


    sharpe_column = find_column(
        filtered_performance,
        [
            "sharpe_ratio",
            "sharpe"
        ]
    )


    return_column = find_column(
        filtered_performance,
        [
            "CAGR_1Y",
            "cagr_1yr",
            "annual_return",
            "return_pct"
        ]
    )


    volatility_column = find_column(
        filtered_performance,
        [
            "annualized_volatility",
            "volatility",
            "risk"
        ]
    )


    # ========================================================
    # KPI
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Selected Funds",
        f"{len(filtered_funds):,}"
    )


    col2.metric(
        "Performance Records",
        f"{len(filtered_performance):,}"
    )


    if (
        sharpe_column
        and not filtered_performance.empty
    ):

        col3.metric(
            "Average Sharpe",
            f"{filtered_performance[sharpe_column].mean():.2f}"
        )

    else:

        col3.metric(
            "Average Sharpe",
            "—"
        )


    if (
        return_column
        and not filtered_performance.empty
    ):

        col4.metric(
            "Average Return",
            f"{filtered_performance[return_column].mean():.2f}%"
        )

    else:

        col4.metric(
            "Average Return",
            "—"
        )


    st.divider()


    # ========================================================
    # PERFORMANCE TABLE
    # ========================================================

    st.subheader(
        "🏆 Fund Performance Scorecard"
    )


    st.dataframe(
        filtered_performance,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # RISK VS RETURN
    # ========================================================

    if (
        return_column
        and volatility_column
    ):

        risk_return = (
            filtered_performance[
                [
                    return_column,
                    volatility_column
                ]
            ]
            .dropna()
        )


        if not risk_return.empty:

            st.subheader(
                "⚖️ Risk vs Return"
            )


            st.scatter_chart(
                risk_return,
                x=volatility_column,
                y=return_column,
                use_container_width=True
            )


    # ========================================================
    # NAV
    # ========================================================

    st.subheader(
        "📊 NAV Trend"
    )


    try:

        nav = load_nav()

        nav, nav_date = convert_date(
            nav,
            ["date", "nav_date"]
        )


        # Only selected funds
        if (
            amfi_column
            and "amfi_code" in nav.columns
        ):

            nav = nav[
                nav["amfi_code"].isin(
                    selected_codes
                )
            ].copy()


        if (
            not nav.empty
            and nav_date
            and scheme_column
        ):

            nav = nav.merge(
                filtered_funds[
                    [
                        amfi_column,
                        scheme_column
                    ]
                ],
                on=amfi_column,
                how="left"
            )


            nav_pivot = (
                nav
                .pivot_table(
                    index=nav_date,
                    columns=scheme_column,
                    values="nav",
                    aggfunc="last"
                )
                .sort_index()
            )


            st.line_chart(
                nav_pivot,
                use_container_width=True
            )

        else:

            st.info(
                "NAV data is not available for the selected filters."
            )


    except Exception as e:

        st.warning(
            f"NAV chart unavailable: {e}"
        )


# ============================================================
# PAGE 3 — INVESTOR ANALYTICS
# ============================================================

elif page == "👥 Investor Analytics":

    st.header(
        "👥 Investor Analytics"
    )


    # Load only when page is opened
    try:

        transactions = load_transactions()

    except Exception as e:

        st.error(
            f"Unable to load transaction data: {e}"
        )

        transactions = pd.DataFrame()


    if transactions.empty:

        st.warning(
            "Investor transaction data is not available."
        )

    else:

        amount_column = find_column(
            transactions,
            [
                "amount",
                "transaction_amount",
                "transaction_value",
                "sip_amount"
            ]
        )


        type_column = find_column(
            transactions,
            [
                "transaction_type",
                "type",
                "txn_type"
            ]
        )


        state_column = find_column(
            transactions,
            [
                "state",
                "investor_state"
            ]
        )


        transactions, transaction_date = convert_date(
            transactions,
            [
                "date",
                "transaction_date"
            ]
        )


        # ====================================================
        # KPI
        # ====================================================

        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Transactions",
            f"{len(transactions):,}"
        )


        if amount_column:

            col2.metric(
                "Transaction Value",
                f"{transactions[amount_column].sum():,.2f}"
            )

        else:

            col2.metric(
                "Transaction Value",
                "—"
            )


        if type_column:

            col3.metric(
                "Transaction Types",
                f"{transactions[type_column].nunique():,}"
            )

        else:

            col3.metric(
                "Transaction Types",
                "—"
            )


        st.divider()


        # ====================================================
        # TRANSACTION TYPES
        # ====================================================

        if (
            type_column
            and amount_column
        ):

            st.subheader(
                "💳 Transaction Type Analysis"
            )


            transaction_summary = (
                transactions
                .groupby(
                    type_column
                )[amount_column]
                .sum()
                .sort_values(
                    ascending=False
                )
            )


            st.bar_chart(
                transaction_summary,
                use_container_width=True
            )


        # ====================================================
        # STATE
        # ====================================================

        if (
            state_column
            and amount_column
        ):

            st.subheader(
                "🗺️ State-wise Investment"
            )


            state_summary = (
                transactions
                .groupby(
                    state_column
                )[amount_column]
                .sum()
                .sort_values(
                    ascending=False
                )
                .head(15)
            )


            st.bar_chart(
                state_summary,
                use_container_width=True
            )


        # ====================================================
        # MONTHLY TREND
        # ====================================================

        if (
            transaction_date
            and amount_column
        ):

            st.subheader(
                "📅 Monthly Transaction Trend"
            )


            monthly_transactions = (
                transactions
                .dropna(
                    subset=[
                        transaction_date
                    ]
                )
                .set_index(
                    transaction_date
                )[amount_column]
                .resample("ME")
                .sum()
            )


            st.line_chart(
                monthly_transactions,
                use_container_width=True
            )


        # ====================================================
        # DATA
        # ====================================================

        with st.expander(
            "📋 View Transaction Data"
        ):

            st.dataframe(
                transactions,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# PAGE 4 — SIP & MARKET TRENDS
# ============================================================

else:

    st.header(
        "💰 SIP & Market Trends"
    )


    # Load only when required
    try:

        sip = load_sip()

    except Exception as e:

        st.error(
            f"Unable to load SIP data: {e}"
        )

        sip = pd.DataFrame()


    if sip.empty:

        st.warning(
            "SIP data is not available."
        )

    else:

        sip, sip_date = convert_date(
            sip,
            [
                "month",
                "date"
            ]
        )


        sip_column = find_column(
            sip,
            [
                "sip_inflow_crore",
                "sip_inflow",
                "sip_amount",
                "amount"
            ]
        )


        accounts_column = find_column(
            sip,
            [
                "active_sip_accounts_crore",
                "active_sip_accounts",
                "sip_accounts",
                "active_accounts"
            ]
        )


        sip_category_column = find_column(
            sip,
            [
                "category",
                "fund_category"
            ]
        )


        # ====================================================
        # KPI
        # ====================================================

        col1, col2, col3 = st.columns(3)


        col1.metric(
            "SIP Records",
            f"{len(sip):,}"
        )


        if sip_column:

            col2.metric(
                "Total SIP Inflow",
                f"{sip[sip_column].sum():,.2f}"
            )


            if sip_date:

                latest_sip = (
                    sip
                    .dropna(
                        subset=[sip_date]
                    )
                    .sort_values(
                        sip_date
                    )
                )


                if not latest_sip.empty:

                    col3.metric(
                        "Latest SIP Inflow",
                        f"{latest_sip[sip_column].iloc[-1]:,.2f}"
                    )

                else:

                    col3.metric(
                        "Latest SIP Inflow",
                        "—"
                    )

            else:

                col3.metric(
                    "Latest SIP Inflow",
                    "—"
                )

        else:

            col2.metric(
                "Total SIP Inflow",
                "—"
            )

            col3.metric(
                "Latest SIP Inflow",
                "—"
            )


        st.divider()


        # ====================================================
        # SIP TREND
        # ====================================================

        if (
            sip_date
            and sip_column
        ):

            st.subheader(
                "📈 Monthly SIP Inflow"
            )


            sip_trend = (
                sip
                .dropna(
                    subset=[sip_date]
                )
                .sort_values(
                    sip_date
                )
                .set_index(
                    sip_date
                )[sip_column]
            )


            st.line_chart(
                sip_trend,
                use_container_width=True
            )


        # ====================================================
        # ACTIVE SIP ACCOUNTS
        # ====================================================

        if (
            sip_date
            and accounts_column
        ):

            st.subheader(
                "👥 Active SIP Accounts"
            )


            accounts_trend = (
                sip
                .dropna(
                    subset=[sip_date]
                )
                .sort_values(
                    sip_date
                )
                .set_index(
                    sip_date
                )[accounts_column]
            )


            st.line_chart(
                accounts_trend,
                use_container_width=True
            )


        # ====================================================
        # CATEGORY
        # ====================================================

        if (
            sip_category_column
            and sip_column
        ):

            st.subheader(
                "📊 SIP Inflow by Category"
            )


            category_summary = (
                sip
                .groupby(
                    sip_category_column
                )[sip_column]
                .sum()
                .sort_values(
                    ascending=False
                )
            )


            st.bar_chart(
                category_summary,
                use_container_width=True
            )


        # ====================================================
        # DATA
        # ====================================================

        with st.expander(
            "📋 View SIP Data"
        ):

            st.dataframe(
                sip,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Mutual Fund Analytics | SQLite + Python + Streamlit | "
    "ETL + Live NAV + Automated Email Reporting"
)