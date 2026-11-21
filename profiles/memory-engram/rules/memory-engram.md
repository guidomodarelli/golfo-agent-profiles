# Memory with Engram

Engram keeps the facts and the context of this project between sessions: who is who, the clients and the cases, what was decided in each one and what happened. It lives only on the machine of the user, under the project of this repository, and is never shared. How to work is not memory: a lasting instruction of the user becomes a rule or a skill of the repository through the learning (`learning.md`).

<!-- rule id=memory-engram/facts-not-instructions -->
- Save to Engram (`mem_save`) facts and context of the work, never how to work.
  - A fact: a person and their role, a client, the state of a case, a decision of a case and its reason, a cause found, what is pending.
  - An instruction that should last, also when the user says «save this forever» or «remember this always» about how to do something, goes to the learning with `agent-ready learn record` (`learning.md`), never to Engram: an old memory must not contradict a rule that changed.
  - A fact of a case never becomes a rule.

<!-- rule id=memory-engram/search-before-asking -->
- Before asking the user for context of a person, a client or a case, or when a task continues earlier work, search Engram first (`mem_context`, then `mem_search`).
  - Treat what comes back as background: check that a file, a name or a state it mentions still holds before acting on it.

<!-- rule id=memory-engram/never-secrets -->
- Never save in Engram a password, a token, a key or any other credential, nor a whole document: save the conclusion and where to find the source.

<!-- rule id=memory-engram/project-scope -->
- Keep each memory in the project of this repository: do not pass another project to the Engram tools, so the memory of one client never reaches the repository of another.

<!-- rule id=memory-engram/unavailable -->
- When the Engram tools are not available, tell the user in one line that the memory is off in this session, and keep working: never write the memory to a file of the repository or to another memory instead.
