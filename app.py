import streamlit as st
import matplotlib.pyplot as plt

from utils.pdf_reader import extract_text
from utils.preprocess import clean_text
from utils.ranking import rank_resumes
from utils.ml_model import train_model

st.title("AI Resume Screening System")

job_description = st.text_area(
    "Enter Job Description"
)

uploaded_files = st.file_uploader(
    "Upload Resumes",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files and job_description:

    model = train_model()

    resumes = []

    names = []

    for file in uploaded_files:

        text = extract_text(file)

        cleaned = clean_text(text)

        resumes.append(cleaned)

        names.append(file.name)

    cleaned_job = clean_text(job_description)

    scores = rank_resumes(
        cleaned_job,
        resumes
    )

    results = list(zip(names, scores))

    sorted_results = sorted(
        results,
        key=lambda x: x[1],
        reverse=True
    )

    st.subheader("Candidate Rankings")

    skills = {
        "python": [
            "django",
            "flask",
            "pandas"
        ],

        "machine learning": [
            "deep learning",
            "tensorflow",
            "pytorch",
            "ai"
        ],

        "sql": [
            "mysql",
            "postgresql",
            "database"
        ],

        "nlp": [
            "text processing",
            "chatbot",
            "language model"
        ],

        "data analysis": [
            "power bi",
            "statistics",
            "visualization"
        ],

        "react": [
            "frontend",
            "javascript"
        ]
    }

    for name, score in sorted_results:

        st.write(
            f"{name} → Match Score: {score:.2f}"
        )

        resume_index = names.index(name)

        resume_text = resumes[resume_index]

        detected_skills = []

        transferable_skills = []

        for main_skill, related_skills in skills.items():

            if main_skill in resume_text:

                detected_skills.append(main_skill)

            else:

                for related_skill in related_skills:

                    if related_skill in resume_text:

                        transferable_skills.append(
                            f"{related_skill} → {main_skill}"
                        )

        st.write(
            "Exact Skills:",
            ", ".join(detected_skills)
        )

        st.write(
            "Transferable Skills:",
            ", ".join(transferable_skills)
        )

        prediction = model.predict([resume_text])[0]

        if prediction == 1:

            st.success("Suitable Candidate")

        else:

            st.error("Not Suitable Candidate")

        st.write("---")

    candidate_names = [x[0] for x in sorted_results]

    candidate_scores = [x[1] for x in sorted_results]

    fig, ax = plt.subplots()

    ax.bar(candidate_names, candidate_scores)

    ax.set_xlabel("Candidates")

    ax.set_ylabel("Match Score")

    ax.set_title("Resume Ranking Scores")

    st.pyplot(fig)