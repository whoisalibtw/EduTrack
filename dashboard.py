
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# Dataset location
DATA_PATH = Path(__file__).resolve().parent / "data" / "student_data.csv"


@st.cache_data
def load_data():
    """Load the student dataset."""

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

    return df


def show_overview(df):

    st.title("EduTrack Dashboard")
    st.write("Student Dropout Risk & Academic Success Analytics")

    st.info(
        "Explore student academic outcomes and monitor "
        "important education statistics."
    )

    # Calculate student statistics
    total = len(df)
    outcomes = df["Target"].value_counts()

    graduates = outcomes.get("Graduate", 0)
    dropouts = outcomes.get("Dropout", 0)
    enrolled = outcomes.get("Enrolled", 0)

    # Display statistics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", f"{total:,}")
    col2.metric("Graduates", f"{graduates:,}")
    col3.metric("Dropouts", f"{dropouts:,}")
    col4.metric("Enrolled", f"{enrolled:,}")

    st.divider()

    # Outcome distribution
    st.subheader("Academic Outcome Distribution")

    outcome_df = outcomes.reset_index()
    outcome_df.columns = ["Outcome", "Students"]

    fig = px.bar(
        outcome_df,
        x="Outcome",
        y="Students",
        color="Outcome",
        text="Students",
        title="Student Academic Outcomes"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Age distribution
    st.subheader("Student Age Distribution")

    age_fig = px.histogram(
        df,
        x="Age at enrollment",
        nbins=20,
        title="Students by Age at Enrollment"
    )

    st.plotly_chart(age_fig, use_container_width=True)


def show_data_explorer(df):

    st.title("Student Data Explorer")

    st.write(
        "Explore the student dataset using filters "
        "and view individual student records."
    )

    # Outcome filter
    outcomes = sorted(df["Target"].unique().tolist())

    selected_outcomes = st.multiselect(
        "Select Academic Outcomes",
        options=outcomes,
        default=outcomes
    )

    # Age filter
    min_age = int(df["Age at enrollment"].min())
    max_age = int(df["Age at enrollment"].max())

    age_range = st.slider(
        "Select Student Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )

    # Apply filters
    filtered_df = df[
        (df["Target"].isin(selected_outcomes)) &
        (df["Age at enrollment"].between(
            age_range[0], age_range[1]
        ))
    ]

    st.metric("Filtered Student Records", len(filtered_df))

    # Display records
    st.subheader("Student Records")

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )

    # Filtered visualization
    st.subheader("Filtered Academic Outcomes")

    if not filtered_df.empty:

        fig = px.histogram(
            filtered_df,
            x="Age at enrollment",
            color="Target",
            barmode="overlay",
            title="Age Distribution by Academic Outcome"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No student records match your filters.")


def show_prediction_demo(df):

    st.title("Student Risk Prediction Demo")

    st.write(
        "Enter student academic information to demonstrate "
        "a simulated academic outcome prediction."
    )

    st.warning(
        "Demo Mode: These predictions use predefined rules. "
        "No trained machine learning model is being used."
    )

    min_age = int(df["Age at enrollment"].min())
    max_age = int(df["Age at enrollment"].max())

    with st.form("prediction_form"):

        age = st.number_input(
            "Student Age",
            min_value=min_age,
            max_value=max_age,
            value=min(max(22, min_age), max_age)
        )

        first_sem = st.number_input(
            "First Semester Approved Units",
            min_value=0,
            max_value=30,
            value=5
        )

        second_sem = st.number_input(
            "Second Semester Approved Units",
            min_value=0,
            max_value=30,
            value=5
        )

        tuition = st.selectbox(
            "Are Tuition Fees Up to Date?",
            ["Yes", "No"]
        )

        submitted = st.form_submit_button(
            "Predict Academic Outcome",
            use_container_width=True
        )

    if submitted:

        # Simple predefined demonstration rules
        risk_score = 0
        reasons = []

        if tuition == "No":
            risk_score += 40
            reasons.append("Tuition fees are not up to date.")

        if first_sem < 3:
            risk_score += 20
            reasons.append(
                "Low number of approved first semester units."
            )

        if second_sem < 3:
            risk_score += 20
            reasons.append(
                "Low number of approved second semester units."
            )

        if age >= 30:
            risk_score += 10
            reasons.append(
                "Student is in a higher age group."
            )

        risk_score = min(risk_score, 100)

        # Demonstration classification
        if risk_score >= 60:
            prediction = "Dropout"
            category = "High Risk"

        elif risk_score >= 30:
            prediction = "Enrolled"
            category = "Moderate Risk"

        else:
            prediction = "Graduate"
            category = "Low Risk"

        st.divider()

        st.subheader("Prediction Results")

        col1, col2 = st.columns(2)

        col1.metric("Predicted Outcome", prediction)
        col2.metric("Illustrative Risk Score", f"{risk_score}/100")

        st.write("Risk Indicator")
        st.progress(risk_score / 100)

        st.info(f"Risk Category: {category}")

        st.subheader("Assessment Details")

        if reasons:

            for reason in reasons:
                st.write("- " + reason)

        else:
            st.success(
                "No risk indicators were triggered by "
                "the demonstration rules."
            )

        st.caption(
            "This is an illustrative rule-based demonstration, "
            "not a validated prediction or probability."
        )


def show_dashboard(user):

    # Load dataset
    try:
        df = load_data()

        required_columns = [
            "Target",
            "Age at enrollment",
            "Curricular units 1st sem (approved)",
            "Curricular units 2nd sem (approved)",
            "Tuition fees up to date"
        ]

        missing_columns = [
            column for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            st.error(
                "Required dataset columns are missing: "
                + ", ".join(missing_columns)
            )
            return

    except Exception as error:
        st.error(f"Unable to load the dataset: {error}")
        return

    # Sidebar navigation
    st.sidebar.title("EduTrack")

    st.sidebar.write("Student Analytics Platform")

    st.sidebar.divider()

    st.sidebar.write(
        f"Welcome, {user.get('full_name', 'Student')}"
    )

    page = st.sidebar.selectbox(
        "Navigation",
        [
            "Overview",
            "Data Explorer",
            "Student Risk Demo"
        ]
    )

    st.sidebar.divider()

    st.sidebar.caption(
        "EduTrack | Academic Analytics System"
    )

    if st.sidebar.button("Logout", use_container_width=True):

        st.session_state["authenticated"] = False
        st.session_state.pop("user", None)

        st.rerun()

    # Display selected page
    if page == "Overview":
        show_overview(df)

    elif page == "Data Explorer":
        show_data_explorer(df)

    elif page == "Student Risk Demo":
        show_prediction_demo(df)
