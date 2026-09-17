# Client Notes

A thin end-to-end implementation of an internal advisor notes feature using
FastAPI, React, and TypeScript.

## What I implemented

- A FastAPI API for listing and adding notes for a client.
- A React and TypeScript UI for selecting a demo advisor, viewing their
  assigned clients, reading notes, and adding a note.
- Typed models for authors, clients, note creation, and note responses.
- A mocked authentication context using the `X-Author-Id` request header.
- Backend authorization that checks the advisor is assigned to the requested
  client before allowing reads or writes.
- An in-memory repository behind a typed interface so it can be replaced with
  database-backed persistence.
- Dependency injection and an application factory to keep the API testable.
- Backend tests covering successful reads and writes, multiple assignments,
  forbidden access, missing clients, and the demo data endpoints.

The frontend gets its demo users and assigned clients from the API rather than
duplicating that data in React. Authentication is intentionally mocked and
notes are stored only in memory, so notes reset whenever the API restarts.

Seeded assignments:

- `author-1` can access `client-1` and `client-3`.
- `author-2` can access `client-2` and `client-4`.

## How to run it

### Backend

From the project root in PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Open
`http://127.0.0.1:8000/docs` for its interactive documentation.

### Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

### Tests

From the project root:

```powershell
.venv\Scripts\python.exe -m pytest
```

To verify the frontend production build:

```powershell
cd frontend
npm run build
```

## API examples

```powershell
curl.exe -H "X-Author-Id: author-1" http://127.0.0.1:8000/clients/client-1/notes

curl.exe -X POST http://127.0.0.1:8000/clients/client-1/notes `
  -H "X-Author-Id: author-1" `
  -H "Content-Type: application/json" `
  -d '{"content":"Follow up next Tuesday"}'
```

## Project structure

- `app/routers/` handles HTTP routes and dependencies.
- `app/services.py` contains authorization and use-case logic.
- `app/repository.py` contains the persistence interface and in-memory data.
- `app/models.py` contains the typed API and domain models.
- `frontend/src/` contains the React UI and typed API client.
- `tests/` contains the backend API tests.

## What I would do next with more time

- Replace the fake author header and demo-user endpoint with verified SSO or
  OAuth/JWT authentication.
- Store clients, assignments, and notes in a relational database with
  migrations and transactions.
- Add audit logging for note access and changes.
- Add pagination and sorting controls for clients with many notes.
- Add rate limiting, structured logging, and production error monitoring.
- Add frontend component and end-to-end tests, including rapid user/client
  switching and failed API requests.
- Add deployment configuration and continuous integration for tests and builds.
