from fastapi import FastAPI

# Tạo ứng dụng FastAPI
app = FastAPI()

# Endpoint 1: Trang gốc
@app.get("/")
def read_root():
    return {"message": "Chào mừng bạn đến với FastAPI!"}

# Endpoint 2: Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}
