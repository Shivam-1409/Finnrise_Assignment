# Finnrise_Assignment:

Created an automated web app that takes pdf and generate atleast 10 logical questions with scoring parameters, making it user friendly along with a logical game generated automatically based on the content in the pdf.

**ARCHITECTURE**:
**content_ingestion.py**-- Using PDFPLUMBER extracting text from pdf
**text_chunking.py**--     Extracted text are then chunked using Recurssive chunking with chunk_size=1500 and allowed overalapping of 300****
**llm_helper.py** --       Used Groq API keys to prevent cubersome issues faced by local download of model and "openai/gpt-oss-120b" model.
**prompt_generator.py** -- Created three prompts (**PROMPT STRATEGY**)
                           First prompt i.e. **"build_document_understanding_two"** extracting logical flows such as Implicit Constraints, Causal Chains, Contradictory Scenarios, Inference Seeds, Preserve 
                           Complexity,expansion over Compression from the provided document and instead of providing entire text all at once, we have provided it in chunks and each chunks gets added to previous chunks and 
                           then llm builds logic flows with addition pf each chunk  to prevent optimize tokens and to generate flows from each para of the pdf and iteratively creating a **knowledge base**.
                           Second prompt i.e. **"generate_logical_questions"** use existing knowledge base to create atleast 10 different logical question instead of recall questions which should be a mix of fill in the
                           blanks, short answer and mcqs
                           Third prompt i.e. **choose_best_game** again use existing knowledge base to decide which game is most suitable to play based on the given content
                           FOR EACH PROMPT CLIENT SERVICE IS USED INSTEAD OF INVOKE SO THAT THE PROMPT THAT CAN DIRECTLY BE ANSWERED THROUGH GROQ API INSTEAD OF USING LANGCHAIN WRAPPER.
**ui.py** --               Used Streamlit to create web app interface which interacts with groq apis on real time to fetch answers of each prompt whenever a user hit **"Generate Questions"** button with slide questions
                           to prevent all question bombarding at once.
                           3 differents UIs are designed for 3 different types of questions (MCQ, Fill in the blanks, Short Answers) which change on real time
                           4 different UIs are designed for 4 different logical games which also changes as per the choice of LLM to which games suited for given content.
                           NOTE: SCORING AND ROUNDS OF GAMES ARE NOT ADDED DUE TO LIMITED TOKENS IF HEAVY DOCUMENT IS PASSED IT WILL EXHAUST ALL THE TOKENS AS LLM NEED TO DESIGN THE 4 GAME FIRST AND IF EACH WOULD HAVE
                           DIFFERENT ROUND THEN ALONG WITH CREATING ATLEAST 10 LOGICAL QUESTIONS IT NEEDS TO DESIGN SCENARIOS, CASE STUDIES CONTINOUSLY TILL WHENEVER THE USER WANTS TO PLAY. SO IT IS NOT IMPLEMENTED YET, BUT 
                           IT CAN BE IMPLEMENTED.
