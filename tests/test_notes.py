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


def test_each_user_can_access_a_second_assigned_client() -> None:
    client = make_client()

    author_one_response = client.get(
        "/clients/client-3/notes", headers={"X-Author-Id": "author-1"}
    )
    author_two_response = client.get(
        "/clients/client-4/notes", headers={"X-Author-Id": "author-2"}
    )

    assert author_one_response.status_code == 200
    assert author_two_response.status_code == 200


def test_users_only_receive_their_assigned_clients() -> None:
    client = make_client()

    author_one_clients = client.get(
        "/clients", headers={"X-Author-Id": "author-1"}
    ).json()
    author_two_clients = client.get(
        "/clients", headers={"X-Author-Id": "author-2"}
    ).json()

    assert {item["id"] for item in author_one_clients} == {"client-1", "client-3"}
    assert {item["id"] for item in author_two_clients} == {"client-2", "client-4"}


def test_demo_authors_are_loaded_from_the_api() -> None:
    response = make_client().get("/demo/authors")

    assert response.status_code == 200
    assert response.json() == [
        {"id": "author-1", "name": "Maya Chen"},
        {"id": "author-2", "name": "Jon Bell"},
    ]


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
