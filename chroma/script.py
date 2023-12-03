import chromadb
import yaml

from ..src.utils.config import Config


def main():
    config = Config.get()
    chroma_kwargs = config.chromadb.to_dict()
    chroma = chromadb.HttpClient(**chroma_kwargs)

    collection = chroma.create_collection("main")

    with open("seed.yaml", "r") as f:
        context = yaml.load(f, Loader=yaml.SafeLoader)

    collection.add(
        documents=[document["body"] for document in context],
        metadatas=[
            dict(
                title=document["title"],
                source=document["link"],
            )
            for document in context
        ],
        ids=[str(i) for i in range(len(context))],
    )


if __name__ == "__main__":
    main()
