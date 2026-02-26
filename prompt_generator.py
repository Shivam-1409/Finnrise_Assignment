from dotenv import load_dotenv
from groq import Groq
import os
import json
load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

knowledge_base = ""

# Prompt to generate knowledge base of logical understanding from the document
def build_document_understanding_two(chunks, client, model):
    knowledge_base = ""

    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks):

        prompt = f"""
    You are an expert in logical reasoning and structured analysis.
    We are analysing a document step by step.

    This is chunk {i+1} out of {total_chunks}.

    Previously extracted structured knowledge:
    {knowledge_base}

    New document chunk:
    {chunk}

    Your Task:

    Synthesize Knowledge: Integrate the "New document chunk" into the "Previously extracted knowledge" without losing granular detail.

    Map the Logic (Do NOT Summarize):

    Implicit Constraints: Identify rules or limits implied by the text but not explicitly stated.

    Causal Chains: Document every "If [A], then [B]" relationship found or inferred.

    Contradictory Scenarios: Identify conditions where two goals or rules might conflict.

    Inference Seeds: Extract specific facts that, when combined, lead to a new conclusion.

    Preserve Complexity: Maintain specific names, values, and technical dependencies.

    Expansion over Compression: If new information adds depth to a previous point, expand that point rather than replacing it.

    Return ONLY the updated comprehensive logical map.
    """

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a reasoning engine."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        knowledge_base = response.choices[0].message.content

    return knowledge_base




# Prompt to generate logical_questions from knowledge base created from above prompt
def generate_logical_questions(knowledge_base, client, model):

    prompt = f"""
You are an expert logical reasoning question designer.

Based on the following structured knowledge:
{knowledge_base}

Generate atleast 10 Mix (MCQ, Fill in the blank, Short answer) high-quality logical reasoning questions.
Questions should involve:
- decision making
- cause-effect
- trade-offs
- ethical reasoning
- scenario thinking

Return STRICT JSON only.

Format:

[
  {{
    "type": "mcq",
    "question": "...",
    "options": ["A","B","C","D"],
    "answer": "correct option"
  }},
  {{
    "type": "fill",
    "question": "...",
    "answer": "correct answer"
  }},
  {{
    "type": "short",
    "question": "...",
    "answer": "..."
  }}
]
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You design reasoning problems."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    questions = json.loads(response.choices[0].message.content)

    return questions


# Prompt to choose best games out of 4 based on the content
def choose_best_game(knowledge_base, client, model):
    prompt = f"""
You are an expert in educational game design.

Based on the logical complexity and structure of the knowledge base,
choose the BEST game type from the list below.

Choose ONLY ONE.

Game types:
1. Scenario Decision Game
2. Cause-Effect Mapping
3. Identify the Misconception
4. Fix the Logic

IMPORTANT:
- Return ONLY valid JSON.
- Do NOT add explanation.
- Do NOT use markdown.
- Output must be parseable.

If you choose Scenario Decision Game:
{{
"type": "Scenario Decision Game",
"scenario": "...",
"options": ["A","B","C","D"],
"answer": "correct option"
}}

If you choose Cause-Effect Mapping:
{{
"type": "Cause-Effect Mapping",
"statements": "...",
"options": ["Cause → Effect", "Effect → Cause"],
"answer": "correct option"
}}

If you choose Identify the Misconception:
{{
"type": "Identify the Misconception",
"statement": "...",
"options": ["True","False"],
"answer": "correct option"
}}

If you choose Fix the Logic:
{{
"type": "Fix the Logic",
"statement": "...",
"answer": "correct explanation"
}}

Knowledge Base:
{knowledge_base}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert game designer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    game_config = json.loads(response.choices[0].message.content)

    return game_config



