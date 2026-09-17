# Client Notes API

A deliberately small FastAPI take-home project. It demonstrates typed models,
authorization at the service boundary, an in-memory repository, and testable
dependency injection without adding database or authentication setup.

## Run it

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.
The fake authenticated user is supplied in the `X-Author-Id` header.
The demo UI loads its fake users and their assigned clients from the API; it
does not duplicate that domain data in React.

In a second terminal, start the React + TypeScript frontend:

```powershell
cd frontend
npm install
npm run dev
```

Then open `http://127.0.0.1:5173`.

Seeded assignments:

- `author-1` can access `client-1` and `client-3`
- `author-2` can access `client-2` and `client-4`

## Examples

```powershell
curl.exe -H "X-Author-Id: author-1" http://127.0.0.1:8000/clients/client-1/notes

curl.exe -X POST http://127.0.0.1:8000/clients/client-1/notes `
  -H "X-Author-Id: author-1" `
  -H "Content-Type: application/json" `
  -d '{"content":"Follow up next Tuesday"}'
```

Run tests with `pytest`.

## Structure and production follow-ups

- `routers/` owns HTTP concerns.
- `services.py` owns authorization and use-case logic.
- `repository.py` isolates persistence behind a small interface.
- `models.py` contains typed domain/API models.
- `frontend/src/` contains the typed React UI and API client.

For production, the repository would be backed by a database, the user ID and
assignments would come from verified auth/authorization data, and writes would
include transactions, auditing, pagination, and structured logging.
