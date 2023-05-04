import uvicorn
import sys
import os

diratual = os.getcwd()
sys.path.append(diratual + '/api/processamento')

if __name__ == "__main__":
    uvicorn.run("api.api:app", uds="../iarandu.sock", host="0.0.0.0", port=4002, reload=True)
