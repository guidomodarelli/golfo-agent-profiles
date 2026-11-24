---
trigger: always_on
---

# Testing Rules — Java

<!-- rule id=java-testing/junit-5-assertion-library -->
- Use JUnit 5 and the assertion library the project already uses (for example AssertJ).
  - Name tests after the behavior they verify.

<!-- rule id=java-testing/prefer-slice-tests-webmvctest -->
- Prefer slice tests (`@WebMvcTest`, `@DataJpaTest`) over `@SpringBootTest` when a single layer is under test.

<!-- rule id=java-testing/run-repository-sql-tests -->
- Run repository and SQL tests against a real database through Testcontainers or the project's test database, not an in-memory substitute with a different dialect.

<!-- rule id=java-testing/mockito-boundaries-project-owns -->
- Use Mockito only at the boundaries the project owns (repositories, outbound clients).
  - Do not mock the JDK, the framework, or value objects.

<!-- rule id=java-testing/test-controllers-through-mockmvc -->
- Test controllers through MockMvc or `WebTestClient` and assert status, headers, and body as the client sees them.

<!-- rule id=java-testing/mock-own-database-layer -->
- Do not mock your own database layer in integration tests.
  - See `Data` in `patterns-we-do-not-use.md`.
