import streamlit as st
import json
from pypdf import PdfReader
from kss import summarize_sentences


def load_subject_info():
    with open('data/subject_info.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text


def summarize_text(text, max_chars=200):
    if not text:
        return ""
    try:
        sents = summarize_sentences(text, max_sentences=3)
        summary = " ".join(sents)
    except Exception:
        summary = text
    summary = summary.strip()
    if len(summary) > max_chars:
        summary = summary[:max_chars]
    return summary


def main():
    st.title("생활기록부 프롬프트 생성기")

    student_id = st.text_input("학생 번호")
    student_name = st.text_input("학생 이름")

    subjects = load_subject_info()
    subject = st.selectbox("교과 선택", list(subjects.keys()))

    uploaded_file = st.file_uploader("학생활동자료 PDF 업로드", type=["pdf"])

    summary = ""
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        summary = summarize_text(text)
        summary = st.text_area("요약 (200자 내외)", value=summary, max_chars=200, height=150)

    remarks = st.text_area("관찰 특기 사항", height=150)

    if st.button("프롬프트 생성"):
        if not uploaded_file:
            st.warning("PDF 파일을 업로드하세요.")
            return
        prompt = f"""학생 번호: {student_id}
이름: {student_name}
교과: {subject}
교과 역량: {subjects[subject]['skills']}
2022 개정 교육과정: {subjects[subject]['curriculum_2022']}
생활기록부 기록 예시: {subjects[subject]['record_examples']}
학생 활동 요약: {summary}
관찰 특기 사항: {remarks}

위 정보를 활용하여 생활기록부 기록 문장을 작성하시오."""
        st.text_area("최종 프롬프트", value=prompt, height=300)


if __name__ == "__main__":
    main()
