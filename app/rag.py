import os
from typing import List, Dict, Tuple
import re
from dotenv import load_dotenv
import chromadb
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in .env")

# Initialize Clients
groq_client = Groq(api_key=GROQ_API_KEY)
chroma_client = chromadb.PersistentClient(path="chroma_store")
COLLECTION_NAME = "pathsetter_docs"

def generate_answer(messages: List[Dict[str, str]]) -> Tuple[str, List[str]]:
    """
    1. Extract latest user message.
    2. Retrieve context from Chroma (fast).
    3. Send History + Context to Groq (8b-instant).
    """

    # 1. Validate input and get the latest user question
    if not messages:
        return "I couldn't find a question to answer. Please send a message.", []

    latest_query = messages[-1].get('content', '').strip()
    if not latest_query:
        return "Please type a question and try again.", []

    # Quick heuristics to keep conversation natural
    low = latest_query.lower()

    # 1) Greeting => short friendly reply (do not call model)
    if re.match(r"^(hi|hello|hey|h[iy]{1,2}|hiya|good (morning|afternoon|evening))(\b|[!.,?])",
                low):
        return ("Hi — I'm Alfred. I can help with Pathsetter project questions. What would you like to know?"), []

    # 2) Very short/ambiguous inputs (e.g., 'info', 'company') => ask clarifying question
    words = low.split()
    question_words = {'what','how','why','who','when','where','does','do','is','are','explain','describe','tell'}
    if len(words) <= 3 and not any(w in question_words for w in words) and not low.endswith('?'):
        return ("Could you please clarify what you'd like to know about Pathsetter or Alfred?"), []

    # 2. Retrieve relevant chunks (Limit to 3 for max speed)
    # 2. Retrieve relevant chunks (limit to 3 for speed)
    try:
        collection = chroma_client.get_collection(COLLECTION_NAME)
        results = collection.query(query_texts=[latest_query], n_results=3)
        # results["documents"] is a list per query; take first
        chunks = results.get("documents", [[]])[0]
    except Exception:
        chunks = []

    # Prepare a single context string (may be empty)
    context_text = "\n\n".join(chunks) if chunks else ""

    # 3. System instruction: ask the model to be conversational and simple
    system_instruction = (
        "You are an expert assistant for Pathsetter's infrastructure."
        " Use the retrieved context to answer the user's question when possible."
        " Guidelines:"
        " - Be conversational and friendly."
        " - Use simple, plain language and avoid jargon."
        " - Keep answers short (1-3 sentences) unless the user asks for more detail."
        " - If the answer is not contained in the provided context, respond:"
        " 'I do not have sufficient information to answer that.'"
        " - If the user's question is ambiguous, ask one concise clarifying question."
        "\n\n"
    )

    # Build messages: system prompt (with context) then the conversation history
    final_messages = [
        {"role": "system", "content": system_instruction + ("\nContext:\n" + context_text if context_text else "\nContext: <none retrieved>")}
    ]
    final_messages.extend(messages)

    # 5. Call Groq (Using the FASTEST model)
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=final_messages,
            temperature=0.25,
            max_tokens=256
        )
        # normalize extraction depending on response shape
        answer = getattr(completion.choices[0].message, 'content', None) or completion.choices[0].message.content
        # Ensure string
        if not isinstance(answer, str):
            answer = str(answer)
    except Exception as e:
        # friendly fallback
        answer = "I'm having trouble processing that right now — please try again shortly."

    return answer.strip(), chunks
# openai/gpt-oss-120b

