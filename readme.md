# Learn FastAPI

A Comprehensive Python API Course using FastAPI. This repo keeps track of all the lessons and exercises done while learning to build APIs from the scratch.

Part of a **100 days of code** challenge. Open [Logsheet](logsheet.md) to see the tasks each day done.

*Logsheet is dedicated to this repo only.*


---

## Tech Stack

- Python
- FastAPI
- Uvicorn
- SQLAlchemy

---

## Usage

1. First, clone this project *(git must be installed)*,
    ```bash
    git clone https://github.com/mearjunsingh/learn-fastapi.git
    ```

2. Then get inside that folder,
    ```bash
    cd learn-fastapi
    ```

3. Now make sure you have python installed. It is a best practice to install Python projects in a Virtual Environment. Install and create Virtual Envronment,
    ```bash
    pip install virtualenv
    virtualenv venv
    ```

4. Also we need to activate the virtual environment,
   - In windows
        ```bash
        venv\Scripts\activate
        ```
   - In Linux or Mac
        ```bash
        source venv/bin/activate
        ```

5. Then install dependencies,
    ```bash
    pip install -r requirements.txt
    ```

6. Now we are ready to run the project,
    ```bash
    uvicorn app.main:app --reload
    ```

7. Then locate http://127.0.0.1:8000/docs in browser for **SwaggerAPI** documentation or http://127.0.0.1:8000/redoc for **ReDoc** documentation.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.