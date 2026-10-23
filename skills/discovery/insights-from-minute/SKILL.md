---
name: insights-from-minute
description: "Propose short, catchy insight statements from a meeting minute (full transcript or a plain collection of notes) and insert the ones the user picks directly into the minute, marked with a '💡 ' prefix so they can be extracted into insight items later. Use when processing interview or discovery minutes, generating candidate insights from meeting notes, or asked to find/add insights to meeting notes."
---

# Insights from minute

Turn a meeting minute – whether it is a full transcript or just a collection of notes – into a short list of catchy insight candidates, let the user pick which ones matter, then insert each selected insight directly into the minute at the spot where it was discussed.

## When to use

- The user asks for "insights" from a minute, meeting, or set of meeting notes.
- The user asks to "add insights to the minutes" (or a specific minute file).
- Preparing a minute so that its `💡 ` lines can be extracted into items of the type `insight`.

A minute is not necessarily a verbatim transcript – it may just as well be a short list of bullet-point notes. The rules below apply the same way regardless of the minute's shape.

## Downstream contract

Any line starting with `💡 ` (emoji, then one space) is an insight to extract into an `insight` item. Every insight statement this skill inserts MUST start with `💡 ` at the very beginning of its own line – never mid-sentence, never without the trailing space. An extractor can only pick up an insight line when it is the last line of its paragraph – never insert an insight line and then continue the same paragraph with more transcript text below it.

## Sentence-level vs. section-level

An insight is **sentence-level** if it is triggered by a single statement, quote, or bullet. It is **section-level** if it synthesizes two or more exchanges or notes that span a paragraph or more. Classify each candidate against this definition in Step 2, and use that same classification to decide placement in Step 4.

## Workflow

### Step 1 – Load the minute

- Resolve the target minute file: an explicit path, an item id in the folder of `pmos where --pmos-type minute --json`, or the file currently open in the editor. A type that is not mapped returns nothing: say so, do not guess a path.
- If the folder is synced read-only (`writable` is false in `pmos types --json`), do not edit the minute. Offer the candidates in chat only, and say where the user can add them upstream (`url` in the minute's frontmatter).
- If it's ambiguous which minute to use, ask.
- Read the full minute content before drafting anything – it may be a verbatim transcript, a short set of bullet-point notes, or something in between; treat whatever structure is there as the source of truth.

### Step 2 – Propose insights (present only, do not insert yet)

- Scan the minute for passages that carry a real insight: a risk, a surprising fact, a decision, a constraint, a validated/invalidated assumption, or a strong stated opinion.
- If no qualifying passages are found, inform the user: "No insight candidates were identified in this minute – it appears to contain only logistical or procedural content." Do not fabricate candidates.
- Draft each as a short, catchy, self-contained statement (see formatting rules below).
- Present the full list to the user as numbered candidates, each showing:
  1. The draft statement
  2. The exact source-file line number(s) it ties to (e.g. `line 42` or `lines 118-124`, from the file as currently read) – this is the primary reference, since it is what you'll use to locate the spot again in Step 4 and what lets the user jump straight to it.
  3. Whether it is sentence-level or section-level (see "Sentence-level vs. section-level" above)
- Do not write anything into the file at this step.

### Step 3 – User selects

- Ask which candidates to add: by number, "all", or "none".
- Invite wording edits directly by proposing the reply format `[number], [title]` (e.g. `2, Bug in Prototype: ...`) so the user can supply an adjusted title inline while selecting.
- Accept wording edits from the user before insertion.

### Step 4 – Insert at the respective location

Decide placement per selected insight:

- **Sentence/statement-level** – the insight ties to one specific line, whether spoken by one person or written as one note entry. Insert it as the last line of that same paragraph, as a new line via `<br>` after all of that paragraph's existing text – never mid-paragraph, since an extractor only recognizes an insight line that sits at the very end of its paragraph.

  **Example:**

  > PM: Start with the biggest problem.
  >
  > -> Clearly the language. Acme Planner is German only. We have colleagues in Poland and the Netherlands who need English as an option. For us that is not a nice-to-have but a blocker for rolling out to the other sites.<br>
  >💡 English language option is missing (Example Corp)

- **Section/paragraph-level** – the insight summarizes a whole exchange rather than one line. Insert as its own new paragraph immediately below the relevant block of dialogue, separated by a blank line above and below.

  **Example:**

  > PM: Let's go through it systematically. What else do you notice?
  >
  > -> A few things, let me sort them:
  >
  > * Language switch is missing completely (see above)
  > * The overview loads too slowly (about 4-5 seconds)
  > * The export button is hard to find, hidden in the three-dot menu
  > * Filters are not kept after a reload
  > * The mobile view is practically unusable on a tablet
  > * Contrast of the status badges is partly too weak
  > * No way to show or hide table columns
  > * Search only reacts after 3+ letters, which is annoying for article numbers

  > 💡 Usability and accessibility fall short (Example Corp)

Formatting rules for every insight statement (apply regardless of placement):

- Starts with `💡 ` at the beginning of the line.
- Written in the same language as the minute itself – never translate it. This is a deliberate override of any workspace-wide "respond in English" instruction: an insight line is a verbatim artifact inserted into the minute's own content, not a conversational reply to the user, so it stays in the minute's language even while your chat replies to the user stay in English.
- One short line: a catchy title-style phrase rather than a full descriptive sentence, roughly 3-8 words. Drop hedging, subordinate clauses, and any meta-commentary about the meeting itself.
- Name the expert (speaker) or the company the insight is about or comes from, in parentheses at the end of the line, as every example in this skill does. Omit it only when the minute has a single participant and the attribution would therefore carry no information.

  **Example:**

  > -> Right now 14 people at the two sites would start using the tool as soon as English is available. That is more than double our current user count.<br>
  > 💡 14 users ready once English is available (Example Corp)

Apply all selected insertions to the file in one editing pass rather than re-reading and rewriting it per insight, and give each edit enough surrounding context to match exactly one location.

### Step 5 – Report and next step

- Confirm which insights were added and where (paragraph/speaker reference), in a short list.
- Remind the user that the minute was only changed locally – pushing it (`/push`, when the minute type can push) is a separate, manual step.
