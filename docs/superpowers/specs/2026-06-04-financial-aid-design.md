# Financial Aid Page — PyCon Ireland 2026

**Date:** 2026-06-04
**Status:** Approved

## Summary

Create a `/financial-aid/` page for PyCon Ireland 2026 using the existing `single` layout. The page informs visitors of the financial aid programme without actively inviting applications (to avoid budget overrun and disappointment). Status is "Coming Soon" — the Google Form is in preparation.

## Approach

Option A: Markdown page with `layout: single`. No new template needed. Consistent with `code-of-conduct/`.

- `content/financial-aid/_index.md` — all content
- Footer: add link in the Community column
- Tickets page: add a link to `/financial-aid/`

## Page Structure

### 1. Title + Coming Soon badge
- H1: "Financial Aid"
- Visible badge indicating applications are not yet open

### 2. What the aid covers
- Complimentary conference ticket
- Full or partial reimbursement of travel costs
- Full or partial reimbursement of accommodation costs
- Maximum award: **€350 per person**

### 3. Eligibility and priorities
Priority order (economic, budgetary, and environmental reasons):
1. Residents of Ireland
2. Residents of the United Kingdom
3. Residents of Europe

### 4. How to apply
- Application form: Google Form (link to be added when available)
- Application deadline: TBD
- Form is not yet open

### 5. Decision process
- Applications reviewed by a committee chaired by at least one director
- Awards may be fully approved, partially approved, or denied
- Decisions are not motivated and cannot be appealed

### 6. Attribution rules
- Successful applicants are notified by email
- **1 week to accept or decline** the aid
- If no response within 1 week: aid is cancelled and redistributed to the next eligible applicant, with explicit notification sent to the original recipient

### 7. Reimbursement conditions
Applicants approved for travel or accommodation reimbursement must:
- Attend the conference and register at the desk
- Submit receipts for approved expenses
- Provide full legal name and address matching banking information
- Supply complete IBAN details
- Email all documentation to the organisation within **30 days** post-event

Incomplete submissions will not be followed up.

### 8. No-show policy
Applicants who receive aid and cannot attend must:
- Notify organisers **at least 7 days before** the event, OR
- Provide documented justification **within 30 days** after the event

Failure to comply results in ineligibility for future financial aid at Python Ireland events, unless circumstances demonstrate absolute necessity.

## Navigation

- **Footer:** add link in the "Community" column (alongside Code of Conduct, Terms & Conditions, etc.)
- **Tickets page:** add a short paragraph or link pointing to `/financial-aid/`
- **Main nav:** not included

## Files to Create / Modify

| File | Action |
|------|--------|
| `content/financial-aid/_index.md` | Create |
| `layouts/partials/footer.html` | Add link in Community column |
| `layouts/partials/tickets.html` | Add link to financial aid page (note: tickets section is currently commented out on homepage — link to be activated when tickets section goes live) |

## Out of Scope

- Google Form integration (to be added later)
- Dedicated custom layout/template
- Data-driven content model
