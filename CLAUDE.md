# pm-os-playbook

The PMOS Playbook is the PM layer of PMOS: skills, agents, rules and prompts for product
management work, plus the PMOS types they work on. `pmos` installs it into a
product workspace at a pinned ref. Product spec: `brgn81/pm-os` (`docs/`). PMOS contracts:
the schemas attached to each `pm-os-footing` release.

## Repo structure

```text
manifest.yaml        name, version, requires_pmos
types.yaml           the PMOS types: name, description, icon, color slot, template
preset/pmos.yaml  the starting configuration a new workspace gets
playbook.md          base rules; the workspace CLAUDE.md imports it
skills/<pack>/<skill>/SKILL.md
agents/*.md          Claude Code subagents and Copilot agents, shared frontmatter
rules/*.md           path-scoped authoring rules
commands/*.md        slash-command workflows
templates/*.md       item templates referenced by types.yaml
hooks/*.py           hooks, Python run with uv run, dependencies inline (PEP 723)
LICENSE, NOTICE      MIT; NOTICE credits phuryn/pm-skills (MIT)
```

`pmos` places `skills/`, `agents/`, `rules/`, `commands/` and `playbook.md` under the
workspace's `.claude/`. Paths inside skills refer to that installed layout.

## Invariants – never break these

- Talk to the tool only through `pmos`, always with `--json`. Never import its code,
  never reference `.claude/lib`, `item_sync.py` or any other internals.
- Never hardcode a workspace folder. Resolve it: `pmos where --pmos-type <type>`.
  A type the workspace has not mapped returns nothing: say so, do not guess a path.
- Read only the identity frontmatter (`item_id`, `title`, `url`) and the body of an item.
  Never depend on tool-specific fields; Jira, Confluence and Notion items look different.
- Every PMOS type a skill reads or writes is declared in `types.yaml`. A new type means
  `types.yaml` + `preset/pmos.yaml` + template, in one change.
- Never write into folders of category `context`. Write only to `work` and local types.
- Sync only through `/pull`, `/push`, `/status` or `pmos pull|push|status`. On a blocked item
  present the guidance options to the user; never choose one, never jump to `--force`.
- No product-specific content: no customer or company names, project keys, site URLs.
  Examples use the neutral sample product "Acme Planner".
- Never rename or remove a skill, agent, command or type in a minor version.
- Hooks are Python with `uv run`. No bash, no Node.

## Writing skills

- `SKILL.md` frontmatter: `name`, `description`. The description says when to use the skill,
  in the user's words, in one or two sentences.
- Workflows that must only run on request set `disable-model-invocation: true`.
- One job per skill. Put long reference material into `references/` next to `SKILL.md` and
  load it on demand.
- Agents keep the shared frontmatter (`name`, `description`) both Claude Code and Copilot read.
- Output follows `rules/markdown.md` and `rules/language.md`: sentence case, en dash with
  spaces, never em dash, fenced code with a language, English unless a rule says otherwise.

## Contract with PMOS

- `manifest.yaml` `requires_pmos` pins the PMOS versions this Playbook works with.
- `types.yaml`, `preset/pmos.yaml` and `manifest.yaml` validate against the schemas of that
  PMOS version: `pmos playbook validate .`
- Every `pmos` call in a skill, command or hook must match a command contract from
  `pmos help describe`. CI checks this.
- A change that needs something PMOS does not offer yet is a `contract` issue in both
  repos, linked. PMOS ships first; the Playbook follows.

## Build and test

- Install the pinned PMOS:
  `gh release download <tag> --repo brgn81/pm-os-footing --pattern "*.whl"`, then
  `uv tool install ./pmos-*.whl`
- `pmos playbook validate .` – schemas and CLI calls, before every commit
- `uv run scripts/lint.py` – markdown rules: em dash, casing, fence languages, BOM
- `pmos init --playbook . --workspace <scratch>` – install into a scratch workspace,
  then `pmos skills install --workspace <scratch>` and `pmos where` for every type in `types.yaml`
- Nightly the sandbox installs PMOS's latest release with this repo's `main`.

## Engineering defaults

- Small changes, one concern per PR. Conventional Commits: `type(scope): description`.
- Version: semver in `manifest.yaml`; patch for wording, minor for new skills or types,
  major for removals or renames. Every release gets a CHANGELOG entry.
- Vendored phuryn/pm-skills content keeps its attribution; note local changes in `NOTICE`.
- Record decisions that change the contract in `brgn81/pm-os` `docs/decisions.md`.
