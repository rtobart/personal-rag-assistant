from datetime import datetime

from fastapi import Request, Response

from app.logger.logger import LoggerInstance
from datetime import datetime

from datetime import datetime


async def log_request(request: Request, call_next):
    """
    Request wrapper. Logging purposes or metrics.
    """
    start = datetime.now()
    calldata = "REQUEST METHOD: " + request.method + "- URL: " + str(request.url) + "\n"
    response: Response = await call_next(request)
    end = datetime.now()
    difference = (end - start).total_seconds()
    LoggerInstance.info(
        calldata
        + f"\nRESPONSE STATUS: {str(response.status_code)}  tiempo de ejecion : {difference}"
    )
    return response
