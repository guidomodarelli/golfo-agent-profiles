---
trigger: always_on
---

# Documents

The documents of the office (records, letters, reports) live in this repository as Markdown, so several people can work on them and the sync of agent-ready merges their changes. A PDF or a Word file is either generated from that Markdown or an input someone uploaded; neither is ever edited.

<!-- rule id=documents/markdown-source -->
- Write and edit every document as a Markdown file (`.md`).
  - It is the only version of the document that is kept: Markdown can be compared and merged, so two people can change different parts of it at the same time.

<!-- rule id=documents/generated-output -->
- Generate a PDF, or a Word file when someone asks for one, from its Markdown into `output/`, with the `markdown-to-pdf` skill.
  - `output/` is ignored by Git: any machine generates the file again from the Markdown, so no binary is ever merged.
  - To change a generated document, change its Markdown and generate it again.

<!-- rule id=documents/inputs-read-only -->
- Never edit, rename or replace a PDF or Word file that someone uploaded.
  - It is an input, kept as it came: it is versioned once and stays as evidence of what was received.

<!-- rule id=documents/extracted-markdown -->
- Next to each uploaded PDF or Word file, write its content as a Markdown file named after the whole name of the input, and work on that file.
  - `acta-4512.pdf` gets `acta-4512.pdf.md`, and `acta-4512.docx` gets its own `acta-4512.docx.md`: two inputs never share one Markdown. If that Markdown already exists, work on it instead of extracting it again.
  - The `markdown-to-pdf` skill extracts a Word file; read a PDF yourself and transcribe it faithfully, marking with `[illegible]` what cannot be read.

<!-- rule id=documents/duplicate-names -->
- When a file arrives with the name of one already in its folder, keep both and add the date to the name of the new one.
  - `acta-4512.pdf` arrives again: save it as `acta-4512-2026-11-23.pdf`, never over the first one.
