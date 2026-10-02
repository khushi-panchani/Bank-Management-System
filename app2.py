import json
import random
import string
from pathlib import Path

import streamlit as st


class Bank:

    database = Path("data.json")
    data = []

    # -----------------------------
    # Load existing data
    # -----------------------------
    @classmethod
    def load_data(cls):

        try:
            if cls.database.exists():

                with open(cls.database, "r") as fs:
                    cls.data = json.load(fs)

                # Convert old integer PINs to strings
                # This helps if your old data.json has PINs like 1234
                for user in cls.data:
                    user["Pin"] = str(user["Pin"])

            else:
                cls.data = []

        except json.JSONDecodeError:
            st.error("data.json contains invalid JSON.")
            cls.data = []

        except Exception as err:
            st.error(f"Error loading data: {err}")
            cls.data = []

    # -----------------------------
    # Save data
    # -----------------------------
    @classmethod
    def update_data(cls):

        try:
            with open(cls.database, "w") as fs:
                json.dump(cls.data, fs, indent=4)

        except Exception as err:
            st.error(f"Error saving data: {err}")

    # -----------------------------
    # Generate Account Number
    # -----------------------------
    @classmethod
    def account_generate(cls):

        while True:

            alpha = random.choices(string.ascii_letters, k=3)
            num = random.choices(string.digits, k=3)
            special = random.choices("!@#$%^&*", k=1)

            account_id = alpha + num + special

            random.shuffle(account_id)

            account = "".join(account_id)

            # Make sure account number is unique
            if not any(user["Account"] == account for user in cls.data):
                return account

    # -----------------------------
    # Find User
    # -----------------------------
    @classmethod
    def find_user(cls, account, pin):

        for user in cls.data:

            if user["Account"] == account and user["Pin"] == pin:
                return user

        return None

    # -----------------------------
    # Validate PIN
    # -----------------------------
    @staticmethod
    def validate_pin(pin):

        return len(pin) == 4 and pin.isdigit()

    # -----------------------------
    # Create Account
    # -----------------------------
    @classmethod
    def create_account(cls, name, age, email, pin):

        if not name.strip():
            return False, "Name cannot be empty."

        if age < 18:
            return False, "You must be at least 18 years old."

        if not cls.validate_pin(pin):
            return False, "PIN must contain exactly 4 digits."

        account = cls.account_generate()

        user = {
            "Name": name.strip(),
            "Age": age,
            "Email": email.strip(),
            "Pin": pin,
            "Account": account,
            "Balance": 0
        }

        cls.data.append(user)
        cls.update_data()

        return True, account

    # -----------------------------
    # Deposit Money
    # -----------------------------
    @classmethod
    def deposit(cls, account, pin, amount):

        user = cls.find_user(account, pin)

        if user is None:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Amount must be greater than 0."

        if amount > 10000:
            return False, "You cannot deposit more than ₹10,000 at once."

        user["Balance"] += amount

        cls.update_data()

        return True, f"₹{amount} deposited successfully."

    # -----------------------------
    # Withdraw Money
    # -----------------------------
    @classmethod
    def withdraw(cls, account, pin, amount):

        user = cls.find_user(account, pin)

        if user is None:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Amount must be greater than 0."

        if user["Balance"] < amount:
            return False, "Insufficient balance."

        user["Balance"] -= amount

        cls.update_data()

        return True, f"₹{amount} withdrawn successfully."

    # -----------------------------
    # Get User Details
    # -----------------------------
    @classmethod
    def get_details(cls, account, pin):

        user = cls.find_user(account, pin)

        if user is None:
            return None

        return user

    # -----------------------------
    # Update User Details
    # -----------------------------
    @classmethod
    def update_details(
        cls,
        account,
        pin,
        name,
        email,
        new_pin
    ):

        user = cls.find_user(account, pin)

        if user is None:
            return False, "Invalid account number or PIN."

        if not name.strip():
            return False, "Name cannot be empty."

        if not cls.validate_pin(new_pin):
            return False, "New PIN must contain exactly 4 digits."

        user["Name"] = name.strip()
        user["Email"] = email.strip()
        user["Pin"] = new_pin

        cls.update_data()

        return True, "Bank details updated successfully."

    # -----------------------------
    # Delete Account
    # -----------------------------
    @classmethod
    def delete_account(cls, account, pin):

        user = cls.find_user(account, pin)

        if user is None:
            return False, "Invalid account number or PIN."

        cls.data.remove(user)

        cls.update_data()

        return True, "Bank account deleted successfully."


# Load data when application starts
Bank.load_data()


# =====================================================
# STREAMLIT UI
# =====================================================

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Bank Management System")
st.write("Manage your bank account easily.")


# Sidebar
st.sidebar.title("Bank Menu")

choice = st.sidebar.radio(
    "Select an Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Details",
        "Update Details",
        "Delete Account"
    ]
)


# =====================================================
# CREATE ACCOUNT
# =====================================================

if choice == "Create Account":

    st.header("Create New Account")

    with st.form("create_account_form"):

        name = st.text_input("Full Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18
        )

        email = st.text_input("Email")

        pin = st.text_input(
            "4 Digit PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button("Create Account")

    if submit:

        success, result = Bank.create_account(
            name,
            age,
            email,
            pin
        )

        if success:

            st.success("Account created successfully!")

            st.info(
                f"Your Account Number is: **{result}**"
            )

            st.warning(
                "Please save your Account Number safely."
            )

        else:
            st.error(result)


# =====================================================
# DEPOSIT
# =====================================================

elif choice == "Deposit Money":

    st.header("💰 Deposit Money")

    with st.form("deposit_form"):

        account = st.text_input("Account Number")

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0
        )

        submit = st.form_submit_button("Deposit")

    if submit:

        success, message = Bank.deposit(
            account,
            pin,
            amount
        )

        if success:
            st.success(message)
        else:
            st.error(message)


# =====================================================
# WITHDRAW
# =====================================================

elif choice == "Withdraw Money":

    st.header("💸 Withdraw Money")

    with st.form("withdraw_form"):

        account = st.text_input("Account Number")

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0
        )

        submit = st.form_submit_button("Withdraw")

    if submit:

        success, message = Bank.withdraw(
            account,
            pin,
            amount
        )

        if success:
            st.success(message)
        else:
            st.error(message)


# =====================================================
# SHOW DETAILS
# =====================================================

elif choice == "Show Details":

    st.header("👤 Account Details")

    with st.form("details_form"):

        account = st.text_input("Account Number")

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button("Show Details")

    if submit:

        user = Bank.get_details(account, pin)

        if user:

            st.success("Account found!")

            st.write("### Your Information")

            st.write(f"**Name:** {user['Name']}")
            st.write(f"**Age:** {user['Age']}")
            st.write(f"**Email:** {user['Email']}")
            st.write(f"**Account Number:** {user['Account']}")
            st.write(f"**Balance:** ₹{user['Balance']}")

        else:
            st.error("Invalid account number or PIN.")


# =====================================================
# UPDATE DETAILS
# =====================================================

elif choice == "Update Details":

    st.header("✏️ Update Account Details")

    with st.form("update_form"):

        account = st.text_input("Account Number")

        pin = st.text_input(
            "Current PIN",
            type="password",
            max_chars=4
        )

        name = st.text_input("New Name")

        email = st.text_input("New Email")

        new_pin = st.text_input(
            "New PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button("Update Details")

    if submit:

        success, message = Bank.update_details(
            account,
            pin,
            name,
            email,
            new_pin
        )

        if success:
            st.success(message)
        else:
            st.error(message)


# =====================================================
# DELETE ACCOUNT
# =====================================================

elif choice == "Delete Account":

    st.header("🗑️ Delete Account")

    st.warning(
        "⚠️ Deleting your account is permanent."
    )

    with st.form("delete_form"):

        account = st.text_input("Account Number")

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        confirm = st.checkbox(
            "I understand that my account will be permanently deleted."
        )

        submit = st.form_submit_button("Delete Account")

    if submit:

        if not confirm:
            st.error(
                "Please confirm that you want to delete the account."
            )

        else:

            success, message = Bank.delete_account(
                account,
                pin
            )

            if success:
                st.success(message)
            else:
                st.error(message)