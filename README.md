# DevOps Delivery Strategy — report sources

Source for the written report (Deliverable 1) and presentation (Deliverable 3) of the Learnkey Institute DevOps assessment, Scenario B. The artefact repository (Deliverable 2) is separate: **github.com/imranneta5555/DevOps**.

## Build

```bash
./build.sh          # assembles and renders out/DevOps_Delivery_Strategy.pdf
./build-slides.sh   # renders out/DevOps_Presentation.pdf (19 slides, 16:9)
python3 wordcount.py report.html                    # assessed word count, per part
python3 wordcount.py report.html --exclude-tables   # count with tables excluded too
```

Both scripts render through Playwright's Chromium so the report carries a page-number footer; `build.sh` falls back to the Google Chrome CLI if Playwright is unavailable.

## Layout

| Path | Purpose |
| --- | --- |
| `template.html` | Cover page, contents, and the placeholders the parts are inserted into |
| `parts/part1..6.html` | One file per report part — edit these, not `report.html` |
| `parts/appendix.html` | Appendix A (artefacts) and Appendix B (references) |
| `figures/*.html` | Inline SVG figures with captions, referenced by `<!-- FIGURE:name -->` markers |
| `slides-src.html` | Presentation deck source; reuses the same figure fragments |
| `styles.css` / `slides.css` | Print stylesheets for the report and the deck |
| `assemble.py` | Builds `report.html` and `slides.html`, and stamps the live word count onto the cover |
| `WRITING_GUIDE.md` | The argument for each part as notes to write the prose from |
| `AUDIT.md` | Rubric self-audit, known deviations and the submission checklist |
| `PRESENTATION_NOTES.md` | Speaker notes per slide and fifteen prepared defence answers |

`report.html` and `slides.html` are generated — they are not committed. Edit the sources and rebuild.

## Status

The structure, figures, tables, deck and build tooling are finished. **The prose in `parts/` is a structural reference and is meant to be rewritten** — see `WRITING_GUIDE.md` for the argument of each part in note form, and the checklist at the end of `AUDIT.md` for what is still outstanding.
