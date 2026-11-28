# Financial Aid Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a `/financial-aid/` page for PyCon Ireland 2026 with "Coming Soon" status, add it to the footer, and add a link in the tickets partial.

**Architecture:** Markdown page using the existing `single` layout (same pattern as `code-of-conduct/`). No new template needed. Three files touched: one created, two modified.

**Tech Stack:** Hugo static site, Tailwind CSS v4, Markdown with inline HTML for the badge.

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `content/financial-aid/_index.md` | Create | Page content with frontmatter |
| `layouts/partials/footer.html` | Modify | Add Financial Aid link in Community column |
| `layouts/partials/tickets.html` | Modify | Add note linking to financial aid page |

---

### Task 1: Create the financial aid content page

**Files:**
- Create: `content/financial-aid/_index.md`

- [ ] **Step 1: Create the file**

```markdown
---
title: "Financial Aid"
description: "Financial assistance is available for eligible attendees of PyCon Ireland 2026."
layout: "single"
---

<div class="mb-8 text-center">
  <span class="inline-block bg-py-yellow/10 text-py-yellow text-sm font-semibold px-4 py-2 rounded-full uppercase tracking-wider">Applications opening soon</span>
</div>

Python Ireland offers financial assistance to help members of the community attend PyCon Ireland 2026 who would otherwise be unable to do so.

## What the Aid Covers

Financial assistance may include:

- A complimentary conference ticket
- Full or partial reimbursement of travel expenses
- Full or partial reimbursement of accommodation costs

The maximum award is **€350 per person**.

## Eligibility and Priorities

Due to economic, budgetary, and environmental considerations, applications are evaluated in the following order of priority:

1. Residents of Ireland
2. Residents of the United Kingdom
3. Residents of Europe

## How to Apply

The application form will be available shortly. The application deadline is to be announced.

## Decision Process

Applications are reviewed by a committee chaired by at least one director of Python Ireland. Awards may be fully approved, partially approved, or denied. Decisions are not motivated and cannot be appealed.

## Attribution and Acceptance

Successful applicants are notified by email and have **one week** to accept or decline the award. If no response is received within that period, the aid is cancelled and redistributed to the next eligible applicant. The original recipient will be notified of the cancellation.

## Reimbursement Conditions

Applicants approved for travel or accommodation reimbursement must:

- Attend the conference and register at the desk
- Submit receipts for approved expenses
- Provide their full legal name and address, matching their banking information
- Supply complete IBAN details
- Email all documentation to Python Ireland within **30 days** of the event

Incomplete submissions will not receive follow-up reminders.

## No-Show Policy

Recipients who are unable to attend must notify the organisers **at least 7 days before** the event, or provide documented justification **within 30 days** after the event. Failure to comply results in ineligibility for financial aid at future Python Ireland events, unless circumstances demonstrate absolute necessity.

---

For questions, contact [contact@python.ie](mailto:contact@python.ie).
```

- [ ] **Step 2: Verify the page builds**

Run: `hugo --minify 2>&1 | tail -5`
Expected: `Total in X ms` with no errors. Check: `grep -r "financial-aid" public/sitemap.xml`

- [ ] **Step 3: Commit**

```bash
git add content/financial-aid/_index.md
git commit -m "feat(financial-aid): add financial aid page with coming soon status"
```

---

### Task 2: Add Financial Aid link in footer

**Files:**
- Modify: `layouts/partials/footer.html`

- [ ] **Step 1: Add the link in the Community column**

In `layouts/partials/footer.html`, locate the Community `<ul>` block (around line 32). Add after the `Blog` entry and before `Code of Conduct`:

```html
<li><a href="/financial-aid/" class="text-text-secondary hover:text-py-yellow transition-colors">Financial Aid</a></li>
```

The Community column should look like:

```html
<div>
  <h4 class="text-text-heading font-semibold text-sm uppercase tracking-wider mb-4">Community</h4>
  <ul class="space-y-2 text-sm">
    <li><a href="/blog/" class="text-text-secondary hover:text-py-yellow transition-colors">Blog</a></li>
    <li><a href="/financial-aid/" class="text-text-secondary hover:text-py-yellow transition-colors">Financial Aid</a></li>
    <li><a href="/code-of-conduct/" class="text-text-secondary hover:text-py-yellow transition-colors">Code of Conduct</a></li>
    <li><a href="/terms-and-conditions/" class="text-text-secondary hover:text-py-yellow transition-colors">Terms &amp; Conditions</a></li>
    <li><a href="/credits/" class="text-text-secondary hover:text-py-yellow transition-colors">Photo Credits</a></li>
    <li><a href="https://python.ie" class="text-text-secondary hover:text-py-yellow transition-colors" target="_blank" rel="noopener">Python Ireland</a></li>
  </ul>
</div>
```

- [ ] **Step 2: Verify the footer renders**

Run: `hugo --minify 2>&1 | tail -3`
Then: `grep -c "financial-aid" public/index.html`
Expected: at least `1` (footer link present on homepage).

- [ ] **Step 3: Commit**

```bash
git add layouts/partials/footer.html
git commit -m "feat(financial-aid): add Financial Aid link in footer Community column"
```

---

### Task 3: Add financial aid note in tickets partial

**Files:**
- Modify: `layouts/partials/tickets.html`

- [ ] **Step 1: Add note below the ticket grid**

In `layouts/partials/tickets.html`, add a note after the closing `</div>` of the grid (after line 39, before `</section>`):

```html
    <p class="text-center text-sm text-text-secondary mt-8">
      Need help covering costs?
      <a href="/financial-aid/" class="text-py-blue-light hover:text-py-yellow transition-colors">Financial aid is available</a>
      for eligible attendees.
    </p>
```

The bottom of the section should look like:

```html
    </div>

    <p class="text-center text-sm text-text-secondary mt-8">
      Need help covering costs?
      <a href="/financial-aid/" class="text-py-blue-light hover:text-py-yellow transition-colors">Financial aid is available</a>
      for eligible attendees.
    </p>
  </div>
</section>
```

- [ ] **Step 2: Verify the build**

Run: `hugo --minify 2>&1 | tail -3`
Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add layouts/partials/tickets.html
git commit -m "feat(financial-aid): add financial aid link in tickets section"
```

---

### Task 4: Final verification and PR

- [ ] **Step 1: Full build check**

Run: `hugo --minify 2>&1 | tail -5`
Expected: `Total in X ms`, 0 errors, 0 warnings.

- [ ] **Step 2: Check the financial aid page was generated**

Run: `ls public/financial-aid/`
Expected: `index.html` present.

- [ ] **Step 3: Spot-check the HTML output**

Run: `grep -A3 "Applications opening soon" public/financial-aid/index.html`
Expected: the badge span is present.

Run: `grep "financial-aid" public/financial-aid/index.html | wc -l`
Expected: 0 (no self-referential links needed).

- [ ] **Step 4: Push and open PR**

```bash
git push origin HEAD
gh pr create \
  --title "feat(financial-aid): add financial aid page for PyCon Ireland 2026" \
  --body "$(cat <<'EOF'
## Summary

- Add `/financial-aid/` page with coming soon status (Google Form in preparation)
- Max award €350, priority: Ireland > UK > Europe
- Covers: complimentary ticket, travel, accommodation reimbursement
- Includes attribution rules (1-week acceptance window), reimbursement conditions, no-show policy
- Add link in footer Community column
- Add link in tickets partial

## Test plan

- [ ] Hugo build succeeds with no errors
- [ ] `/financial-aid/` page renders at correct URL
- [ ] "Applications opening soon" badge visible
- [ ] Footer Community column shows Financial Aid link
- [ ] Tickets partial shows financial aid note
EOF
)"
```
