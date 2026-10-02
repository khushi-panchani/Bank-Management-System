import json
import random
import string
from pathlib import Path

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SecureBank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #eef2ff 0%,
        #f8fafc 50%,
        #e0f2fe 100%
    );
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}


/* ================= HEADER ================= */

.bank-header {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e3a8a,
        #2563eb
    );

    padding: 35px;
    border-radius: 24px;

    color: white;
    text-align: center;

    margin-bottom: 30px;

    box-shadow:
        0 15px 35px rgba(30, 58, 138, 0.25);
}

.bank-header h1 {
    font-size: 44px;
    font-weight: 800;
    margin: 0;
}

.bank-header p {
    font-size: 17px;
    margin-top: 8px;
    opacity: 0.85;
}


/* ================= WELCOME CARD ================= */

.welcome-card {
    background: rgba(255, 255, 255, 0.95);

    padding: 28px;

    border-radius: 20px;

    margin-bottom: 25px;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.08);

    border: 1px solid #e2e8f0;
}

.welcome-card h2 {
    margin-top: 0;
    color: #0f172a;
}

.welcome-card p {
    color: #64748b;
    font-size: 16px;
}


/* ================= FEATURE CARDS ================= */

.feature-card {
    background: white;

    padding: 25px;

    border-radius: 18px;

    text-align: center;

    min-height: 150px;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.07);

    border: 1px solid #e2e8f0;
}

.feature-icon {
    font-size: 38px;
    margin-bottom: 8px;
}

.feature-title {
    font-size: 19px;
    font-weight: 700;
    color: #0f172a;
}

.feature-text {
    margin-top: 8px;
    font-size: 14px;
    color: #64748b;
}


/* ================= ACCOUNT CARD ================= */

.account-box {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );

    color: white;

    padding: 28px;

    border-radius: 20px;

    text-align: center;

    margin-top: 20px;

    box-shadow:
        0 12px 30px rgba(15, 23, 42, 0.25);
}

.account-label {
    font-size: 15px;
    opacity: 0.75;
}

.account-number {
    font-size: 30px;
    font-weight: 800;
    letter-spacing: 4px;
    margin-top: 8px;
}


/* ================= BALANCE CARD ================= */

.balance-card {
    background: linear-gradient(
        135deg,
        #047857,
        #10b981
    );

    color: white;

    padding: 28px;

    border-radius: 20px;

    margin-bottom: 25px;

    box-shadow:
        0 12px 30px rgba(16, 185, 129, 0.25);
}

.balance-title {
    font-size: 15px;
    opacity: 0.8;
}

.balance-value {
    font-size: 38px;
    font-weight: 800;
    margin-top: 5px;
}


/* ================= INFORMATION CARD ================= */

.info-card {
    background: white;

    padding: 25px;

    border-radius: 18px;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.07);

    border: 1px solid #e2e8f0;
}


/* ================= BUTTONS ================= */

.stButton > button,
.stFormSubmitButton > button {

    width: 100%;

    border-radius: 10px;

    min-height: 45px;

    font-weight: 700;

    border: none;

    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;

    transition: all 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(37, 99, 235, 0.3);
}


/* ================= INPUTS ================= */

.stTextInput input,
.stNumberInput input {

    border-radius: 10px;

    border: 1px solid #cbd5e1;

    min-height: 42px;
}


/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #0f172a,
        #172554
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}


/* ================= SIDEBAR LOGO ================= */

.sidebar-logo {
    text-align: center;
    padding: 15px;
    margin-bottom: 15px;
}

.sidebar-logo-title {
    font-size: 27px;
    font-weight: 800;
}

.sidebar-logo-text {
    font-size: 13px;
    opacity: 0.7;
}


/* ================= FOOTER ================= */

.footer {
    text-align: center;
    margin-top: 40px;
    color: #64748b;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# BANK CLASS
# ============================================================

class Bank:

    database = Path("data.json")
    data = []


    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    @classmethod
    def load_data(cls):

        try:

            if cls.database.exists():

                with open(cls.database, "r") as fs:

                    content = fs.read().strip()

                    if content:
                        cls.data = json.loads(content)
                    else:
                        cls.data = []

                # Convert old integer PINs into strings
                for user in cls.data:
                    user["Pin"] = str(user["Pin"])

            else:

                cls.data = []

        except json.JSONDecodeError:

            st.error(
                "⚠️ data.json contains invalid JSON."
            )

            cls.data = []

        except Exception as err:

            st.error(
                f"⚠️ Error loading database: {err}"
            )

            cls.data = []


    # --------------------------------------------------------
    # SAVE DATA
    # --------------------------------------------------------

    @classmethod
    def update_data(cls):

        try:

            with open(cls.database, "w") as fs:

                json.dump(
                    cls.data,
                    fs,
                    indent=4
                )

        except Exception as err:

            st.error(
                f"⚠️ Error saving data: {err}"
            )


    # --------------------------------------------------------
    # GENERATE ACCOUNT NUMBER
    # --------------------------------------------------------

    @classmethod
    def account_generate(cls):

        while True:

            alpha = random.choices(
                string.ascii_letters,
                k=3
            )

            numbers = random.choices(
                string.digits,
                k=3
            )

            special = random.choices(
                "!@#$%^&*",
                k=1
            )

            account_parts = (
                alpha +
                numbers +
                special
            )

            random.shuffle(account_parts)

            account = "".join(account_parts)

            if not any(
                user["Account"] == account
                for user in cls.data
            ):
                return account


    # --------------------------------------------------------
    # FIND USER
    # --------------------------------------------------------

    @classmethod
    def find_user(cls, account, pin):

        for user in cls.data:

            if (
                user["Account"] == account
                and
                user["Pin"] == pin
            ):

                return user

        return None


    # --------------------------------------------------------
    # VALIDATE PIN
    # --------------------------------------------------------

    @staticmethod
    def validate_pin(pin):

        return (
            len(pin) == 4
            and
            pin.isdigit()
        )


    # --------------------------------------------------------
    # CREATE ACCOUNT
    # --------------------------------------------------------

    @classmethod
    def create_account(
        cls,
        name,
        age,
        email,
        pin
    ):

        if not name.strip():

            return False, "Name cannot be empty."


        if not email.strip():

            return False, "Email cannot be empty."


        if age < 18:

            return (
                False,
                "You must be at least 18 years old."
            )


        if not cls.validate_pin(pin):

            return (
                False,
                "PIN must contain exactly 4 digits."
            )


        account = cls.account_generate()


        user = {

            "Name": name.strip(),

            "Age": int(age),

            "Email": email.strip(),

            "Pin": pin,

            "Account": account,

            "Balance": 0
        }


        cls.data.append(user)

        cls.update_data()


        return True, account


    # --------------------------------------------------------
    # DEPOSIT
    # --------------------------------------------------------

    @classmethod
    def deposit(
        cls,
        account,
        pin,
        amount
    ):

        user = cls.find_user(
            account,
            pin
        )


        if user is None:

            return (
                False,
                "Invalid account number or PIN."
            )


        if amount <= 0:

            return (
                False,
                "Amount must be greater than ₹0."
            )


        if amount > 10000:

            return (
                False,
                "You cannot deposit more than ₹10,000 at once."
            )


        user["Balance"] += amount

        cls.update_data()


        return (
            True,
            f"₹{amount:,.2f} deposited successfully."
        )


    # --------------------------------------------------------
    # WITHDRAW
    # --------------------------------------------------------

    @classmethod
    def withdraw(
        cls,
        account,
        pin,
        amount
    ):

        user = cls.find_user(
            account,
            pin
        )


        if user is None:

            return (
                False,
                "Invalid account number or PIN."
            )


        if amount <= 0:

            return (
                False,
                "Amount must be greater than ₹0."
            )


        if user["Balance"] < amount:

            return (
                False,
                "Insufficient balance."
            )


        user["Balance"] -= amount

        cls.update_data()


        return (
            True,
            f"₹{amount:,.2f} withdrawn successfully."
        )


    # --------------------------------------------------------
    # GET DETAILS
    # --------------------------------------------------------

    @classmethod
    def get_details(
        cls,
        account,
        pin
    ):

        return cls.find_user(
            account,
            pin
        )


    # --------------------------------------------------------
    # UPDATE DETAILS
    # --------------------------------------------------------

    @classmethod
    def update_details(
        cls,
        account,
        pin,
        name,
        email,
        new_pin
    ):

        user = cls.find_user(
            account,
            pin
        )


        if user is None:

            return (
                False,
                "Invalid account number or PIN."
            )


        if name.strip():

            user["Name"] = name.strip()


        if email.strip():

            user["Email"] = email.strip()


        if new_pin.strip():

            if not cls.validate_pin(new_pin):

                return (
                    False,
                    "New PIN must contain exactly 4 digits."
                )

            user["Pin"] = new_pin


        cls.update_data()


        return (
            True,
            "Bank details updated successfully."
        )


    # --------------------------------------------------------
    # DELETE ACCOUNT
    # --------------------------------------------------------

    @classmethod
    def delete_account(
        cls,
        account,
        pin
    ):

        user = cls.find_user(
            account,
            pin
        )


        if user is None:

            return (
                False,
                "Invalid account number or PIN."
            )


        cls.data.remove(user)

        cls.update_data()


        return (
            True,
            "Bank account deleted successfully."
        )


# ============================================================
# LOAD DATABASE
# ============================================================

Bank.load_data()


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="bank-header">

    <h1>🏦 SecureBank</h1>

    <p>Simple • Secure • Smart Banking</p>

</div>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-logo">

        <div class="sidebar-logo-title">
            🏦 SecureBank
        </div>

        <div class="sidebar-logo-text">
            Banking Management System
        </div>

    </div>
    """)

    st.markdown("---")

    choice = st.radio(
        "🏦 Banking Services",
        [
            "Home",
            "Create Account",
            "Deposit Money",
            "Withdraw Money",
            "Show Details",
            "Update Details",
            "Delete Account"
        ]
    )

    st.markdown("---")

    st.caption(
        "🔐 Your banking data is stored locally."
    )


# ============================================================
# HOME
# ============================================================

if choice == "Home":

    st.html("""
    <div class="welcome-card">

        <h2>👋 Welcome to SecureBank</h2>

        <p>
            Manage your bank account easily and securely
            using the services available in the sidebar.
        </p>

    </div>
    """)


    col1, col2, col3 = st.columns(3)


    with col1:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">
                💰
            </div>

            <div class="feature-title">
                Deposit Money
            </div>

            <div class="feature-text">
                Add money to your bank account.
            </div>

        </div>
        """)


    with col2:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">
                💸
            </div>

            <div class="feature-title">
                Withdraw Money
            </div>

            <div class="feature-text">
                Withdraw money from your account.
            </div>

        </div>
        """)


    with col3:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">
                👤
            </div>

            <div class="feature-title">
                Manage Account
            </div>

            <div class="feature-text">
                View and update your account details.
            </div>

        </div>
        """)


    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        "💡 Select an option from the sidebar to get started."
    )


# ============================================================
# CREATE ACCOUNT
# ============================================================

elif choice == "Create Account":

    st.header("🆕 Create New Account")

    st.write(
        "Fill in your details to create a new bank account."
    )


    with st.form("create_account_form"):

        col1, col2 = st.columns(2)


        with col1:

            name = st.text_input(
                "Full Name",
                placeholder="Enter your name"
            )

            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=18
            )


        with col2:

            email = st.text_input(
                "Email",
                placeholder="example@gmail.com"
            )

            pin = st.text_input(
                "4 Digit PIN",
                type="password",
                max_chars=4,
                placeholder="Enter 4 digit PIN"
            )


        submit = st.form_submit_button(
            "🏦 Create Account"
        )


    if submit:

        success, result = Bank.create_account(
            name,
            age,
            email,
            pin
        )


        if success:

            st.success(
                "🎉 Account created successfully!"
            )

            st.html(f"""
            <div class="account-box">

                <div class="account-label">
                    Your Account Number
                </div>

                <div class="account-number">
                    {result}
                </div>

                <div style="
                    margin-top:15px;
                    opacity:0.75;
                ">
                    Please save your account number safely.
                </div>

            </div>
            """)

        else:

            st.error(
                f"❌ {result}"
            )


# ============================================================
# DEPOSIT MONEY
# ============================================================

elif choice == "Deposit Money":

    st.header("💰 Deposit Money")

    st.write(
        "Add money to your bank account."
    )


    with st.form("deposit_form"):

        account = st.text_input(
            "Account Number",
            placeholder="Enter account number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4,
            placeholder="Enter PIN"
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            max_value=10000.0,
            step=100.0
        )

        submit = st.form_submit_button(
            "💰 Deposit Money"
        )


    if submit:

        success, message = Bank.deposit(
            account,
            pin,
            amount
        )


        if success:

            st.success(
                f"✅ {message}"
            )

        else:

            st.error(
                f"❌ {message}"
            )


# ============================================================
# WITHDRAW MONEY
# ============================================================

elif choice == "Withdraw Money":

    st.header("💸 Withdraw Money")

    st.write(
        "Withdraw money from your bank account."
    )


    with st.form("withdraw_form"):

        account = st.text_input(
            "Account Number",
            placeholder="Enter account number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4,
            placeholder="Enter PIN"
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0
        )

        submit = st.form_submit_button(
            "💸 Withdraw Money"
        )


    if submit:

        success, message = Bank.withdraw(
            account,
            pin,
            amount
        )


        if success:

            st.success(
                f"✅ {message}"
            )

        else:

            st.error(
                f"❌ {message}"
            )


# ============================================================
# SHOW DETAILS
# ============================================================

elif choice == "Show Details":

    st.header("👤 Account Details")

    st.write(
        "Enter your account information to view your details."
    )


    with st.form("details_form"):

        account = st.text_input(
            "Account Number",
            placeholder="Enter account number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4,
            placeholder="Enter PIN"
        )

        submit = st.form_submit_button(
            "🔍 Show Details"
        )


    if submit:

        user = Bank.get_details(
            account,
            pin
        )


        if user:

            st.success(
                "✅ Account found!"
            )


            st.html(f"""
            <div class="balance-card">

                <div class="balance-title">
                    Available Balance
                </div>

                <div class="balance-value">
                    ₹{user['Balance']:,.2f}
                </div>

            </div>
            """)


            st.subheader(
                "👤 Personal Information"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**Name:** {user['Name']}"
                )

                st.write(
                    f"**Age:** {user['Age']}"
                )

                st.write(
                    f"**Email:** {user['Email']}"
                )


            with col2:

                st.write(
                    f"**Account Number:** {user['Account']}"
                )

                st.write(
                    "**PIN:** ••••"
                )


        else:

            st.error(
                "❌ Invalid account number or PIN."
            )


# ============================================================
# UPDATE DETAILS
# ============================================================

elif choice == "Update Details":

    st.header("✏️ Update Account Details")

    st.write(
        "Leave a field empty if you don't want to change it."
    )


    with st.form("update_form"):

        account = st.text_input(
            "Account Number",
            placeholder="Enter account number"
        )

        pin = st.text_input(
            "Current PIN",
            type="password",
            max_chars=4,
            placeholder="Enter current PIN"
        )


        st.markdown("### New Details")


        col1, col2 = st.columns(2)


        with col1:

            name = st.text_input(
                "New Name",
                placeholder="Leave empty to keep current name"
            )


        with col2:

            email = st.text_input(
                "New Email",
                placeholder="Leave empty to keep current email"
            )


        new_pin = st.text_input(
            "New PIN",
            type="password",
            max_chars=4,
            placeholder="Leave empty to keep current PIN"
        )


        submit = st.form_submit_button(
            "✏️ Update Details"
        )


    if submit:

        success, message = Bank.update_details(
            account,
            pin,
            name,
            email,
            new_pin
        )


        if success:

            st.success(
                f"✅ {message}"
            )

        else:

            st.error(
                f"❌ {message}"
            )


# ============================================================
# DELETE ACCOUNT
# ============================================================

elif choice == "Delete Account":

    st.header("🗑️ Delete Account")

    st.warning(
        "⚠️ Warning: Account deletion is permanent."
    )


    with st.form("delete_form"):

        account = st.text_input(
            "Account Number",
            placeholder="Enter account number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4,
            placeholder="Enter PIN"
        )

        confirm = st.checkbox(
            "I understand that my account will be permanently deleted."
        )

        submit = st.form_submit_button(
            "🗑️ Delete Account"
        )


    if submit:

        if not confirm:

            st.error(
                "❌ Please confirm the deletion first."
            )

        else:

            success, message = Bank.delete_account(
                account,
                pin
            )


            if success:

                st.success(
                    f"✅ {message}"
                )

                st.balloons()

            else:

                st.error(
                    f"❌ {message}"
                )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    🏦 SecureBank Management System
    <br>
    Built with Python + OOP + JSON + Streamlit

</div>
""")