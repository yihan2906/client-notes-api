import type { Author, Client, CreateNoteInput, Note } from "./types";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function request<T>(
  path: string,
  authorId?: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(authorId ? { "X-Author-Id": authorId } : {}),
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as
      | { detail?: string }
      | null;
    throw new Error(body?.detail ?? "Something went wrong. Please try again.");
  }

  return response.json() as Promise<T>;
}

export function getDemoAuthors(): Promise<Author[]> {
  return request<Author[]>("/demo/authors");
}

export function getNotes(clientId: string, authorId: string): Promise<Note[]> {
  return request<Note[]>(`/clients/${clientId}/notes`, authorId);
}

export function getAssignedClients(authorId: string): Promise<Client[]> {
  return request<Client[]>("/clients", authorId);
}

export function createNote(
  clientId: string,
  authorId: string,
  input: CreateNoteInput,
): Promise<Note> {
  return request<Note>(`/clients/${clientId}/notes`, authorId, {
    method: "POST",
    body: JSON.stringify(input),
  });
}
