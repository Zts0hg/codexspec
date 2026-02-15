---
description: Generate a custom quality checklist for validating requirements completeness, clarity, and consistency
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
---

# Requirements Quality Checklist Generator

## Checklist Purpose: "Unit Tests for Requirements"

**CRITICAL CONCEPT**: Checklists are **UNIT TESTS FOR REQUIREMENTS WRITING** - they validate the quality, clarity, and completeness of requirements.

**NOT for verification/testing:**
- ❌ NOT "Verify the button clicks correctly"
- ❌ NOT "Test error handling works"
- ❌ NOT "Confirm the API returns 200"

**FOR requirements quality validation:**
- ✅ "Are visual hierarchy requirements defined for all card types?" (completeness)
- ✅ "Is 'prominent display' quantified with specific sizing/positioning?" (clarity)
- ✅ "Are hover state requirements consistent across all interactive elements?" (consistency)
- ✅ "Are accessibility requirements defined for keyboard navigation?" (coverage)

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Steps

### 1. Setup

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - Feature directory path
- `AVAILABLE_DOCS` - Available documents list

### 2. Clarify Intent

Generate up to THREE contextual clarifying questions based on:
- Feature domain keywords (auth, latency, UX, API)
- Risk indicators ("critical", "must", "compliance")
- Stakeholder hints ("QA", "review", "security team")

Question types:
- Scope refinement
- Risk prioritization
- Depth calibration
- Audience framing

### 3. Load Feature Context

Read from FEATURE_DIR:
- spec.md: Feature requirements and scope
- plan.md (if exists): Technical details
- tasks.md (if exists): Implementation tasks

### 4. Generate Checklist

Create `FEATURE_DIR/checklists/` directory if needed.
Generate unique checklist filename: `[domain].md` (e.g., `ux.md`, `api.md`, `security.md`)

**Category Structure - Group items by requirement quality dimensions:**
- **Requirement Completeness**: Are all necessary requirements present?
- **Requirement Clarity**: Are requirements specific and unambiguous?
- **Requirement Consistency**: Do requirements align without conflicts?
- **Acceptance Criteria Quality**: Are success criteria measurable?
- **Scenario Coverage**: Are all flows/cases addressed?
- **Edge Case Coverage**: Are boundary conditions defined?
- **Non-Functional Requirements**: Performance, Security, Accessibility specified?
- **Dependencies & Assumptions**: Are they documented?

### 5. Item Structure

Each item should follow this pattern:
```
- [ ] CHK### - Are [requirement type] defined for [scenario]? [Quality Dimension, Spec §X.Y]
```

**Examples by Quality Dimension:**

**Completeness:**
- "Are error handling requirements defined for all API failure modes? [Gap]"
- "Are accessibility requirements specified for all interactive elements?"

**Clarity:**
- "Is 'fast loading' quantified with specific timing thresholds? [Clarity, Spec §NFR-2]"
- "Are 'related items' selection criteria explicitly defined?"

**Consistency:**
- "Do navigation requirements align across all pages? [Consistency, Spec §FR-10]"
- "Are card component requirements consistent between pages?"

**Coverage:**
- "Are requirements defined for zero-state scenarios? [Coverage, Edge Case]"
- "Are concurrent user interaction scenarios addressed?"

### 6. Prohibited Patterns

**❌ WRONG (Testing implementation):**
- "Verify landing page displays 3 cards"
- "Test hover states work on desktop"
- "Confirm logo click navigates home"

**✅ CORRECT (Testing requirements quality):**
- "Are the number and layout of featured items explicitly specified? [Completeness]"
- "Are hover state requirements consistently defined for all interactive elements? [Consistency]"
- "Are navigation requirements clear for all clickable brand elements? [Clarity]"

### 7. Report

Output:
- Full path to created checklist
- Item count
- Focus areas selected
- Depth level

## Example Checklist Types

**UX Requirements Quality:** `ux.md`
- Visual hierarchy requirements
- Interaction state requirements
- Accessibility requirements
- Fallback behavior requirements

**API Requirements Quality:** `api.md`
- Error response formats
- Rate limiting requirements
- Authentication requirements
- Versioning strategy

**Performance Requirements Quality:** `performance.md`
- Performance metrics quantification
- Load condition specifications
- Degradation requirements

**Security Requirements Quality:** `security.md`
- Authentication requirements
- Data protection requirements
- Threat model alignment
- Breach response requirements

> [!NOTE]
> Each `/codexspec.checklist` run creates a NEW file in `checklists/` directory.
