"use strict";
/* Distill review workspace controller.
   Dynamic visual state is carried by class names, attributes and native element state
   only: the content-security policy admits no style attribute, and the three front-end
   assets are asserted to contain no absolute URL scheme, which rules out vector graphics. */
const fragment = new URLSearchParams(location.hash.slice(1));
const token = fragment.get("token") || "";
history.replaceState(null, "", location.pathname);
let state = null;
let selected = null;
let messages = {};
let conflictRecords = [];
/* What this page previewed, per item: the digest the backend returned and the exact
   operation it was taken for. The backend reports which digests it still holds, so a
   gate can never read as satisfied for a revision the backend would refuse. */
const previews = {};
const FIELD_SIZING = typeof CSS !== "undefined" && typeof CSS.supports === "function"
  && CSS.supports("field-sizing", "content");
const MARKS = {candidate: "◆", vetted: "✓", removed: "✕", deferred: "◦", cluster: "⬢"};

function t(key, fallback) { return messages[key] || fallback; }

function format(key, fallback, values) {
  return String(t(key, fallback)).replace(/\{(\w+)\}/g, (whole, name) =>
    Object.hasOwn(values, name) ? String(values[name]) : whole);
}

function fieldLabel(key) {
  const labels = messages.fieldLabels || {};
  return labels[key] || key;
}

async function api(path, options = {}) {
  const headers = {Authorization: `Bearer ${token}`, ...(options.headers || {})};
  if (options.body) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify({schema_version: 1, ...JSON.parse(options.body)});
  }
  const response = await fetch(path, {...options, headers});
  const value = await response.json();
  if (!response.ok) {
    const error = new Error(value.error || `Request failed (${response.status})`);
    error.details = value;
    throw error;
  }
  return value;
}

/* ---------- status and feedback ---------- */

function setStatus(message, error = false) {
  const node = document.querySelector("#status");
  node.textContent = message;
  node.className = error ? "error" : "";
}

function formatError(error) {
  const details = error && error.details ? error.details : {};
  const raw = String((details && details.error) || (error && error.message) || error);
  const separator = raw.indexOf(":");
  const code = separator === -1 ? raw : raw.slice(0, separator);
  const detail = separator === -1 ? "" : raw.slice(separator + 1).trim();
  const localized = t(`error.${code}`, t("error.validation", "Review validation failed."));
  const lines = [localized, `${t("error.code", "Rule")}: ${code}`];
  if (detail) lines.push(`${t("error.detail", "Detail")}: ${detail}`);
  if (Array.isArray(details.records) && details.records.length) {
    lines.push(`${t("error.records", "Records")}: ${details.records.join(", ")}`);
  }
  if (Array.isArray(details.failures) && details.failures.length) {
    lines.push(`${t("error.failures", "Failures")}: ${details.failures.join("; ")}`);
  }
  return lines.join("\n");
}

function setErrorStatus(error) {
  setStatus(formatError(error), true);
}

/* Feedback for a decision control belongs next to that control, not only in the
   page-level status region. */
function setFeedback(message, error = false) {
  const node = document.querySelector("#feedback");
  if (!node) {
    setStatus(message, error);
    return;
  }
  node.textContent = message;
  node.className = error ? "feedback error" : "feedback";
  node.hidden = !message;
}

/* ---------- field controls ---------- */

function fieldId(prefix, key) {
  return `${prefix}-${String(key).replace(/[^A-Za-z0-9_-]/g, "-")}`;
}

function autoGrow(field) {
  if (FIELD_SIZING) return;
  field.rows = 1;
  let rows = 1;
  while (field.scrollHeight > field.clientHeight && rows < 16) {
    rows += 1;
    field.rows = rows;
  }
}

/* The record codec rejects any field value containing a line break, so a line break
   can neither be typed nor survive a paste. */
function singleLineOnly(field) {
  field.addEventListener("beforeinput", event => {
    if (event.inputType === "insertLineBreak" || event.inputType === "insertParagraph") event.preventDefault();
  });
  field.addEventListener("input", () => {
    if (/[\r\n]/.test(field.value)) field.value = field.value.replace(/[\r\n]+/g, " ");
    autoGrow(field);
  });
}

function makeField(name, value) {
  const input = document.createElement("textarea");
  input.name = name;
  input.rows = 1;
  input.value = value === undefined || value === null ? "" : String(value);
  singleLineOnly(input);
  return input;
}

function appendField(form, labelText, input, prefix) {
  const id = fieldId(prefix, input.name);
  const label = document.createElement("label");
  label.htmlFor = id;
  label.append(document.createTextNode(labelText));
  input.id = id;
  const error = document.createElement("span");
  error.id = `${id}-error`;
  error.className = "field-error";
  error.hidden = true;
  input.dataset.errorId = error.id;
  label.append(input, error);
  form.append(label);
}

function clearFormErrors(form) {
  for (const input of form.elements) {
    if (!input.dataset || !input.dataset.errorId) continue;
    input.removeAttribute("aria-invalid");
    input.removeAttribute("aria-describedby");
    const error = document.getElementById(input.dataset.errorId);
    if (error) error.hidden = true;
  }
}

function reportFormError(form, error) {
  clearFormErrors(form);
  const message = String(error.message || error);
  let key = null;
  if (message.startsWith("verification_required")) key = "verification";
  else if (message.startsWith("invalid_title")) key = "title";
  else {
    const match = message.match(/^(?:multiline_field|missing_consolidation_field):\s*(.+)$/);
    if (match) key = match[1];
  }
  const input = key ? Array.from(form.elements).find(item => item.name === key) : null;
  if (input && input.dataset.errorId) {
    const errorNode = document.getElementById(input.dataset.errorId);
    input.setAttribute("aria-invalid", "true");
    input.setAttribute("aria-describedby", input.dataset.errorId);
    errorNode.textContent = t("fieldError", "Check this field and try again.");
    errorNode.hidden = false;
    input.focus();
  }
  setFeedback(formatError(error), true);
}

/* ---------- preview gate ---------- */

function gateState(operation) {
  const record = previews[selected];
  if (!record || !state.gate_tokens.includes(record.token)) return "none";
  return record.operation === JSON.stringify(operation) ? "fresh" : "stale";
}

function previewMatches(form, operation) {
  return gateState(operation) === "fresh";
}

/* Each gated control submits its own operation, and the backend keys the gate on that
   exact operation. Deriving the indicator from one hard-coded variant made it claim
   "preview matches" for a control the backend would still refuse, so every gated control
   carries its own builder and is marked ready or not on its own terms. */
const gatedOperations = new WeakMap();

function markGated(button, build) {
  button.dataset.gated = "true";
  gatedOperations.set(button, build);
}

function renderGate(form) {
  const panel = form.querySelector(".final");
  const gate = form.querySelector(".gate");
  const primary = form.querySelector(".preview-action");
  if (!panel || !gate || !primary) return;
  const previewed = previews[selected];
  const live = Boolean(previewed && state.gate_tokens.includes(previewed.token));
  let ready = false;
  for (const button of form.querySelectorAll("[data-gated]")) {
    const build = gatedOperations.get(button);
    const matches = Boolean(build) && gateState(build()) === "fresh";
    button.dataset.ready = String(matches);
    if (matches) ready = true;
  }
  const value = ready ? "fresh" : (live ? "stale" : "none");
  panel.className = `final gate-${value}`;
  gate.textContent = value === "fresh"
    ? t("gate.fresh", "Preview matches the current edits")
    : value === "stale" ? t("gate.stale", "Edits changed after the preview") : t("gate.none", "Not previewed");
  primary.className = value === "fresh" ? "preview-action" : "preview-action btn-primary";
}

/* Re-derive the gate for whatever surface is open. A mutation clears the backend's
   previewed-operation set, so the indicator goes stale the moment a decision is staged. */
function refreshGate() {
  const form = document.querySelector("#editor form");
  if (form) renderGate(form);
}

/* ---------- decision state ---------- */

function recordState(id) {
  if (state.draft.deferred.includes(id)) return "deferred";
  const decision = state.draft.decisions[id];
  if (decision) {
    if (decision.action === "remove") return "removed";
    return decision.status === "vetted" ? "vetted" : "candidate";
  }
  for (const entry of Object.values(state.draft.decisions)) {
    if (entry.action === "merge" && entry.members.includes(id)) return "removed";
  }
  return null;
}

function clusterState(cluster) {
  const decision = state.draft.decisions[`cluster:${cluster}`];
  if (decision) return decision.status === "vetted" ? "vetted" : "candidate";
  const members = state.clusters[cluster] || [];
  if (members.length && members.every(member => state.draft.deferred.includes(member))) return "deferred";
  /* The queue lists members individually, so deciding each one is how a cluster is
     resolved without a merge. That outcome is terminal: the cluster owes no decision
     of its own, or the remaining-work set could never empty. */
  if (members.length && members.every(member => state.draft.decisions[member] || state.draft.deferred.includes(member))) {
    return "separate";
  }
  return null;
}

function candidateRecords() {
  return state.records.filter(record => record.status === "candidate");
}

function undecidedKeys() {
  const keys = candidateRecords().filter(record => recordState(record.id) === null).map(record => record.id);
  for (const cluster of Object.keys(state.clusters).sort()) {
    if (clusterState(cluster) === null) keys.push(`cluster:${cluster}`);
  }
  return keys;
}

/* ---------- header, queue and ledger ---------- */

function renderHeader() {
  document.querySelector("#project").textContent = state.project_name || "";
  const total = state.records.length;
  const decided = total - (state.summary.undecided || []).length;
  const bar = document.querySelector("#progress");
  bar.max = total;
  bar.value = decided;
  document.querySelector("#progress-text").textContent =
    format("progress", "{done} of {total} decided", {done: decided, total});
}

function queueEntry(key, mark, stateName, label, meta) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "queue-entry";
  if (key === selected) button.setAttribute("aria-current", "true");
  const glyph = document.createElement("span");
  glyph.className = `mark state-${stateName}`;
  glyph.textContent = mark;
  glyph.setAttribute("aria-hidden", "true");
  const title = document.createElement("span");
  title.className = "label";
  title.textContent = label;
  const detail = document.createElement("span");
  detail.className = "meta";
  detail.textContent = meta;
  button.append(glyph, title, detail);
  button.addEventListener("click", () => select(key));
  return button;
}

function queueGroup(parent, heading, entries) {
  if (!entries.length) return;
  const group = document.createElement("div");
  group.className = "queue-group";
  const title = document.createElement("h3");
  const name = document.createElement("span");
  name.textContent = heading;
  const count = document.createElement("span");
  count.textContent = String(entries.length);
  title.append(name, count);
  group.append(title, ...entries);
  parent.append(group);
}

function renderNavigation() {
  const nav = document.querySelector("#records");
  nav.replaceChildren();
  const pending = [];
  const staged = [];
  const deferred = [];
  for (const record of candidateRecords()) {
    const current = recordState(record.id);
    const meta = `${record.category} · ${record.id}`;
    const entry = queueEntry(record.id, MARKS[current || "candidate"], current || "candidate", record.title, meta);
    if (current === null) pending.push(entry);
    else if (current === "deferred") deferred.push(entry);
    else staged.push(entry);
  }
  const clusters = Object.keys(state.clusters).map(cluster => {
    const current = clusterState(cluster);
    const members = (state.clusters[cluster] || []).length;
    return queueEntry(`cluster:${cluster}`, MARKS.cluster, current || "candidate", cluster,
      `${t("members", "Cluster members")}: ${members}`);
  });
  queueGroup(nav, t("queue.pending", "Awaiting review"), pending);
  queueGroup(nav, t("queue.staged", "Staged"), staged);
  queueGroup(nav, t("queue.deferred", "Deferred"), deferred);
  queueGroup(nav, t("queue.clusters", "Clusters"), clusters);
  if (!nav.childElementCount) {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = t("queue.empty", "Nothing is awaiting review.");
    nav.append(empty);
  }
}

function ledgerTarget(key, group) {
  if (group === "added") {
    /* A record a merge will create does not exist yet; it resolves to the cluster that
       declares it. */
    for (const decision of Object.values(state.draft.decisions)) {
      if (decision.action === "merge" && decision.record_id === key) return `cluster:${decision.cluster}`;
    }
    return null;
  }
  const record = state.records.find(item => item.id === key);
  if (!record) return null;
  if (record.status === "candidate") return key;
  /* In scope only as a cluster member: the working surface for it is its cluster. */
  return record.cluster ? `cluster:${record.cluster}` : null;
}

function renderSummary() {
  const panel = document.querySelector("#summary");
  panel.replaceChildren();
  for (const group of ["added", "replaced", "promoted", "removed", "merged", "deferred", "undecided"]) {
    const entries = (state.summary && state.summary[group]) || [];
    if (!entries.length && group !== "undecided") continue;
    const block = document.createElement("div");
    block.className = "ledger-group";
    const heading = document.createElement("h3");
    const name = document.createElement("span");
    name.textContent = t(`summary.${group}`, group);
    const count = document.createElement("span");
    count.textContent = String(entries.length);
    heading.append(name, count);
    block.append(heading);
    if (entries.length) {
      const chips = document.createElement("div");
      chips.className = "chips";
      for (const key of entries) {
        const target = group === "merged" ? `cluster:${key}` : ledgerTarget(key, group);
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "chip";
        chip.textContent = key;
        chip.disabled = target === null;
        if (target !== null) chip.addEventListener("click", () => select(target));
        chips.append(chip);
      }
      block.append(chips);
    }
    panel.append(block);
  }
}

/* ---------- working surface ---------- */

function renderRecordContext(parent, record) {
  const details = document.createElement("dl");
  details.className = "record-meta";
  const values = {
    id: record.id,
    category: record.category,
    path: record.path,
    status: record.status,
    provenance: record.fields.provenance
  };
  for (const [key, value] of Object.entries(values)) {
    const term = document.createElement("dt");
    term.textContent = t(`field.${key}`, key);
    const description = document.createElement("dd");
    if (key === "id" || key === "path") description.className = "mono";
    description.textContent = value;
    details.append(term, description);
  }
  parent.append(details);
}

function editableEntries(record) {
  return record.editable_fields.map(key => [key, key === "title" ? record.title : record.fields[key]]);
}

function finalPanel(markdown) {
  const panel = document.createElement("div");
  panel.className = "final gate-none";
  const head = document.createElement("div");
  head.className = "final-head";
  const title = document.createElement("h3");
  title.textContent = t("finalText", "Final file content");
  const gate = document.createElement("span");
  gate.className = "gate";
  const preview = document.createElement("button");
  preview.type = "button";
  preview.className = "preview-action btn-primary";
  preview.textContent = t("previewFinal", "Preview final content");
  head.append(title, gate, preview);
  const body = document.createElement("pre");
  body.textContent = markdown;
  panel.append(head, body);
  return {panel, preview, body};
}

function actionBar(form, verificationNode) {
  const actions = document.createElement("div");
  actions.className = "actions";
  const routine = document.createElement("div");
  routine.className = "routine";
  const destructive = document.createElement("div");
  destructive.className = "destructive";
  const feedback = document.createElement("p");
  feedback.id = "feedback";
  feedback.className = "feedback";
  feedback.hidden = true;
  actions.append(routine, destructive, verificationNode, feedback);
  form.append(actions);
  return {routine, destructive};
}

/* `key` is the keyboard letter this control answers to; dispatch reads the attribute
   rather than a position, so the same letter never means a different action on
   another surface. */
function addAction(parent, label, className, handler, key) {
  const button = document.createElement("button");
  button.type = "button";
  if (className) button.className = className;
  button.textContent = label;
  if (key) button.dataset.key = key;
  button.addEventListener("click", handler);
  parent.append(button);
  return button;
}

function verificationHint(satisfied) {
  const node = document.createElement("p");
  node.className = satisfied ? "verification" : "verification required";
  node.textContent = satisfied
    ? t("verification.satisfied", "Stored evidence already establishes verification.")
    : t("verification.required", "Vetting requires verification evidence.");
  return node;
}

function renderEditor() {
  const editor = document.querySelector("#editor");
  editor.replaceChildren();
  /* A null selection means the queue has nothing undecided left: the stored record
     status stays `candidate` while a decision is only staged, so completion is read
     from the draft rather than from the record set. */
  if (selected === null) {
    renderAllDecided(editor);
    return;
  }
  if (selected.startsWith("cluster:")) {
    renderConsolidation(selected.slice(8), editor);
    return;
  }
  let record = candidateRecords().find(item => item.id === selected);
  if (!record) {
    /* The selection no longer resolves — a refresh dropped it, or it named a record that
       is in scope only as a cluster member. Fall back to remaining work rather than to
       the completion state, which would claim the queue is finished when it is not. */
    const remaining = undecidedKeys();
    selected = remaining.length ? remaining[0] : null;
    if (selected === null) {
      renderAllDecided(editor);
      return;
    }
    if (selected.startsWith("cluster:")) {
      renderConsolidation(selected.slice(8), editor);
      return;
    }
    record = candidateRecords().find(item => item.id === selected);
    if (!record) {
      renderAllDecided(editor);
      return;
    }
  }
  const form = document.createElement("form");
  const head = document.createElement("div");
  head.className = "surface-head";
  const title = document.createElement("h2");
  title.textContent = record.title;
  head.append(title);
  renderRecordContext(head, record);
  const body = document.createElement("div");
  body.className = "surface-body";
  const suggested = (state.proposals[record.id] || {}).fields || {};
  const staged = state.draft.decisions[record.id] || {};
  const stagedFields = staged.fields || {};
  for (const [key, value] of editableEntries(record)) {
    const input = makeField(key, Object.hasOwn(stagedFields, key)
      ? stagedFields[key]
      : (Object.hasOwn(suggested, key) ? suggested[key] : value));
    appendField(body, fieldLabel(key), input, `record-${record.id}`);
  }
  const verifyInput = makeField("verification", staged.verification || "");
  appendField(body, t("verification", "Verification result or evidence"), verifyInput, `record-${record.id}`);
  const final = finalPanel(record.markdown);
  body.append(final.panel);
  form.append(head, body);
  const bar = actionBar(form, verificationHint(record.outcome_verified));
  final.preview.addEventListener("click", () =>
    previewOperation(candidateOperation(record, "replace", form), final.body, form));
  markGated(
    addAction(bar.routine, t("candidate", "Keep candidate"), "", () => stage(record, "replace", form), "r"),
    () => candidateOperation(record, "replace", form)
  );
  markGated(
    addAction(bar.routine, t("vetted", "Vetted"), "", () => stage(record, "vet", form), "v"),
    () => candidateOperation(record, "vet", form)
  );
  addAction(bar.routine, t("defer", "Defer"), "btn-quiet", () => stage(record, "defer", form), "s");
  addAction(bar.destructive, t("discard", "Discard"), "btn-danger", () => {
    if (!window.confirm(t("confirmDiscardRecord", "Applying will delete this record file. Continue?"))) return;
    stage(record, "remove", form);
  }, "d");
  form.addEventListener("input", () => {
    clearFormErrors(form);
    renderGate(form);
  });
  editor.append(form);
  renderGate(form);
  for (const field of form.elements) if (field.tagName === "TEXTAREA") autoGrow(field);
}

function renderAllDecided(editor) {
  const panel = document.createElement("div");
  panel.className = "empty";
  const message = document.createElement("p");
  const inScope = Object.keys(state.clusters).length || candidateRecords().length;
  message.textContent = inScope && !undecidedKeys().length
    ? t("allDecided", "Every record is decided. Apply when ready.")
    : t("queue.empty", "Nothing is awaiting review.");
  const cta = document.createElement("p");
  cta.className = "cta";
  const apply = document.createElement("button");
  apply.type = "button";
  apply.className = "btn-primary";
  apply.textContent = t("apply", "Apply all");
  apply.addEventListener("click", () => finish("/api/apply"));
  cta.append(apply);
  panel.append(message, cta);
  editor.append(panel);
}

function renderConsolidation(cluster, editor) {
  const proposal = state.consolidations.find(item => item.cluster === cluster);
  const form = document.createElement("form");
  const head = document.createElement("div");
  head.className = "surface-head";
  const heading = document.createElement("h2");
  heading.textContent = `${t("cluster", "Cluster")}: ${cluster}`;
  head.append(heading);
  const body = document.createElement("div");
  body.className = "surface-body";
  const memberTitle = document.createElement("h3");
  memberTitle.textContent = t("members", "Cluster members");
  const members = document.createElement("ul");
  members.className = "members";
  for (const id of state.clusters[cluster] || []) {
    const item = document.createElement("li");
    const record = state.records.find(candidate => candidate.id === id);
    const name = document.createElement("strong");
    name.textContent = id;
    item.append(name);
    if (record) {
      renderRecordContext(item, record);
      const source = document.createElement("pre");
      source.textContent = record.markdown;
      item.append(source);
    }
    members.append(item);
  }
  if (!proposal) {
    const notice = document.createElement("p");
    notice.textContent = t("noProposal", "A generalized proposal is required before this cluster can be reviewed.");
    notice.className = "empty";
    body.append(notice, memberTitle, members);
    form.append(head, body);
    editor.append(form);
    return;
  }
  const staged = state.draft.decisions[`cluster:${cluster}`] || {};
  const stagedFields = staged.field_changes || {};
  for (const [key, value] of Object.entries(proposal.fields || {})) {
    const input = makeField(key, Object.hasOwn(stagedFields, key) ? stagedFields[key] : value);
    appendField(body, fieldLabel(key), input, `cluster-${cluster}`);
  }
  const verifyInput = makeField("verification", staged.verification || "");
  appendField(body, t("verification", "Verification result or evidence"), verifyInput, `cluster-${cluster}`);
  const final = finalPanel(proposal.markdown);
  body.append(final.panel, memberTitle, members);
  form.append(head, body);
  /* Whether the proposal's evidence already satisfies vetting is backend knowledge
     (REQ-007): the flag rides on the consolidation like it does on a record. */
  const bar = actionBar(form, verificationHint(proposal.outcome_verified === true));
  final.preview.addEventListener("click", () =>
    previewOperation(mergeOperation(proposal, "candidate", form), final.body, form));
  const memberCount = (state.clusters[cluster] || []).length;
  const confirmMerge = () =>
    window.confirm(format("confirmMerge",
      "Applying will delete the {count} member records this merge replaces. Continue?", {count: memberCount}));
  /* On a resolved cluster keep-separate would only bump the revision: members already
     carry decisions (separate) or deferrals (deferred), so the backend changes nothing. */
  if (!["separate", "deferred"].includes(clusterState(cluster))) {
    addAction(bar.routine, t("keepSeparate", "Keep separate"), "btn-quiet", () => stageKeepSeparate(cluster, form), "x");
  }
  markGated(
    addAction(bar.destructive, t("mergeCandidate", "Merge as candidate"), "btn-danger", () => {
      if (confirmMerge()) stageMerge(proposal, "candidate", form);
    }, "m"),
    () => mergeOperation(proposal, "candidate", form)
  );
  markGated(
    addAction(bar.destructive, t("mergeVetted", "Merge as vetted"), "btn-danger", () => {
      if (confirmMerge()) stageMerge(proposal, "vetted", form);
    }),
    () => mergeOperation(proposal, "vetted", form)
  );
  form.addEventListener("input", () => {
    clearFormErrors(form);
    renderGate(form);
  });
  editor.append(form);
  renderGate(form);
  for (const field of form.elements) if (field.tagName === "TEXTAREA") autoGrow(field);
}

/* ---------- operations ---------- */

function candidateOperation(record, action, form) {
  const fields = {};
  for (const [key, original] of editableEntries(record)) {
    if (form.elements[key].value !== original) fields[key] = form.elements[key].value;
  }
  const operation = {action, record_id: record.id};
  /* `remove` and `defer` carry no payload: the domain rejects a removal that arrives
     with fields or a verification attestation. */
  if (action === "replace" || action === "vet") {
    operation.fields = fields;
    if (form.elements.verification.value) operation.verification = form.elements.verification.value;
  }
  return operation;
}

function mergeOperation(proposal, status, form) {
  const field_changes = {};
  for (const key of Object.keys(proposal.fields || {})) field_changes[key] = form.elements[key].value;
  const operation = {action: "merge", cluster: proposal.cluster, field_changes, status};
  if (form.elements.verification.value) operation.verification = form.elements.verification.value;
  return operation;
}

async function previewOperation(operation, previewNode, form = null) {
  try {
    if (form) clearFormErrors(form);
    const result = await api("/api/preview", {method: "POST", body: JSON.stringify({operation})});
    previewNode.textContent = result.markdown;
    previews[selected] = {token: result.gate_token, operation: JSON.stringify(operation)};
    if (!state.gate_tokens.includes(result.gate_token)) state.gate_tokens.push(result.gate_token);
    if (form) renderGate(form);
    setFeedback(t("previewUpdated", "Preview updated; no decision was staged."));
    return true;
  } catch (error) {
    if (form) reportFormError(form, error);
    else setErrorStatus(error);
  }
  return false;
}

async function previewBeforeStage(operation, previewNode, form) {
  if (await previewOperation(operation, previewNode, form)) {
    setFeedback(t("previewBeforeStage", "Review the final preview, then choose the same action again to stage it."));
  }
}

function applyDraft(result) {
  state.draft = result;
  state.summary = result.summary;
  state.gate_tokens = result.gate_tokens || [];
  for (const key of Object.keys(previews)) delete previews[key];
  renderHeader();
  renderNavigation();
  renderSummary();
  refreshGate();
}

/* With the switch off the surface stays on the record just decided; with it on, and
   nothing undecided left, the selection becomes null and the completion state shows. */
function advance() {
  const remaining = undecidedKeys();
  /* The switch governs jumping to the next item. When there is no next item there is
     nothing to jump to, and the interface still has to say the queue is finished. */
  if (!remaining.length) {
    select(null);
    return;
  }
  if (!document.querySelector("#auto-advance").checked) return;
  select(remaining[0]);
}

async function stage(record, action, form) {
  const operation = candidateOperation(record, action, form);
  if ((action === "replace" || action === "vet") && !previewMatches(form, operation)) {
    await previewBeforeStage(operation, form.querySelector(".final pre"), form);
    return;
  }
  try {
    const result = await api("/api/draft",
      {method: "POST", body: JSON.stringify({expected_revision: state.draft.revision, operation})});
    applyDraft(result);
    setFeedback(t("staged", "Decision staged."));
    advance();
  } catch (error) { reportFormError(form, error); }
}

async function stageMerge(proposal, status, form) {
  const operation = mergeOperation(proposal, status, form);
  if (!previewMatches(form, operation)) {
    await previewBeforeStage(operation, form.querySelector(".final pre"), form);
    return;
  }
  try {
    const result = await api("/api/draft",
      {method: "POST", body: JSON.stringify({expected_revision: state.draft.revision, operation})});
    applyDraft(result);
    setFeedback(t("staged", "Decision staged."));
    advance();
  } catch (error) { reportFormError(form, error); }
}

async function stageKeepSeparate(cluster, form) {
  try {
    const operation = {action: "keep_separate", cluster};
    const result = await api("/api/draft",
      {method: "POST", body: JSON.stringify({expected_revision: state.draft.revision, operation})});
    applyDraft(result);
    setFeedback(t("staged", "Decision staged."));
    advance();
  } catch (error) { reportFormError(form, error); }
}

function select(key) {
  selected = key;
  renderNavigation();
  renderEditor();
}

function formatResult(result) {
  if (result.summary) {
    state.summary = result.summary;
    renderSummary();
    renderHeader();
  }
  return t(`result.${result.status}`, result.status);
}

async function finish(path) {
  const applyButton = document.querySelector("#apply");
  if (path === "/api/apply") applyButton.disabled = true;
  try {
    const body = path === "/api/apply" ? {expected_revision: state.draft.revision} : {};
    const result = await api(path, {method: "POST", body: JSON.stringify(body)});
    setStatus(formatResult(result));
  } catch (error) {
    if (path === "/api/apply") applyButton.disabled = false;
    conflictRecords = error.details && Array.isArray(error.details.records) ? error.details.records : [];
    document.querySelector("#refresh").hidden = conflictRecords.length === 0;
    setErrorStatus(error);
  }
}

async function refreshConflicts() {
  if (!conflictRecords.length) return;
  try {
    state = await api("/api/refresh",
      {method: "POST", body: JSON.stringify({record_ids: conflictRecords, expected_revision: state.draft.revision})});
    state.gate_tokens = state.gate_tokens || [];
    conflictRecords = [];
    for (const key of Object.keys(previews)) delete previews[key];
    document.querySelector("#refresh").hidden = true;
    renderHeader();
    renderNavigation();
    renderEditor();
    renderSummary();
    setStatus(t("refreshed", "Conflicted records refreshed; review them again."));
  } catch (error) { setErrorStatus(error); }
}

/* ---------- keyboard ---------- */

const KEYS = {
  j: () => move(1),
  ArrowDown: () => move(1),
  k: () => move(-1),
  ArrowUp: () => move(-1),
  e: () => {
    const field = document.querySelector("#editor textarea");
    if (field) field.focus();
  },
  p: () => click(".preview-action"),
  v: () => clickKey("v"),
  r: () => clickKey("r"),
  s: () => clickKey("s"),
  d: () => clickKey("d"),
  m: () => clickKey("m"),
  x: () => clickKey("x"),
  "?": () => toggleShortcuts()
};

function click(selector) {
  const button = document.querySelector(`#editor ${selector}`);
  if (button) button.click();
}

function clickKey(key) {
  click(`[data-key="${key}"]`);
}

function move(step) {
  const entries = Array.from(document.querySelectorAll(".queue-entry"));
  if (!entries.length) return;
  const current = entries.findIndex(entry => entry.getAttribute("aria-current") === "true");
  const next = entries[Math.min(entries.length - 1, Math.max(0, (current === -1 ? 0 : current) + step))];
  if (next) next.click();
}

function toggleShortcuts() {
  const hint = document.querySelector("#shortcuts");
  const toggle = document.querySelector("#shortcuts-toggle");
  hint.hidden = !hint.hidden;
  toggle.setAttribute("aria-expanded", String(!hint.hidden));
}

/* No key is bound to Apply all, Cancel or Discard draft: those stay deliberate. */
document.addEventListener("keydown", event => {
  if (event.metaKey || event.ctrlKey || event.altKey) return;
  const target = event.target;
  if (target && target.closest && target.closest("textarea, input, select")) {
    if (event.key === "Escape" && selected) {
      const entry = document.querySelector('.queue-entry[aria-current="true"]');
      if (entry) entry.focus();
    }
    return;
  }
  const handler = KEYS[event.key];
  if (!handler) return;
  event.preventDefault();
  handler();
});

/* ---------- boot ---------- */

document.querySelector("#apply").addEventListener("click", () => finish("/api/apply"));
document.querySelector("#cancel").addEventListener("click", () => finish("/api/cancel"));
document.querySelector("#discard").addEventListener("click", () => {
  const count = Object.keys(state && state.draft ? state.draft.decisions : {}).length
    + (state && state.draft ? state.draft.deferred.length : 0);
  if (!window.confirm(format("confirmDiscardDraft", "{count} staged decisions will be dropped. Continue?", {count}))) {
    return;
  }
  finish("/api/discard");
});
document.querySelector("#refresh").addEventListener("click", refreshConflicts);
document.querySelector("#shortcuts-toggle").addEventListener("click", toggleShortcuts);
api("/api/session").then(async value => {
  state = value;
  state.gate_tokens = state.gate_tokens || [];
  const language = /^[A-Za-z-]+$/.test(state.interaction_language) ? state.interaction_language : "en";
  const catalogLanguage = language.startsWith("pt-") ? "pt" : language;
  const catalogResponse = await fetch(`/i18n/${catalogLanguage}.json`);
  if (catalogResponse.ok) messages = await catalogResponse.json();
  else messages = await (await fetch("/i18n/en.json")).json();
  document.documentElement.lang = language;
  document.documentElement.dir = language === "ar" ? "rtl" : "ltr";
  document.title = t("documentTitle", "CodexSpec Distill Review");
  document.querySelector("#records").setAttribute("aria-label", t("navigationLabel", "Candidate records"));
  document.querySelector("#page-title").textContent = t("title", "Distill review");
  document.querySelector("#summary-title").textContent = t("summary", "Staged changes");
  document.querySelector("#refresh").textContent = t("refresh", "Refresh conflicted records");
  document.querySelector("#apply").textContent = t("apply", "Apply all");
  document.querySelector("#cancel").textContent = t("cancel", "Cancel");
  document.querySelector("#discard").textContent = t("discardDraft", "Discard draft");
  document.querySelector("#auto-advance-label").textContent = t("autoAdvance", "Advance to the next undecided record");
  document.querySelector("#shortcuts").textContent = t("shortcuts", "");
  if (!selected) {
    /* A staged decision never changes a record's stored status, so a restored draft that
       decides everything must open on the completion state, not on an arbitrary record. */
    const first = undecidedKeys()[0];
    selected = first === undefined ? null : first;
  }
  renderHeader();
  renderNavigation();
  renderEditor();
  renderSummary();
  setStatus(t("ready", "Ready."));
}).catch(error => setErrorStatus(error));
