import { beforeEach, describe, expect, it } from "vitest";
import { createNote, listNotes, resetNotes } from "@/lib/notes";

describe("notes store", () => {
  beforeEach(() => resetNotes());

  it("starts empty", () => {
    expect(listNotes()).toEqual([]);
  });

  it("assigns incrementing ids and timestamps on create", () => {
    const first = createNote("write the DevOps report");
    const second = createNote("record the presentation");
    expect(first.id).toBe(1);
    expect(second.id).toBe(2);
    expect(Date.parse(first.createdAt)).not.toBeNaN();
    expect(listNotes()).toHaveLength(2);
  });
});
