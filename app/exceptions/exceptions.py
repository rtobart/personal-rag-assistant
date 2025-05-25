from fastapi.exceptions import HTTPException

PROCESS_ERROR = "PROCESS ERROR - "


class BadRequest(HTTPException):
    def __init__(self, status_code: int = 400, detail: str = "Bad request"):
        super().__init__(status_code=status_code, detail=detail)


class EnvironmentFileNotFound(HTTPException):
    def __init__(self, status_code: int = 500, message="Environment file not found"):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)


class EnvironmentVarNotFound(HTTPException):
    def __init__(
        self, status_code: int = 500, message="Environment variable not found"
    ):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)


class PromptLoadingException(HTTPException):
    def __init__(self, status_code: int = 500, message="Couldn't load prompt files."):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)


class ProxyException(HTTPException):
    def __init__(
        self, status_code: int = 500, message="Couldn't answer the proxy service."
    ):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)


class ProxyEmbeddingException(HTTPException):
    def __init__(self, status_code: int = 500, message="Error in getting embeddings."):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)


class NearestNeighborException(HTTPException):
    def __init__(
        self, status_code: int = 500, message="Error in getting nearest neighbors."
    ):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)


class ServicePointInsertionError(HTTPException):
    def __init__(self, status_code: int = 500, message="Service point error."):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)


class ChromaDBSaveDataException(HTTPException):
    def __init__(
        self, status_code: int = 500, message="Chroma service error inserting data."
    ):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)


class ChromaDBGetDataException(HTTPException):
    def __init__(
        self, status_code: int = 500, message="Chroma service error retrieving data."
    ):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)


class SemanticCacheException(HTTPException):
    def __init__(self, status_code: int = 500, message="Error using semantic cache."):
        super().__init__(status_code=status_code, detail=PROCESS_ERROR + message)

class DatabaseConnectionError(Exception):
    def __init__(self, message="Can't connect with database."):
        self.message = f"{PROCESS_ERROR} - {message}"
        super().__init__(self.message)
        
class DatabaseOffline(HTTPException):
    def __init__(self, status_code: int = 500, message: str = "Database is offline"):
        super().__init__(status_code=status_code, detail=message)

class InvalidQuery(HTTPException):
    def __init__(self, status_code: int = 400, message: str = "Invalid query"):
        super().__init__(status_code=status_code, detail=message)