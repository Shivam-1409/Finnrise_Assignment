# About:

Created an automated web app that takes pdf and generate atleast 10 logical questions with scoring parameters, making it user friendly along with a logical game generated automatically based on the content in the pdf.

## ARCHITECTURE:

**content_ingestion.py**  
Using PDFPLUMBER extracting text from pdf.  

**text_chunking.py**  
Extracted text are then chunked using Recursive chunking with chunk_size = 1500 and allowed overlapping of 300.  

**llm_helper.py**  
Used Groq API keys to prevent cumbersome issues faced by local download of model and "openai/gpt-oss-120b" model.  

**prompt_generator.py**  
Created three prompts (**PROMPT STRATEGY**)

First prompt i.e. **build_document_understanding_two**  
Extracting logical flows such as:
- Implicit Constraints  
- Causal Chains  
- Contradictory Scenarios  
- Inference Seeds  
- Preserve Complexity  
- Expansion over Compression  

Instead of providing the entire text all at once, the document is given in chunks.  
Each chunk is added to the previous chunk and the LLM builds logic flows iteratively to create a **knowledge base**.

Second prompt i.e. **generate_logical_questions**  
Uses the existing knowledge base to create atleast 10 different logical questions instead of recall questions.  
These include:
- Fill in the blanks  
- Short answers  
- MCQs  

Third prompt i.e. **choose_best_game**  
Uses the existing knowledge base to decide which game is most suitable based on the document.

For each prompt, **client service is used instead of invoke**, so that prompts can directly interact with the Groq API instead of using a LangChain wrapper.

**ui.py**  
Used Streamlit to create a web app interface which interacts with Groq APIs in real time to fetch questions and answers when the user clicks the **"Generate Questions"** button with caching
implemented to avoid reprompting, chunking or extracting text from same doc again and again.
A sliding mechanism is used to avoid overwhelming the user.

3 different UIs are designed for:
- MCQs  
- Fill in the blanks  
- Short answers  

These change dynamically.

4 different UIs are designed for 4 logical games, selected dynamically based on LLM output.

---

### NOTE:
Scoring and multiple game rounds are not implemented due to token limitations.  
For large documents, the LLM must design:
- Game structure  
- Scenarios  
- Case studies  
- Question sets  

This consumes excessive tokens. However, this feature can be implemented in future.
