import os

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv, find_dotenv
import yaml

HOST = "localhost"
PORT = "8000"


load_dotenv(find_dotenv())


def main():
    chroma = chromadb.HttpClient(
        host=HOST,
        port=PORT,
        settings=Settings(chroma_api_impl="chromadb.api.fastapi.FastAPI"),
    )

    openai_ef = OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"], model_name="text-embedding-ada-002"
    )

    chroma.delete_collection("main")
    collection = chroma.create_collection("main", embedding_function=openai_ef)

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
