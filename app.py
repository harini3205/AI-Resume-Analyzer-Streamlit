import streamlit as st
import PyPDF2
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------------- CSS ---------------- #
st.markdown("""
<style>

/* Remove sidebar + deploy */
[data-testid="stSidebar"] {display:none;}
header img {display:none;}
button[data-testid="baseButton-header"] {display:none;}

/* Black background */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
}

/* White text */
* { color: #ffffff !important; }

/* Inputs */
textarea, input {
    background-color: black !important;
    color: white !important;
    border: 1px solid white !important;
}

/* Buttons */
.stButton > button {
    background-color: black !important;
    color: white !important;
    border: 1px solid white !important;
}

/* Upload */
[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: 1px dashed white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ---------------- #
if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- FUNCTIONS ---------------- #
def get_match_score(resume, jd):
    cv = CountVectorizer().fit_transform([resume, jd])
    return round(cosine_similarity(cv)[0][1]*100,2)

def calculate_ats_score(text):
    score = 0
    if len(text) > 800: score += 40
    if re.search(r'[\w\.-]+@[\w\.-]+', text): score += 20
    for s in ['experience','education','skills']:
        if s in text.lower(): score += 10
    return min(score,100)

# ---------------- LOGIN PAGE ---------------- #
if st.session_state.page == "login":

    st.markdown("<h2 style='text-align:center;'>Login</h2>", unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.success("Login Successful ✅")
        st.session_state.page = "home"
        st.rerun()

# ---------------- HOME PAGE ---------------- #
else:

    # Header
    col1, col2 = st.columns([8,2])
    with col2:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()

    st.markdown("<h1 style='text-align:center;'>AI Resume Analyzer</h1>", unsafe_allow_html=True)

    # Upload (small)
    st.markdown("### Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

    # Inputs
    col1, col2 = st.columns(2)

    with col1:
        jd = st.text_area("Job Description", height=200)

    with col2:
        skills = st.text_area("Required Skills", height=200)

    # Analyze Button
    analyze = st.button("Analyze & Evaluate", width="stretch")

    # Results
    if analyze and uploaded_file and jd:
        reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = " ".join([p.extract_text() for p in reader.pages])

        match = get_match_score(resume_text.lower(), jd.lower())
        ats = calculate_ats_score(resume_text)

        st.write(f"### Match Score: {match}%")
        st.write(f"### ATS Score: {ats}%")

    # ---------------- FIXED EVALUATION SECTION ---------------- #
    st.markdown("## Evaluation Metrics")

    titles = [
        "Keywords","Skills","Experience","Education","Certifications",
        "Formatting","Projects","Soft Skills","Achievements","ATS Fit"
    ]

    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            st.markdown(f"<div style='border:1px solid white; padding:15px; text-align:center;'>{titles[i]}</div>", unsafe_allow_html=True)