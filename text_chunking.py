from langchain_text_splitters import RecursiveCharacterTextSplitter

def text_splitters(extracted_text):
    full_text = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=300)
    chunks = splitter.split_text(extracted_text)
    for i,chunk in enumerate(chunks):
        text = f"Chunk{i}:\n{chunk}"
        full_text.append(text)
    return full_text

text = """LangChain is a powerful framework for developing applications powered by language models.
It enables developers to chain together components like LLMs, prompts, and memory to create advanced conversational AI systems.
Text splitters in LangChain help break large documents into smaller pieces for processing."""


if __name__ == "__main__":
    result = text_splitters(text)
    print(result)