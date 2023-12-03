from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    answer: str = Field(
        ...,
        title="Answer",
        description="The answer to the question",
        examples=["Hello World"],
    )
    sources: list = Field(
        ...,
        title="Sources",
        description="The sources used to answer the question",
        examples=["Hello World", "Hello World"],
    )
