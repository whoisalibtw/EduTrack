
import re
import streamlit as st

from database import create_user, authenticate_user


def show_signup():

    st.subheader("Create Your Account")
    st.write("Register to access the EduTrack dashboard.")

    with st.form("signup_form"):

        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input(
            "Confirm Password", type="password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

    if submitted:

        full_name = full_name.strip()
        email = email.strip().lower()

        if not full_name or not email or not password or not confirm_password:
            st.error("Please fill in all fields.")

        elif len(full_name) < 2:
            st.error("Please enter a valid full name.")

        elif not re.fullmatch(
            r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", email
        ):
            st.error("Please enter a valid email address.")

        elif len(password) < 8:
            st.error("Password must contain at least 8 characters.")

        elif not any(c.isupper() for c in password):
            st.error("Password must contain an uppercase letter.")

        elif not any(c.islower() for c in password):
            st.error("Password must contain a lowercase letter.")

        elif not any(c.isdigit() for c in password):
            st.error("Password must contain a number.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        else:

            created = create_user(full_name, email, password)

            if created:
                st.success("Account created successfully! Please log in.")
            else:
                st.error("This email address is already registered.")


def show_login():

    st.subheader("Welcome Back")
    st.write("Log in to access your EduTrack account.")

    with st.form("login_form"):

        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if submitted:

        email = email.strip().lower()

        if not email or not password:
            st.error("Please enter both email and password.")

        else:

            success, user = authenticate_user(email, password)

            if success:

                st.session_state["authenticated"] = True
                st.session_state["user"] = user

                st.rerun()

            else:
                st.error("Invalid email or password.")
