import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# User credentials 
USERS = {
    "ashish@123": "ashish123",
    "admin@gmail.com": "admin@123",
    "rahul@321": "rahul321#",
    "bob123@gmail.com": "bob123#"
}

def login_page():
    st.title("🔐 Login to StudyTrack AI")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# If not logged in → show login page ONLY
if not st.session_state.logged_in:
    login_page()
    st.stop()

# STOP DASHBOARD IF NOT LOGGED IN
if not st.session_state.logged_in:
    login_page()
    st.stop()

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="StudyTrack AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# GLOBAL CSS (UNCHANGED)
# ------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-left: 4rem;
    padding-right: 1.5rem;
}
.main-title {
    margin-top: 10px;
    padding-left: 11rem;
    font-size: 44px;
    font-weight: 700;
    color: white;
    margin-bottom: 4px;
}
.sub-title {
    font-size: 18px;
    padding-left: 10rem;
    color: #c7cbd1;
    margin-top: 0px;
    margin-bottom: 16px;
}
.section-title {
    font-size: 30px;
    font-weight: 600;
    margin-top: 8px;
    margin-bottom: 8px;
}
hr {
    margin-top: 10px;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR NAVIGATION (UNCHANGED)
# ------------------------------------------------
st.sidebar.title("📘 Navigation")
menu = st.sidebar.radio(
    "",
    ["🏠 Home", "🧠 Model Training", "📊 Data Insights", "🎓 Student", "📈 Recommendation", "📄 Documentation"]
)

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ------------------------------------------------
# HOME PAGE (UNCHANGED)
# ------------------------------------------------
if menu == "🏠 Home":

    col1, col2 = st.columns([0.7, 9.3])

    with col2:
        st.markdown("<div class='main-title'> 🚀StudyTrack AI </div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='sub-title'>Tracking, Predicting, and Improving Student Performance</div>",
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("<div class='section-title'>Project Overview</div>", unsafe_allow_html=True)

    st.write("""
    **StudyTrack AI – Personal Dashboard** analyzes student academic data using multiple
    behavioral and lifestyle parameters to generate insights, predictions, and
    personalized recommendations.
    The system supports CSV uploads, interactive dashboards, and AI-based performance prediction to help students
     make data-driven decisions.
    """)

    st.image(
        "images.png",
        use_container_width=True
    )

    st.markdown("<div class='section-title'>Project Objectives</div>", unsafe_allow_html=True)

    st.markdown("""
    - Analyze student performance using multiple parameters  
    - Predict academic outcomes  
    - Provide personalized recommendations  
    - Visualize academic trends  
    - Enable data-driven decision making  
    """)

# ------------------------------------------------
# MODEL TRAINING (ONLY TEXT CLARIFIED)
# ------------------------------------------------
elif menu == "🧠 Model Training":
    st.title("🧠 Model Training")

    file = st.file_uploader("Upload Student Dataset (CSV)", type=["csv"])

    if file:
        df = pd.read_csv(file)

        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

        if st.button("Train Model"):

            # ---------- FEATURE SELECTION ----------
            required_cols = [
                "Study_Hours",
                "Sleep_Hours",
                "Attendance_Percentage",
                "Attention_Level",
                "Previous_Marks"
            ]

            if not all(col in df.columns for col in required_cols):
                st.error("❌ Dataset missing required columns!")
                st.stop()

            # ---------- MULTI-PARAMETER PREDICTION ----------
            df["Predicted_Marks"] = (
                0.35 * df["Study_Hours"] * 10 +
                0.20 * df["Sleep_Hours"] * 10 +
                0.20 * df["Attendance_Percentage"] / 10 +
                0.15 * df["Attention_Level"] +
                0.10 * df["Previous_Marks"]
            )

            # ---------- PERFORMANCE LEVEL ----------
            def performance_level(marks):
                if marks >= 85:
                    return "Excellent Performer"
                elif marks >= 70:
                    return "Good Performer"
                elif marks >= 55:
                    return  "Average Performer"  
                else:
                    return "Needs Improvement"

            df["Performance_Level"] = df["Predicted_Marks"].apply(performance_level)

            # ---------- DATA-DRIVEN RECOMMENDATION ----------
            def generate_recommendation(row):
               rec = []

               # First decide based on performance level
               if row["Performance_Level"] == "Excellent Performer":
                   rec.append("Maintain current study routine")
                   if row["Attention_Level"] < 70:
                       rec.append("Improve focus consistency")
                   if row["Sleep_Hours"] < 7:
                       rec.append("Ensure adequate sleep")

               elif row["Performance_Level"] == "Average Performer":
                    rec.append("Increase academic consistency")
                    if row["Study_Hours"] < 6:
                       rec.append("Increase study hours")
                    if row["Attention_Level"] < 65:
                       rec.append("Reduce distractions and improve focus")
                    if row["Attendance_Percentage"] < 80:
                       rec.append("Improve class attendance")
               else:  # Needs Improvement
                    rec.append("Immediate academic intervention required")
                    if row["Study_Hours"] < 6:
                       rec.append("Significantly increase study hours")
                    if row["Sleep_Hours"] < 7:
                       rec.append("Improve sleep routine")
                    if row["Attention_Level"] < 60:
                       rec.append("Work on concentration techniques")
                    if row["Attendance_Percentage"] < 75:
                       rec.append("Attend classes regularly")
               return " | ".join(rec)
                

            df["Recommendation"] = df.apply(generate_recommendation, axis=1)

            # ---------- STORE TRAINED DATA ----------
            st.session_state["trained_data"] = df

            st.success("✅ Model trained successfully using multiple parameters!")
            

#Data Insights----------------------
# ------------------------------------------------
# DATA INSIGHTS
# ------------------------------------------------
elif menu == "📊 Data Insights":
    st.title("📊 Data Insights Dashboard")

    # CHECK IF MODEL IS TRAINED
    if "trained_data" not in st.session_state:
        st.warning("⚠️ Please upload data and train the model first.")
    else:
        df = st.session_state["trained_data"]

        st.success("✅ Data loaded successfully for insights!")

        # -----------------------------
        # DATA PREVIEW
        # -----------------------------
        st.subheader("📄 Trained Data")
        st.dataframe(df)
        st.subheader("⬇️ Download Trained Model Data")

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
           label="📥 Download Trained Dataset (CSV)",
           data=csv_data,
           file_name="studytrack_trained_data.csv",
           mime="text/csv"
        )

        # -----------------------------
        # 1️⃣ Study Hours vs Predicted Marks (FIXED)
        # -----------------------------
        st.subheader("🎯 Study Hours vs Predicted Marks")

        fig1 = px.scatter(
            df,
            x="Study_Hours",
            y="Predicted_Marks",
            color="Performance_Level",
            size="Attendance_Percentage"
        )
        st.plotly_chart(fig1, use_container_width=True)

        # -----------------------------
        # 2️⃣ Average Predicted Marks by Study Hours
        # -----------------------------
        st.subheader("📊 Average Predicted Marks by Study Hours")

        avg_df = df.groupby("Study_Hours", as_index=False)["Predicted_Marks"].mean()

        fig2 = px.bar(
            avg_df,
            x="Study_Hours",
            y="Predicted_Marks",
            color="Predicted_Marks"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # -----------------------------
        # 3️⃣ Performance Level Distribution (PIE CHART)
        # -----------------------------
        st.subheader("🥧 Performance Level Distribution")

        perf_df = df["Performance_Level"].value_counts().reset_index()
        perf_df.columns = ["Performance_Level", "Count"]

        fig3 = px.pie(
            perf_df,
            names="Performance_Level",
            values="Count",
            title="Distribution of Student Performance Levels"
        )
        st.plotly_chart(fig3, use_container_width=True)

        # -----------------------------
        # 4️⃣ Correlation Heatmap
        # -----------------------------
        st.subheader("🔥 Correlation Heatmap")

        numeric_df = df.select_dtypes(include="number")
        corr = numeric_df.corr()

        fig4 = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu"
        )
        st.plotly_chart(fig4, use_container_width=True)

        # -----------------------------
        # 5️⃣ Actual vs Predicted Marks
        # -----------------------------
        st.subheader("📈 Actual vs Predicted Marks")

        # Check required columns
        required_cols = ["Final_Marks", "Predicted_Marks"]
        missing = [c for c in required_cols if c not in df.columns]

        if missing:
           st.warning("⚠️ Actual marks not available to compare.")
        else:
           compare_df = df[["Final_Marks", "Predicted_Marks"]].copy()
           compare_df.columns = ["Actual Marks", "Predicted Marks"]

        # Show table
           st.dataframe(compare_df, use_container_width=True)

        # Line chart
           fig5 = px.line(
               compare_df,
               y=["Actual Marks", "Predicted Marks"],
               markers=True,
               title="Actual vs Predicted Marks Comparison"
            )
        st.plotly_chart(fig5, use_container_width=True)

        st.divider()
        st.subheader("💡 Key Insights Summary")

        avg_study = df["Study_Hours"].mean()
        avg_marks = df["Predicted_Marks"].mean()
        avg_attention = df["Attention_Level"].mean()

        topper = df.loc[df["Predicted_Marks"].idxmax(), "Student_Name"]

        st.markdown(f"""
        - 📘 **Average Study Hours:** {avg_study:.2f} hrs/day  
        - 🎯 **Average Predicted Marks:** {avg_marks:.2f}%  
        - 🏆 **Top Performing Student:** {topper}  
        - 🧠 **Average Attention Level:** {avg_attention:.2f}  
        """)




# ------------------------------------------------
# STUDENT PAGE (MULTI-PARAMETERS ADDED HERE)
# ------------------------------------------------
elif menu == "🎓 Student":
    st.title("🎓 Student Analysis")

    # =====================================================
    # 🔹 PART 1: INDIVIDUAL STUDENT PREDICTION (NO RECOMMENDATION)
    # =====================================================
    st.subheader("🧍 Individual Student Prediction")

    name = st.text_input("Student Name", key="student_name_input")

    col1, col2, col3 = st.columns(3)

    with col1:
        study_hours = st.slider("📘 Study Hours", 0, 12, 5)
        play_hours = st.slider("🎮 Play Hours", 0, 6, 2)

    with col2:
        sleep_hours = st.slider("😴 Sleep Hours", 0, 10, 7)
        social_media = st.slider("📱 Social Media Hours", 0, 6, 2)

    with col3:
        exercise = st.slider("🏃 Exercise (hrs/week)", 0, 7, 3)
        attention = st.slider("🧠 Attention Level", 0, 10, 7)

    if st.button("Analyze Individual Student"):
        # -------- Prediction Logic --------
        predicted_marks = (
            0.35 * study_hours * 10 +
            0.20 * sleep_hours * 10 +
            0.20 * (100 - social_media * 10) / 10 +
            0.15 * attention * 10 +
            0.10 * exercise * 10
        )

        # -------- Performance Level --------
        if predicted_marks >= 85:
            performance = "Excellent Performer"
        elif predicted_marks >= 70:
            performance = "Good Performer"
        elif predicted_marks >= 55:
            performance = "Average Performer"
        else:
            performance = "Needs Improvement"

        # -------- OUTPUT (NO RECOMMENDATION HERE) --------
        st.success(f"Analysis completed for {name}")
        st.markdown("### 📊 Prediction Result")
        st.write(f"**Predicted Marks:** {predicted_marks:.2f}")
        st.write(f"**Performance Level:** {performance}")

        st.markdown("### 📥 Parameters Used")
        st.write(f"""
        - Study Hours: {study_hours}  
        - Play Hours: {play_hours}  
        - Sleep Hours: {sleep_hours}  
        - Social Media Usage: {social_media}  
        - Exercise: {exercise}  
        - Attention Level: {attention}  
        """)

# =====================================================
# 🔹 PART 2: BULK STUDENT PREDICTION (UPDATED)
# =====================================================
    st.divider()
    st.subheader("📂 Bulk Student Prediction (CSV Upload)")

    bulk_file = st.file_uploader(
        "Upload Student CSV for Bulk Prediction",
        type=["csv"]
    )

    if bulk_file:
        bulk_df = pd.read_csv(bulk_file)

        st.subheader("📄 Uploaded Data Preview")
        st.dataframe(bulk_df.head())

        if st.button("Predict Bulk Data"):

            # ---------- REQUIRED COLUMNS ----------
            required_cols = [
                "Student_ID",
                "Student_Name",
                "Study_Hours",
                "Sleep_Hours",
                "Play_Hours",
                "Exercise",
                "Attendance_Percentage",            
                "Attention_Level"
            ]

            if not all(col in bulk_df.columns for col in required_cols):
                st.error("❌ CSV missing required columns!")
                st.stop()

            # ---------- PREDICT MARKS (NO PREVIOUS MARKS) ----------
            bulk_df["Predicted_Marks"] = (
                0.25 * bulk_df["Study_Hours"] *5  +
                0.15 * bulk_df["Sleep_Hours"] *4 +
                0.10 * (6 - bulk_df["Play_Hours"]).clip(0) * 3  +
                0.10 * bulk_df["Exercise"] * 3  +
                0.25 * bulk_df["Attendance_Percentage"] * 0.3 +
                0.15 * bulk_df["Attention_Level"]* 4               
            )
            bulk_df["Predicted_Marks"] = bulk_df["Predicted_Marks"].clip(0, 100).round(2)

            # ---------- PERFORMANCE LEVEL ----------
            def perf_level(marks):
                if marks >= 85:
                    return "Excellent Performer"
                elif marks >= 70:
                    return "Good Performer"
                elif marks >= 55:
                    return "Average Performer"
                else:
                    return "Needs Improvement"

            bulk_df["Performance_Level"] = bulk_df["Predicted_Marks"].apply(perf_level)

            st.success("✅ Bulk prediction completed successfully")

            # ---------- SHOW FULL RESULT ----------
            st.subheader("📊 Bulk Prediction Results")
            st.dataframe(bulk_df, use_container_width=True)

            # ---------- DOWNLOAD CSV ----------
            csv = bulk_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Bulk Prediction Result",
                csv,
                "bulk_student_predictions.csv",
                "text/csv"
            )
 



# ------------------------------------------------
# RECOMMENDATION PAGE (LOGIC BASED ON PARAMETERS)

# RECOMMENDATION PAGE (COMBINED)
# ------------------------------------------------
elif menu == "📈 Recommendation":
    st.title("📈 AI-Based Student Recommendations")

    # =====================================================
    # 🔹 PART 1: SINGLE STUDENT RECOMMENDATION
    # =====================================================
    st.subheader("🧍 Single Student Recommendation")

    student_name = st.text_input("Student Name", key="recommendation_student_name")

    col1, col2, col3 = st.columns(3)

    with col1:
        study_hours = st.slider("📘 Study Hours", 0, 12, 5)
        play_hours = st.slider("🎮 Play Hours", 0, 6, 2)

    with col2:
        sleep_hours = st.slider("😴 Sleep Hours", 0, 10, 7)
        social_media = st.slider("📱 Social Media Hours", 0, 6, 2)

    with col3:
        exercise = st.slider("🏃 Exercise (hrs/week)", 0, 7, 3)
        attention = st.slider("🧠 Attention Level", 0, 10, 7)

    if st.button("Generate Recommendation"):

        # ---------- Prediction Logic ----------
        predicted_marks = (
            0.30 * study_hours * 10 +
            0.20 * sleep_hours * 10 +
            0.15 * attention * 10 +
            0.15 * exercise * 10 +
            0.10 * (6 - play_hours) * 10 +
            0.10 * (6 - social_media) * 10
        )

        # ---------- Recommendation Logic ----------
        rec = []

        if predicted_marks >= 85:
            rec.append("Maintain current study routine")
            if attention < 7:
                rec.append("Improve focus consistency")
            if sleep_hours < 7:
                rec.append("Ensure adequate sleep")
            if social_media > 3:
                rec.append("Limit social media usage")

        elif predicted_marks >= 55:
            rec.append("Increase academic consistency")
            if study_hours < 6:
                rec.append("Increase study hours")
            if attention < 6:
                rec.append("Reduce distractions and improve focus")
            if play_hours > 3:
                rec.append("Balance play time with study")
            if sleep_hours < 7:
                rec.append("Improve sleep routine")

        else:
            rec.append("Immediate academic improvement required")
            if study_hours < 6:
                rec.append("Significantly increase study hours")
            if sleep_hours < 7:
                rec.append("Improve sleep routine")
            if attention < 6:
                rec.append("Work on concentration techniques")
            if social_media > 3:
                rec.append("Reduce social media usage")
            if play_hours > 3:
                rec.append("Reduce play hours and focus on academics")

        # ---------- OUTPUT ----------
        st.success(f"Recommendation generated for {student_name}")
        st.write(f"**Predicted Marks:** {predicted_marks:.2f}")
        st.info(" | ".join(rec))

    # =====================================================
    # 🔹 PART 2: TRAINED MODEL RECOMMENDATIONS (NO PERFORMANCE)
    # =====================================================
    st.divider()
    st.subheader("📄 Trained Model – Student Recommendations")

    if "trained_data" not in st.session_state:
        st.warning("⚠️ Please upload data and train the model first.")
    else:
        df = st.session_state["trained_data"]

        show_cols = [
            "Student_Name",
            "Predicted_Marks",
            "Recommendation"
        ]

        for col in show_cols:
            if col not in df.columns:
                st.error(f"❌ Missing column: {col}")
                st.stop()

        st.dataframe(df[show_cols], use_container_width=True)

# ------------------------------------------------
# DOCUMENTATION PAGE (FULL WORKFLOW)
# ------------------------------------------------
elif menu == "📄 Documentation":
    st.title("📄 Model Workflow Documentation")

    st.markdown("### StudyTrack AI – Workflow")

    # OPTION 1: Local image (recommended)
    st.image(
        "image2.png",   # put image in same folder as app.py
        width=600
    )


st.markdown(
    """
    <hr>
    <div style="text-align:center; color:gray; font-size:14px;">
       © 2025 StudyTrack AI | Designed by Ashish Kumar | Trained by Anil Kumar

    </div>
    """,
    unsafe_allow_html=True
)
