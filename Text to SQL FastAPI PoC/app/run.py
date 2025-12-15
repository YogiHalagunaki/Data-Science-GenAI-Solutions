import uvicorn
from views import app

if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=5000)
    uvicorn.run(app, host='127.0.0.1',port=5000) 
    