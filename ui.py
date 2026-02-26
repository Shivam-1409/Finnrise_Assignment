import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import os
load_dotenv()
from content_ingestion import extract_text_from_pdf
from text_chunking import text_splitters
from prompt_generator import build_document_understanding_two
from prompt_generator import generate_logical_questions
from prompt_generator import choose_best_game

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = "openai/gpt-oss-120b"

st.title("Finnrise Assignment")

if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = None

if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.generated = False

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

tab1, tab2 = st.tabs(["Generate Questions", "Play Game"])

@st.cache_data(show_spinner=True)
def extract_and_chunk(uploaded_file):

    text = extract_text_from_pdf(uploaded_file)
    chunks = text_splitters(str(text).strip())

    return chunks

@st.cache_data(show_spinner=True)
def generate_pipeline(chunks):

    knowledge_base = build_document_understanding_two(
        chunks, client, model
    )

    questions = generate_logical_questions(
        knowledge_base, client, model
    )

    game_config = choose_best_game(
        knowledge_base, client, model
    )

    return knowledge_base, questions, game_config

def handle_next():
    if st.session_state.current_q < len(st.session_state.questions) - 1:
        st.session_state.current_q += 1
        st.session_state.answered = False
    else:
        st.session_state.quiz_completed = True

if "answered" not in st.session_state:
    st.session_state.answered = False

if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False

with tab1:
    if uploaded_file is not None:

       if st.button("Generate Questions"):

          chunks = extract_and_chunk(uploaded_file)

          knowledge_base, questions, game_config = generate_pipeline(chunks)

          st.session_state.knowledge_base = knowledge_base
          st.session_state.questions = questions
          st.session_state.game_config = game_config

          st.session_state.current_q = 0
          st.session_state.score = 0
          st.session_state.generated = True

    if st.session_state.generated and st.session_state.questions:

        q = st.session_state.questions[st.session_state.current_q]
        st.write(f"Score {st.session_state.score}")
        st.write(f"Question {st.session_state.current_q + 1}")

        # MCQ
        if q["type"] == "mcq":
            user_answer = st.radio(q["question"], q["options"])
            if st.button("Check Answer"):
                if user_answer == q["answer"]:
                    st.success("Correct!")
                    st.session_state.score += 1
                else:
                    st.error(f"Wrong. Correct answer: {q['answer']}")
                
                st.session_state.answered = True

        # Fill
        elif q["type"] == "fill":
            user_input = st.text_input(q["question"])

            if st.button("Check Answer"):
                if user_input.strip().lower() == q["answer"].lower():
                    st.success("Correct!")
                    st.session_state.score += 1
                else:
                    st.error(f"Wrong. Correct answer: {q['answer']}")
                
                st.session_state.answered = True

        # Short
        elif q["type"] == "short":
            user_input = st.text_area(q["question"])

            if st.button("Check Answer"):
                st.write("Expected answer:", q["answer"])
            
            st.session_state.answered = True


    if st.session_state.get("answered", False) and not st.session_state.quiz_completed:
       st.button("Next", on_click=handle_next, key="next_btn")

    if st.session_state.quiz_completed:
       st.success("All questions completed!")
       st.write(f"Final Score: {st.session_state.score} / {len(st.session_state.questions)}")

    # if st.button("Reset Game"):
    #     st.session_state.generated = False
    #     st.session_state.questions = []
    #     st.session_state.knowledge_base = None

with tab2:

    if "game_started" not in st.session_state:
        st.session_state.game_started = False

    # Play button
    if st.button("Play Game"):
        st.session_state.game_started = True

    # Run game only after click
    if st.session_state.game_started:
        game = st.session_state.game_config
        game_type = game["type"]

        st.subheader(f"Game Type: {game_type}")

        if game_type == "Scenario Decision Game":

            st.write(game["scenario"])

            choice = st.radio("Choose the best option:", game["options"])

            if st.button("Submit"):
                if choice == game["answer"]:
                    st.success("Correct!")
                else:
                    st.error(f"Wrong! Correct: {game['answer']}")

        elif game_type == "Cause-Effect Mapping":

            st.write(game["statements"])

            choice = st.radio("Select relationship:", game["options"])

            if st.button("Submit"):
                if choice == game["answer"]:
                    st.success("Correct!")
                else:
                    st.error(f"Wrong! Correct: {game['answer']}")
        
        elif game_type == "Identify the Misconception":

            st.write(game["statement"])

            choice = st.radio("True or False:", game["options"])

            if st.button("Submit"):
                if choice == game["answer"]:
                    st.success("Correct!")
                else:
                    st.error(f"Wrong! Correct: {game['answer']}")
        
        elif game_type == "Fix the Logic":

            st.write(game["statement"])

            user_input = st.text_area("Fix the logic:")

            if st.button("Submit"):
                st.write("Expected answer:")
                st.success(game["answer"])