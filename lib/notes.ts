export type Note = {
  id: number;
  text: string;
  createdAt: string;
};

// Deliberately simple in-memory store: the app is a vehicle for the
// DevOps artefacts around it, not a product. State resets on restart.
let notes: Note[] = [];
let nextId = 1;

export function listNotes(): Note[] {
  return [...notes];
}

export function createNote(text: string): Note {
  const note: Note = {
    id: nextId++,
    text,
    createdAt: new Date().toISOString(),
  };
  notes.push(note);
  return note;
}

// Test helper: restores a clean slate between test cases.
export function resetNotes(): void {
  notes = [];
  nextId = 1;
}
