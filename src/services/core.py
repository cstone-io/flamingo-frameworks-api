from ..models.core import Query

"""
Public Services
"""


async def chat(body: Query) -> str:
    """
    Text report agent controller. This controller is responsible for handling
    requests to the /agents/text route.

    :param body: Query object
    :returns: string answer for successful requests
    """
    pass
