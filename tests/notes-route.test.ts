import { beforeEach, describe, expect, it } from "vitest";
import { GET, POST } from "@/app/api/notes/route";
import { resetNotes } from "@/lib/notes";

function jsonRequest(body: unknown): Request {
  return new Request("http://localhost/api/notes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

describe("/api/notes", () => {
  beforeEach(() => resetNotes());

  it("rejects a missing text field with 400", async () => {
    const res = await POST(jsonRequest({}));
    expect(res.status).toBe(400);
  });

  it("rejects blank text with 400", async () => {
    const res = await POST(jsonRequest({ text: "   " }));
    expect(res.status).toBe(400);
  });

  it("creates a note and returns it in the list", async () => {
    const created = await POST(jsonRequest({ text: "ship v1.0.0" }));
    expect(created.status).toBe(201);

    const res = await GET();
    const body = await res.json();
    expect(body.notes).toHaveLength(1);
    expect(body.notes[0].text).toBe("ship v1.0.0");
  });
});
