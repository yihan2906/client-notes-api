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

- **Use real sign-in.** The user switcher and `X-Author-Id` header are useful
  for this demo, but anyone can pretend to be another user. I would replace
  them with the company's login system and take the advisor ID from the
  verified login session.

- **Save the data in a database.** Notes currently disappear when the API
  restarts. I would add PostgreSQL tables for users, clients, assignments, and
  notes, then replace the in-memory repository with a database repository. The
  rest of the application could continue using the same repository interface.

- **Keep a history of note activity.** I would record who viewed or added a
  note, which client it belonged to, and when it happened. I would not put the
  note text in normal application logs because it may contain sensitive
  information.

- **Improve the API for larger amounts of data.** I would trim and validate
  note content on the backend, return consistent error messages, and add
  pagination so the API does not return every note at once for long-running
  clients.

- **Tidy up the frontend.** `App.tsx` is doing several jobs at the moment. I
  would separate the user/client selector, note form, and note list into
  smaller components. I would also cancel outdated requests so switching
  clients quickly cannot display a response from the previous client.

- **Add more tests.** I would add frontend tests for loading, errors, and form
  submission, plus an end-to-end test that selects a user, opens a client, and
  creates a note. On the backend, I would add tests using a real test database
  and cover missing login details, invalid content, and repeated requests.

- **Prepare it for deployment.** I would add Docker configuration and a CI
  workflow that runs the tests and frontend build for every change. I would
  also add useful server logs, error monitoring, and a database-aware health
  check so problems are easier to find after deployment.
