""" This file is used to run a uvicorn server to listening a FastAPI app in port 3001. """
import uvicorn
import multiprocessing

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=3001, reload=True)