import chromadb
from chromadb.config import Settings
import yaml

HOST = "localhost"
PORT = "8000"


def main():
    chroma = chromadb.HttpClient(
        host=HOST,
        port=PORT,
        settings=Settings(chroma_api_impl="chromadb.api.fastapi.FastAPI"),
    )

    chroma.delete_collection("main")
    collection = chroma.create_collection("main")

    with open("seed.yaml", "r") as f:
        context = yaml.load(f, Loader=yaml.SafeLoader)

    collection.add(
        documents=[context[document]["body"] for document in context],
        metadatas=[
            dict(
                title=context[document]["title"],
                source=context[document]["link"],
            )
            for document in context
        ],
        ids=[str(i) for i in range(len(context))],
    )


if __name__ == "__main__":
    main()
