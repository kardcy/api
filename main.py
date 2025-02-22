import csv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class UserCreate(BaseModel):
    user_id: int
    username: str

# Define the CSV file name where data will be saved
CSV_FILE = "users.csv"

# Function to write to CSV
def write_to_csv(user_id: int, username: str):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, username])

# Function to read from CSV
def read_from_csv() -> List[dict]:
    users = []
    try:
        with open(CSV_FILE, mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                users.append({"user_id": int(row[0]), "username": row[1]})
    except FileNotFoundError:
        pass  # If file doesn't exist yet, just return empty list
    return users

@app.post("/create_user/")
async def create_user(user_data: UserCreate):
    user_id = user_data.user_id
    username = user_data.username
    
    # Write data to CSV
    write_to_csv(user_id, username)
    
    return {
        "msg": "We got data successfully",
        "user_id": user_id,
        "username": username,
    }


@app.get("/")
async def get_users():
    return {"users": "welcom"}
@app.get("/get_users/")
async def get_users():
    # Read users from CSV
    users = read_from_csv()
    return {"users": users}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

