
# EduTrack - Student Dropout Risk & Academic Success Prediction System

## Project Overview

EduTrack is an interactive student analytics dashboard developed using Python and Streamlit.

The project aims to demonstrate how student demographic, socioeconomic, and academic information can be explored to understand educational outcomes and identify potential student dropout risks.

The proposed system focuses on three academic outcomes:

- Dropout
- Enrolled
- Graduate

## Problem Statement

Educational institutions may face challenges identifying students who are at risk of dropping out. EduTrack proposes an interactive analytics platform that explores student records and demonstrates how academic information can support student outcome analysis.

## Dataset

**Dataset Name:** Predict Students' Dropout and Academic Success

**Source:** UCI Machine Learning Repository

**Dataset URL:** https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success

Dataset details:
- 4,424 student records
- 36 input features
- 1 target column
- CSV format
- Three academic outcome categories

Place the downloaded dataset at:

`data/student_data.csv`

The dataset is provided under the CC BY 4.0 license. Refer to the UCI repository for attribution.

## Main Features

### 1. User Authentication
- Separate login and signup forms.
- Full name and email validation.
- Password confirmation.
- Duplicate email prevention.
- Password hashing using PBKDF2-HMAC-SHA256.
- SQLite database integration.

### 2. Dashboard Overview
- Total student statistics.
- Graduate, dropout, and enrolled counts.
- Academic outcome visualization.
- Student age distribution chart.

### 3. Student Data Explorer
- Filter records by academic outcomes.
- Filter students by age range.
- Interactive student records table.
- Outcome-based visualizations.

### 4. Student Risk Prediction Demo
- Student age input.
- First semester approved units.
- Second semester approved units.
- Tuition fee status.
- Simulated outcome predictions.
- Illustrative risk score.

**Important:** The current Lab 9 version uses predefined demonstration rules for simulated predictions. It does not contain a trained machine learning model. Model training and evaluation are planned for the future project.

## Project Structure

```text
EduTrack/
│
├── app.py
├── auth.py
├── database.py
├── dashboard.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── student_data.csv
```

The SQLite database file `edutrack.db` is created automatically when the application starts.

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- SQLite
- Git and GitHub

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/whoisalibtw/EduTrack.git
cd EduTrack
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in the browser at:

`http://localhost:8501`

## Database and Security

EduTrack uses SQLite to store registered user accounts.

Passwords are never stored in plaintext. Passwords are hashed using PBKDF2-HMAC-SHA256 with unique random salts.

The local database, virtual environment, and sensitive configuration files are excluded from GitHub using `.gitignore`.

## Future Scope

The proposed final project will include:

- Data preprocessing.
- Exploratory Data Analysis (EDA).
- Machine learning model training.
- Model evaluation.
- Improved student outcome prediction.
- Additional academic performance insights.

## Current Project Scope

This version was developed for Programming for AI — Lab Task 9.

The current implementation focuses on:
- Project topic and dataset selection.
- Streamlit dashboard development.
- Database-integrated user authentication.
- Interactive dashboard functionality.
- Simulated prediction demonstration.

Machine learning model training is not included in this laboratory task.

## Course Information

**Course:** Programming for AI  
**University:** Federal Urdu University of Arts, Science and Technology  
**Instructor:** Ms. Izza Yaqoob  
**Assignment:** Lab Task 9

