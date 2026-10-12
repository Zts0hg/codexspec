### P-2026-1010-21225w-2: Plugin installation does not load project initialization context

- claim: A rule intended to apply before any plugin command must have an automatic plugin context entry, independently of rules written by project init.
- type: pitfall
- scope/when: adding agent behavior shared by CLI-initialized projects and marketplace-only Claude installations
- root-cause: Project init writes CLAUDE.md, but marketplace-only users do not run init. A CLAUDE.md placed in the plugin root is not loaded as context either, and an available slash command is not itself an instruction to invoke it proactively.
- workaround: Keep the rule in a shared renderer and provide an appropriate automatic plugin entry, such as SessionStart stdout context from hooks/hooks.json. Test the installed plugin root with no project init or CodexSpec CLI, and verify that the named command is discoverable under the marketplace's declared command path.
- lesson: Validate the context-loading entry for every supported installation mode separately from validating command availability and runtime dependencies.
- evidence.facts: The commit guidance existed only in init-managed context until test_session_start_emits_commit_rule_without_cli exercised the plugin and fresh installer artifacts. Its four repository/plain-directory cases now emit the same rule without project writes. Claude's official plugin reference documents that plugin-root CLAUDE.md is not loaded; its hooks reference documents SessionStart stdout context.
- evidence.state: Verified for feature 2026-1010-21225w using local hook execution and Claude Code 2.1.296 marketplace validation; see [plugin reference](https://code.claude.com/docs/en/plugins-reference) and [hooks reference](https://code.claude.com/docs/en/hooks). Actual agent adherence is not a deterministic guarantee.
- provenance: distill @implement-tasks, 2026-10-11, derivation: inferred, confidence: high
- status: candidate
