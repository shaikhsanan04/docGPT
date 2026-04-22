import json
import chromadb
import ollama


# Load chunks

with open("jsons/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


# Init Chroma (persistent)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="my_chunks")


# Resume logic

existing_data = collection.get()
existing_ids = set(existing_data["ids"]) if existing_data["ids"] else set()

new_chunks = []
new_ids = []

for i, chunk in enumerate(chunks):
    if str(i) not in existing_ids:
        new_chunks.append(chunk)
        new_ids.append(str(i))

print("Already stored:", len(existing_ids))
print("Remaining:", len(new_chunks))


# Config 

BATCH_SIZE = 32   


# Main loop

total = len(new_chunks)

for i in range(0, total, BATCH_SIZE):
    batch = new_chunks[i:i+BATCH_SIZE]
    batch_ids = new_ids[i:i+BATCH_SIZE]

    print(f"Processing {i + 1} -> {i + len(batch)} / {total}")

    response = ollama.embed(
        model="nomic-embed-text-v2-moe",
        input=batch
    )

    embeddings = response["embeddings"]

    collection.add(
        documents=batch,
        embeddings=embeddings,
        ids=batch_ids
    )

print("All embeddings stored successfully")

# This will print the embeddings alongside the documents
print(collection.get(include=["embeddings", "documents"]))