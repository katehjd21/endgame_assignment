# Apprenticeship Coins API

## Project Overview

This project is a backend API for managing **coins, duties, and KSBs (Knowledge, Skills, and Behaviours)** related to apprenticeship training. The API allows users to **view, create, update, and delete coins**, as well as retrieve duties and KSBs, and see the associations between coins, duties, and KSBs.  

The API is built with **Flask** and uses a **PostgreSQL database** for storage. It is designed to be simple, extendable, and easily testable, with future plans to provide full CRUD functionality for duties and KSBs.

---

## Getting Started

### Prerequisites

- **Python 3.13.5**
- PostgreSQL database (configured in `pg_db_connection.py`)
- Virtual environment recommended (`.venv`)

### Installation

1. Clone this repository:

```bash
git clone https://github.com/katehjd21/endgame_assignment.git
cd endgame_assignment/backend
```

 2. Create a virtual environment:
 ```bash
 python3 -m venv .venv
 ```

 3. Activate the virtual environment:
 - On macOS/Linux:
 ```bash
 source .venv/bin/activate
 ```

 4. Install required packages
 ```bash
 pip install -r requirements.txt
 ```

---

## Running the Backend

Start the backend server with:

```bash
python3 app.py
```

By default, the server runs in debug mode and listens on `http://127.0.0.1:5000`.

---

## Testing the Endpoints

You can test the API endpoints using tools such as:  

- [Postman](https://www.postman.com/) (desktop or web)  
- [Insomnia](https://insomnia.rest/)  
- `curl` in your terminal  

### Example Requests

**To get all coins (v1):**
```http
GET http://127.0.0.1:5000/v1/coins
```


**To create a new coin (v2):**
```http
POST http://127.0.0.1:5000/v2/coins
Content-Type: application/json
{
  "name": "Example Coin",
  "duty_codes": ["D1", "D2"]
}
```

---

## Endpoint Documentation

All endpoints are documented in [endpoints.json](./endpoints.json), which includes:  

- Endpoint paths and HTTP methods  
- Descriptions of each endpoint  
- Example request bodies for POST/PATCH requests  
- Example responses  

This file is a complete reference for developers to understand how to interact with the API.

---

## Running Tests

Tests are written using **pytest**. To run all tests, make sure you are in the `backend` folder and run:

```bash
pytest tests/
```
Make sure your virtual environment (.venv) is active so all dependencies are available.

Tests cover endpoints for coins, duties, and ksbs including error handling and validation.

---

## Next Steps / Future Improvements

The current API supports full CRUD for **coins** and read operations for **duties and KSBs**.  

The next steps I would take would be to configure:  

1. **CRUD endpoints for Duties** – allowing users to create, read, update, and delete duties.  
2. **CRUD endpoints for KSBs** – allowing users to create, read, update, and delete Knowledge, Skills, and Behaviours.  