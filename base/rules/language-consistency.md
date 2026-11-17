# Language Consistency

Keep each file in a single language: the one it already uses.

<!-- rule id=language-consistency/editing-existing-file-write -->
- When editing an existing file, write every addition (prose, headings, list items, comments, examples, messages) in the language the file already uses.
  - Never mix languages within a file.

<!-- rule id=language-consistency/translate-existing-content-unless -->
- Do not translate existing content unless explicitly asked.

<!-- rule id=language-consistency/creating-new-file-language -->
- When creating a new file, use the language of sibling files of the same kind in the same directory.

<!-- rule id=language-consistency/keep-identifiers-paths-commands -->
- Keep identifiers, paths, commands, API names, error and log literals, and any text that must be preserved verbatim unchanged, whatever the language of the file.

<!-- rule id=language-consistency/files-hold-several-languages -->
- Files that hold several languages by design, such as translation catalogs, keep the language of each entry.

<!-- rule id=language-consistency/project-rule-sets-explicit -->
- If a project rule sets an explicit language for a kind of content (for example, specs in Spanish), that rule takes precedence.
