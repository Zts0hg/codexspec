# Security and trust boundaries

## Purpose

Review security and trust boundaries using current affected behavior and contracts.

## Applicability

Protected operations, untrusted inputs, credentials, sensitive data or external side effects are affected.

## Non-Applicability and False Positives

Do not activate detail for hypothetical inputs or absent future requirements. Existing type, validation, state/order, ownership and framework guarantees may satisfy a checkpoint. A candidate cue alone is not a defect or maintenance benefit. Use common.md for admission and contrary-evidence rules.

## Necessary Evidence

For applicable checkpoints identify the input/state source, affected path, actual contract or present maintenance benefit, and existing guarantees. Defects require reachability, impact and change attribution; maintenance requires current benefit and compatibility.

## Completion

Record checked paths and key evidence, resolve material necessary gaps, and stop when applicable questions are answered. New traced boundaries may expand selection within the affected scope.

## Checkpoints

### SEC-01

Trace untrusted data into SQL syntax; check parameters or equivalent verified query safety at the actual boundary.

### SEC-02

Trace input into process execution; distinguish direct arguments, option injection and shell interpretation before admitting injection.

### SEC-03

Check filesystem containment and path identity against reachable external input and actual allowed roots.

### SEC-04

Check real secrets embedded in selected code/config; distinguish public identifiers, placeholders and safe test fixtures.

### SEC-05

Check sensitive exposure against actual consumers and policy. Public diagnostics can be actionable without disclosing secrets or forbidden internals.

### SEC-06

Check credential storage according to its purpose: suitable password hashing for verification; confidentiality/integrity and key handling for recoverable tokens or keys.

### SEC-07

Check deserialization features and reachable untrusted data; ordinary safe data parsing is not executable deserialization.

### SEC-08

Check untrusted data reaching HTML/script contexts and the renderer's actual escaping/sanitization guarantees.

### SEC-09

Check server-side network destinations against the actual trust policy, redirects and resolved targets when relevant.

### SEC-10

Check required authentication on protected operations, including omitted implementations; public endpoints are not automatically protected.

### SEC-11

Trace identity source → authentication execution → authorization result consumption → protected subject/resource/action → propagation → denial behavior.

### SEC-12

Check identity field names and origins agree across headers, contexts, claims, tenant/user data and consumers.

### SEC-13

Verify required authentication/permission checks execute on the actual path rather than merely constructing check objects.

### SEC-14

Verify check results, errors and status values are consumed and influence authorization.

### SEC-15

Verify denial prevents protected success behavior and side effects as the operation requires.

### SEC-16

Check permissions for the actual subject, action and resource; existence or token presence alone is insufficient when policy requires more.

### SEC-17

Trace trusted middleware identity through downstream layers; prevent untrusted request fields replacing it and propagate only as required.

### SEC-18

Review login/reset/refresh/session exchange chains when affected, including required credential and lifecycle checks.

### SEC-19

Check resource authorization under the actual ownership, role, sharing or delegated policy; locating a resource by ID is not permission.

### SEC-20

Check linked resources in cross-resource operations against the applicable policy, not an invented universal ownership rule.

### SEC-21

Check upload content, parser and serving behavior against actual threats/allowed types; extension and declared type alone may be insufficient, and magic bytes alone are not complete validation.
