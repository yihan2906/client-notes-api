import { FormEvent, useCallback, useEffect, useState } from "react";

import {
  createNote,
  getAssignedClients,
  getDemoAuthors,
  getNotes,
} from "./api";
import type { Author, Client, Note } from "./types";

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en-SG", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export default function App() {
  const [authors, setAuthors] = useState<Author[]>([]);
  const [authorId, setAuthorId] = useState("");
  const [clients, setClients] = useState<Client[]>([]);
  const [clientId, setClientId] = useState("");
  const [notes, setNotes] = useState<Note[]>([]);
  const [content, setContent] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  const selectedClient = clients.find((client) => client.id === clientId);
  const selectedAuthor = authors.find((author) => author.id === authorId);

  function handleAuthorChange(nextAuthorId: string) {
    setAuthorId(nextAuthorId);
    setClients([]);
    setClientId("");
    setNotes([]);
    setContent("");
    setIsLoading(true);
  }

  useEffect(() => {
    let cancelled = false;

    async function loadAuthors() {
      setIsLoading(true);
      setError(null);
      try {
        const loadedAuthors = await getDemoAuthors();
        if (cancelled) return;
        setAuthors(loadedAuthors);
        setAuthorId(loadedAuthors[0]?.id ?? "");
        if (loadedAuthors.length === 0) {
          setError("No demo users are available.");
          setIsLoading(false);
        }
      } catch (requestError) {
        if (cancelled) return;
        setError(
          requestError instanceof Error
            ? requestError.message
            : "Unable to load demo users.",
        );
        setIsLoading(false);
      }
    }

    void loadAuthors();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!authorId) return;

    let cancelled = false;

    async function loadClients() {
      setIsLoading(true);
      setError(null);
      try {
        const loadedClients = await getAssignedClients(authorId);
        if (cancelled) return;
        setClients(loadedClients);
        setClientId(loadedClients[0]?.id ?? "");
        if (loadedClients.length === 0) {
          setNotes([]);
          setIsLoading(false);
        }
      } catch (requestError) {
        if (cancelled) return;
        setClients([]);
        setClientId("");
        setNotes([]);
        setError(
          requestError instanceof Error
            ? requestError.message
            : "Unable to load assigned clients.",
        );
        setIsLoading(false);
      }
    }

    void loadClients();
    return () => {
      cancelled = true;
    };
  }, [authorId]);

  const loadNotes = useCallback(async () => {
    if (!clientId || !authorId) return;
    setIsLoading(true);
    setError(null);
    try {
      setNotes(await getNotes(clientId, authorId));
    } catch (requestError) {
      setNotes([]);
      setError(
        requestError instanceof Error ? requestError.message : "Unable to load notes.",
      );
    } finally {
      setIsLoading(false);
    }
  }, [authorId, clientId]);

  useEffect(() => {
    void loadNotes();
  }, [loadNotes]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedContent = content.trim();
    if (!trimmedContent || !clientId || !authorId) return;

    setIsSaving(true);
    setError(null);
    try {
      const note = await createNote(clientId, authorId, {
        content: trimmedContent,
      });
      setNotes((currentNotes) => [...currentNotes, note]);
      setContent("");
    } catch (requestError) {
      setError(
        requestError instanceof Error ? requestError.message : "Unable to add note.",
      );
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace" aria-labelledby="page-title">
        <header className="topbar">
          <div className="brand-mark" aria-hidden="true">CN</div>
          <div>
            <p className="eyebrow">Care team workspace</p>
            <h1 id="page-title">Client notes</h1>
          </div>
          <div className="identity">
            <span className="identity-label">Viewing as</span>
            <strong>{selectedAuthor?.name ?? "Loading…"}</strong>
          </div>
        </header>

        <div className="content-grid">
          <aside className="sidebar" aria-label="Demo controls">
            <div>
              <p className="section-label">Workspace</p>
              <label htmlFor="client">Client</label>
              <select
                id="client"
                value={clientId}
                onChange={(event) => setClientId(event.target.value)}
                disabled={clients.length === 0}
              >
                {clients.length === 0 && (
                  <option value="">No assigned clients</option>
                )}
                {clients.map((client) => (
                  <option key={client.id} value={client.id}>
                    {client.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <p className="section-label">Demo identity</p>
              <label htmlFor="author">Current user</label>
              <select
                id="author"
                value={authorId}
                onChange={(event) => handleAuthorChange(event.target.value)}
                disabled={authors.length === 0}
              >
                {authors.length === 0 && <option value="">Loading users…</option>}
                {authors.map((author) => (
                  <option key={author.id} value={author.id}>
                    {author.name}
                  </option>
                ))}
              </select>
              <p className="helper-text">
                Each demo user sees only their assigned clients.
              </p>
            </div>

            <div className="assignment-card">
              <span className="status-dot" aria-hidden="true" />
              <div>
                <strong>Assignment rule</strong>
                <p>Clients are loaded from the API for the selected user.</p>
              </div>
            </div>
          </aside>

          <section className="notes-panel" aria-labelledby="notes-heading">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">{selectedClient?.id ?? "No client"}</p>
                <h2 id="notes-heading">
                  {selectedClient?.name ?? "No assigned client"}
                </h2>
              </div>
              <span className="note-count">
                {notes.length} {notes.length === 1 ? "note" : "notes"}
              </span>
            </div>

            <form className="note-form" onSubmit={handleSubmit}>
              <label htmlFor="note-content">Add a note</label>
              <textarea
                id="note-content"
                maxLength={2000}
                placeholder={
                  selectedClient
                    ? `Write an update for ${selectedClient.name}…`
                    : "Select an assigned client"
                }
                value={content}
                onChange={(event) => setContent(event.target.value)}
                disabled={isSaving || !selectedClient}
              />
              <div className="form-footer">
                <span>{content.length}/2000</span>
                <button
                  type="submit"
                  disabled={isSaving || !selectedClient || !content.trim()}
                >
                  {isSaving ? "Saving…" : "Add note"}
                </button>
              </div>
            </form>

            {error && (
              <div className="error-message" role="alert">
                <strong>Access unavailable</strong>
                <span>{error}</span>
              </div>
            )}

            <div className="notes-list" aria-live="polite">
              {isLoading ? (
                <div className="empty-state">Loading notes…</div>
              ) : notes.length === 0 && !error ? (
                <div className="empty-state">
                  {selectedClient
                    ? "No notes yet. Add the first update above."
                    : "No clients are assigned to this user."}
                </div>
              ) : (
                notes.map((note) => (
                  <article className="note-card" key={note.id}>
                    <div className="avatar" aria-hidden="true">
                      {note.author_id.slice(-1)}
                    </div>
                    <div>
                      <div className="note-meta">
                        <strong>{note.author_id}</strong>
                        <time dateTime={note.created_at}>
                          {formatDate(note.created_at)}
                        </time>
                      </div>
                      <p>{note.content}</p>
                    </div>
                  </article>
                ))
              )}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}
