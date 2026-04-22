from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

with open("files/content.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,          # smaller, more precise
    chunk_overlap=100,       # enough context, less duplication
    separators=[
        "\n\n",              # paragraph
        "\n",                # line
        ". ",                # sentence
        " "                  # fallback
    ]
)

chunks = text_splitter.split_text(full_text)

with open("jsons/chunks.json", "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)

print(f"Created {len(chunks)} chunks")