import streamlit as st
import re
import random
import string

def generate_password(user_chars=''):
    # Define default character sets for each category
    if user_chars !="" and len(user_chars) <6:
          st.error(f"Your Suggested Character count must be greater then 5")
    else:     
        default_upper = string.ascii_uppercase
        default_lower = string.ascii_lowercase
        default_digits = string.digits
        default_special = "!@#$%^&*"  # Restrict special characters

        # Determine the allowed characters based on user input
        allowed_chars = user_chars if user_chars else default_upper + default_lower + default_digits + default_special

        # Extract characters from each category from the allowed characters
        upper_chars = re.findall(r'[A-Z]', allowed_chars) or list(default_upper)
        lower_chars = re.findall(r'[a-z]', allowed_chars) or list(default_lower)
        digit_chars = re.findall(r'\d', allowed_chars) or list(default_digits)
        special_chars = re.findall(r'[!@#$%^&*]', allowed_chars) or list(default_special)

        # Generate a random password length between 10 and 15
        password_length = random.randint(10, 15)

        # Ensure at least one character from each category
        required = [
            random.choice(upper_chars),
            random.choice(lower_chars),
            random.choice(digit_chars),
            random.choice(special_chars)
        ]

        # Calculate remaining characters needed
        remaining_length = password_length - 4
        remaining_chars = list(allowed_chars)
        remaining = [random.choice(remaining_chars) for _ in range(remaining_length)]

        # Combine and shuffle
        password_list = required + remaining
        random.shuffle(password_list)

        return ''.join(password_list)

def check_password_strength(password):
    score = 0

    # Length Check
    if len(password) >= 8:
        score += 1
        st.success("✔️ Password is at least 8 characters long.")
    else:
        st.error("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
        st.success("✔️ Password contains both uppercase and lowercase letters.")
    else:
        st.error("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
        st.success("✔️ Password contains at least one number.")
    else:
        st.error("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
        st.success("✔️ Password contains at least one special character.")
    else:
        st.error("❌ Include at least one special character (!@#$%^&*).")

    # Strength Rating
    if score == 4:
        st.success("✅ Strong Password!")
    elif score == 3:
        st.warning("⚠️ Moderate Password - Consider adding more security features.")
    else:
        st.error("❌ Weak Password - Improve it using the suggestions above.")

# Initialize session state
if 'generated_password' not in st.session_state:
    st.session_state.generated_password = ""

st.set_page_config("Password Strength Checker", page_icon="🔐", layout="wide")
st.header("🔐 Password Strength Meter")

# Password input field (re-runs app on every keystroke)
password = st.text_input("Enter Password Here for strength measuring:")

# If a password is provided, check its strength immediately
if password:
    check_password_strength(password)

# Two columns for Generate buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Random Password"):
        st.session_state.generated_password = generate_password()

with col2:
    custom_chars = st.text_input("Enter Your Characters:", key="custom_input")
    if st.button("Generate Password with Custom Characters"):
        if custom_chars:
            st.session_state.generated_password = generate_password(custom_chars)
        else:
            st.warning("Please enter custom characters.")

# Show the generated password
if st.session_state.generated_password:
    st.success(f"🔑 Generated Password: `{st.session_state.generated_password}`")
