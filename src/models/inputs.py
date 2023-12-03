from pydantic import BaseModel, Field


class Query(BaseModel):
    """
    Model to describe the structure of the request body for the database agent.
    Also used as a base class for other agents. Performs validation on the
    request body.
    """

    query: str = Field(
        ...,
        max_length=250,
        title="Query",
        description="Query to ask the agent",
        examples=[""],
    )
