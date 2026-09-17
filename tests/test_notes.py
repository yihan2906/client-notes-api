from fastapi.testclient import TestClient

from app.main import create_app
from app.repository import InMemoryNotesRepository


def make_client() -> TestClient:
    return TestClient(create_app(InMemoryNotesRepository()))


def test_assigned_user_can_list_notes() -> None:
    response = make_client().get(
        "/clients/client-1/notes", headers={"X-Author-Id": "author-1"}
    )

    assert response.status_code == 200
    assert response.json()[0]["content"] == "Initial client call completed."


def test_assigned_user_can_add_note() -> None:
    client = make_client()
    response = client.post(
        "/clients/client-1/notes",
        headers={"X-Author-Id": "author-1"},
        json={"content": "Book the next appointment."},
    )

    assert response.status_code == 201
    assert response.json()["author_id"] == "author-1"
    assert len(client.get(
        "/clients/client-1/notes", headers={"X-Author-Id": "author-1"}
    ).json()) == 2


def test_unassigned_user_is_forbidden() -> None:
    response = make_client().get(
        "/clients/client-1/notes", headers={"X-Author-Id": "author-2"}
    )

    assert response.status_code == 403


def test_unknown_client_is_not_found() -> None:
    response = make_client().get(
        "/clients/missing/notes", headers={"X-Author-Id": "author-1"}
    )

    assert response.status_code == 404
