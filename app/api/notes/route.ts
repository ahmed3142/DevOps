import { NextResponse } from "next/server";
import { createNote, listNotes } from "@/lib/notes";

export async function GET() {
  return NextResponse.json({ notes: listNotes() });
}

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Request body must be JSON" }, { status: 400 });
  }

  const text = (body as { text?: unknown })?.text;
  if (typeof text !== "string" || text.trim() === "") {
    return NextResponse.json({ error: "'text' is required" }, { status: 400 });
  }

  const note = createNote(text.trim());
  return NextResponse.json({ note }, { status: 201 });
}
