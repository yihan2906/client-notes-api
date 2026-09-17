export interface Client {
  id: string;
  name: string;
}

export interface Author {
  id: string;
  name: string;
}

export interface Note {
  id: string;
  client_id: string;
  author_id: string;
  content: string;
  created_at: string;
}

export interface CreateNoteInput {
  content: string;
}

