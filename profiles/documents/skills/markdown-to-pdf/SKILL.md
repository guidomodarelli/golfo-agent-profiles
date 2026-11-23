---
name: markdown-to-pdf
description: >-
  Genera el PDF, o el Word si lo piden, de un documento de la oficina desde su
  Markdown, en output/, con pandoc y typst; y pasa a Markdown un Word que alguien
  subió, para trabajar sobre ese texto. Usar siempre que haya que entregar, imprimir,
  mandar o exportar un acta, carta, informe o escrito como PDF o Word, que regenerar
  uno después de cambiar su Markdown, o que trabajar sobre un .docx recibido, aunque el
  pedido solo diga "pasámelo a PDF", "mandale el acta al cliente" o "abrí el Word que
  me mandaron". No usar para editar el contenido del documento: eso se hace en el .md.
license: MIT
metadata:
  version: "1.0.0"
  tags: "documents, pdf, word, markdown, pandoc"
---

# Markdown to PDF

The documents of the office are Markdown: the PDF or Word file is only an output, generated again whenever the Markdown changes. The rules this procedure applies live in `.agents/rules/documents.md`.

## 1. Check the tools

The `documents` profile installs `pandoc` and `typst` on the PATH of the repository when `agent-ready apply` runs.

```bash
pandoc --version && typst --version
```

If either is missing, do not install it some other way: tell the person to run `agent-ready apply` (the profile `documents` installs both, once the security policy allows its CLIs) and stop.

## 2. Generate a PDF or a Word file

Generate from the Markdown, never by editing an earlier output. Keep the same name and the same folder structure under `output/`, so the file is easy to find and the next generation replaces it:

```bash
mkdir -p output/actas
pandoc actas/acta-4512.md -o output/actas/acta-4512.pdf --pdf-engine=typst
pandoc actas/acta-4512.md -o output/actas/acta-4512.docx
```

- `output/` is ignored by Git. Never commit what is there and never move it out of `output/` to version it: any machine generates it again.
- If pandoc fails, show the person its message in one line and fix the Markdown, not the output.
- Tell the person where the file is (`output/actas/acta-4512.pdf`).

## 3. Turn an uploaded Word file into Markdown

A Word file someone uploaded is an input: never edit it. Write its text next to it, with the same name, and work on that Markdown:

```bash
pandoc entradas/contrato-cliente.docx -t gfm -o entradas/contrato-cliente.md
```

- If the Markdown already exists, work on it instead of extracting it again: it may already have changes.
- Read the result once: pandoc keeps the text, the headings, the lists and the tables, but drops what Markdown cannot hold (colors, fonts, comments). Mention what was lost if it matters for the document.
- An uploaded PDF is not converted with pandoc: read it yourself and transcribe it to its `.md`, marking with `[illegible]` what cannot be read.
