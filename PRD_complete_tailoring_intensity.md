# PRD: Add "Complete" Tailoring Intensity Level

## 1. Background

The resume matcher application currently supports **4 tailoring intensity levels**, with **"ATS"** being the highest/most aggressive existing level. Tailoring is implemented via **LLM prompts** — one distinct prompt (or prompt template with parameterized instructions) per intensity level.

This PRD specifies the addition of a **5th, most aggressive intensity level: "Complete."**

## 2. Goal

Add a new tailoring intensity option, **"Complete,"** that maximizes ATS keyword match and JD alignment by rewriting nearly the entire resume content — going further than the current "ATS" level — while preserving only the factual, unchangeable elements of the candidate's identity and work history.

## 3. Functional Requirements

### 3.1 What "Complete" MUST preserve (do not alter)
- Full name
- Contact information (email, phone, location, LinkedIn/portfolio links)
- Company names worked at
- Job titles held
- Employment dates / tenure
- Education institution names, degrees, and dates
- Any certifications/licenses as factual records (name, issuer, date) — names not rewritten, though relevance/order may be adjusted

### 3.2 What "Complete" MUST rewrite/adapt
This is the core behavior of the "Complete" tier: **every bullet point in the resume is completely rewritten**, not lightly edited or keyword-sprinkled. The rewrite target is maximum ATS keyword density and exact JD-term matching, as aggressively as possible while staying truthful.

- **Summary/objective section** (if present) — fully rewritten from scratch to mirror the JD's exact role title, framing, and top keywords/phrases as densely as is coherently possible.
- **Work experience bullet points** — every single bullet under every role is fully rewritten (not just adjusted) so it incorporates JD keywords and phrasing as heavily as possible, while still accurately describing what the candidate actually did in that role. The rewrite should actively pull in exact terms, tools, and phrasing used in the JD wherever the candidate's real experience supports it.
- **Project bullet points** — same full-rewrite, maximum-keyword-density treatment as work bullets.
- **Skills section** — reordered and rewritten to prioritize exact keyword matches from the JD, using the JD's exact phrasing/casing where ATS-relevant (e.g., "Node.js" vs "NodeJS"), and adding any JD-relevant skill terms the candidate's resume supports but doesn't yet name explicitly.
- **Section ordering/emphasis** — may be adjusted to surface JD-relevant experience first, if the existing architecture supports section reordering (confirm against current capabilities).

**Keyword density directive:** Unlike lower intensity tiers (which likely balance readability and natural phrasing more heavily), "Complete" should explicitly prioritize keyword coverage and exact JD-term matching over stylistic smoothness. The prompt should instruct the LLM to scan the JD for its key skills, tools, responsibilities, and qualifications, and ensure each one that's truthfully supported by the candidate's background appears — ideally in the same wording as the JD — somewhere in the rewritten resume (summary, skills, or bullets).

### 3.3 Explicit boundary vs. current "ATS" level
Before implementation, Claude Code must:
1. Read the current "ATS" level's prompt in full.
2. Identify precisely what "ATS" already rewrites vs. preserves.
3. Ensure "Complete" is implemented as a strict superset of rewriting — i.e., anything "ATS" already modifies, "Complete" also modifies, plus the additional elements specified in 3.2 that "ATS" may currently leave untouched (if any).

**Open question for confirmation during implementation:** if "ATS" already rewrites all bullets and skills, the delta for "Complete" may be:
- More aggressive keyword density / exact-phrase matching against the JD
- Rewriting summary/objective (if ATS currently leaves it untouched)
- More willingness to reorder/restructure sections
- Stricter 1:1 keyword mirroring even at the cost of natural phrasing (acceptable tradeoff for this tier, since the tier is explicitly optimizing for ATS parsing over human readability)



This should be stated explicitly in the "Complete" prompt itself as a hard constraint, not just documented here.

## 4. Technical Implementation Requirements

1. **Locate existing intensity implementation**: Find where the 4 current intensity levels are defined (likely an enum/config + corresponding prompt templates or prompt-building functions).
2. **Add "Complete" as a 5th enum value / option**, following the exact naming and wiring convention already used for the other 4 (e.g., if levels are stored as strings like `"light"`, `"moderate"`, `"aggressive"`, `"ats"`, add `"complete"`).
3. **Create a new prompt template** for "Complete" that encodes the rules in Section 3.1–3.3.
4. **Wire it through the full pipeline**: UI/API selector for intensity level, backend prompt dispatch logic, and any validation/type definitions (e.g., TypeScript union types, backend enums, database constraints) must all be updated consistently.
5. **UI update**: Add "Complete" as a selectable option wherever the 4 existing intensities are shown to the user (dropdown, radio buttons, etc.), matching existing UI patterns.
6. **No regression**: The 4 existing levels must continue to function exactly as before.

## 5. Acceptance Criteria

- [ ] "Complete" appears as a 5th selectable tailoring intensity in the UI, alongside the existing 4.
- [ ] Selecting "Complete" and submitting a resume + JD produces output where: name, contact info, employer names, titles, dates, and education are unchanged from the input.
- [ ] Summary/objective (if present), all work experience bullets, and all project bullets are **completely rewritten** (not lightly edited) to maximize JD keyword density and exact-term matching.
- [ ] Skills section is reordered/rewritten to prioritize exact JD keyword matches, including any truthfully-supported JD skill terms not previously named explicitly.
- [ ] A sample side-by-side comparison (JD keyword list vs. final resume) shows the large majority of JD-stated required skills/tools/responsibilities are reflected somewhere in the rewritten resume, in matching or near-matching phrasing.
- [ ] Output contains no fabricated tools, employers, titles, or metrics.
- [ ] Existing 4 intensity levels produce unchanged output (no regression).
- [ ] Prompt for "Complete" is reviewed and confirmed against the actual current "ATS" prompt to ensure it's a true superset (per Section 3.3).

## 6. Out of Scope
- Changes to the resume parsing/extraction logic (assumed already functional)
- Changes to file export/formatting (PDF/DOCX generation) — assume "Complete" output flows through the same rendering pipeline as other levels
- A/B testing or analytics on tailoring effectiveness

## 7. Assumptions Made in This PRD (flag to user if incorrect)
- The 4 existing levels are ordered by increasing aggressiveness, with "ATS" as the current ceiling.
- Intensity levels are implemented as discrete named prompts/templates rather than a single parameterized numeric scale.
- The app has a single JD input flow (per the original description: "just feed the job description") with no multi-JD batching to account for.
- Section reordering may or may not already be supported — Claude Code should verify and note if it needs to be added as a smaller sub-feature.
