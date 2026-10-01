"use strict";
const fragment = new URLSearchParams(location.hash.slice(1));
const token = fragment.get("token") || "";
history.replaceState(null, "", location.pathname);
let state = null;
let selected = null;
let messages = {};
let conflictRecords = [];
function t(key, fallback) { return messages[key] || fallback; }
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

function fieldId(prefix, key) {
  return `${prefix}-${String(key).replace(/[^A-Za-z0-9_-]/g, "-")}`;
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
  } else {
    document.querySelector("#status").focus();
  }
  setErrorStatus(error);
}

function renderRecordContext(parent, record) {
  const details = document.createElement("dl");
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
    description.textContent = value;
    details.append(term, description);
  }
  parent.append(details);
}

function editableEntries(record) {
  return record.editable_fields.map(key => [key, key === "title" ? record.title : record.fields[key]]);
}

function renderNavigation() {
  const nav = document.querySelector("#records");
  nav.replaceChildren();
  if (!selected) {
    const firstCandidate = state.records.find(record => record.status === "candidate");
    const firstCluster = Object.keys(state.clusters).sort()[0];
    selected = firstCandidate ? firstCandidate.id : (firstCluster ? `cluster:${firstCluster}` : null);
  }
  for (const record of state.records) {
    if (record.status !== "candidate") continue;
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = `${record.id} — ${record.fields.claim}`;
    button.addEventListener("click", () => { selected = record.id; renderEditor(); });
    nav.append(button);
  }
  for (const cluster of Object.keys(state.clusters).sort()) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = `${t("cluster", "Cluster")}: ${cluster}`;
    button.addEventListener("click", () => { selected = `cluster:${cluster}`; renderEditor(); });
    nav.append(button);
  }
}

function renderEditor() {
  const editor = document.querySelector("#editor");
  editor.replaceChildren();
  if (selected && selected.startsWith("cluster:")) {
    renderConsolidation(selected.slice(8), editor);
    return;
  }
  const candidates = state.records.filter(item => item.status === "candidate");
  const record = candidates.find(item => item.id === selected) || candidates[0];
  if (!record) return;
  selected = record.id;
  const title = document.createElement("h2");
  title.textContent = record.id;
  editor.append(title);
  renderRecordContext(editor, record);
  const form = document.createElement("form");
  form.addEventListener("input", () => { delete form.dataset.previewOperation; clearFormErrors(form); });
  const suggested = (state.proposals[record.id] || {}).fields || {};
  const staged = state.draft.decisions[record.id] || {};
  const stagedFields = staged.fields || {};
  for (const [key, value] of editableEntries(record)) {
    const input = document.createElement(value.length > 100 ? "textarea" : "input");
    input.name = key;
    input.value = Object.hasOwn(stagedFields, key)
      ? stagedFields[key]
      : (Object.hasOwn(suggested, key) ? suggested[key] : value);
    appendField(form, fieldLabel(key), input, `record-${record.id}`);
  }
  const verifyInput = document.createElement("textarea");
  verifyInput.name = "verification";
  verifyInput.value = staged.verification || "";
  appendField(form, t("verification", "Verification result or evidence"), verifyInput, `record-${record.id}`);
  const preview = document.createElement("pre");
  preview.textContent = record.markdown;
  preview.id = "preview";
  form.append(preview);
  const actions = document.createElement("div");
  actions.className = "actions";
  const previewButton = document.createElement("button");
  previewButton.type = "button";
  previewButton.textContent = t("preview", "Preview");
  previewButton.addEventListener("click", () => previewOperation(candidateOperation(record, "replace", form), preview, form));
  actions.append(previewButton);
  for (const [label, action] of [[t("candidate", "Keep candidate"), "replace"], [t("vetted", "Vetted"), "vet"], [t("discard", "Discard"), "remove"], [t("defer", "Defer"), "defer"]]) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.addEventListener("click", () => stage(record, action, form));
    actions.append(button);
  }
  form.append(actions);
  editor.append(form);
}

function renderConsolidation(cluster, editor) {
  const proposal = state.consolidations.find(item => item.cluster === cluster);
  const heading = document.createElement("h2");
  heading.textContent = `${t("cluster", "Cluster")}: ${cluster}`;
  editor.append(heading);
  const members = document.createElement("ul");
  for (const id of state.clusters[cluster] || []) {
    const item = document.createElement("li");
    const record = state.records.find(candidate => candidate.id === id);
    const memberTitle = document.createElement("strong");
    memberTitle.textContent = id;
    item.append(memberTitle);
    if (record) {
      renderRecordContext(item, record);
      const source = document.createElement("pre");
      source.textContent = record.markdown;
      item.append(source);
    }
    members.append(item);
  }
  editor.append(members);
  if (!proposal) {
    const notice = document.createElement("p");
    notice.textContent = t("noProposal", "A generalized proposal is required before this cluster can be reviewed.");
    notice.className = "error";
    editor.append(notice);
    return;
  }
  const form = document.createElement("form");
  form.addEventListener("input", () => { delete form.dataset.previewOperation; clearFormErrors(form); });
  const staged = state.draft.decisions[`cluster:${cluster}`] || {};
  const stagedFields = staged.field_changes || {};
  for (const [key, value] of Object.entries(proposal.fields || {})) {
    const input = document.createElement(String(value).length > 100 ? "textarea" : "input");
    input.name = key;
    input.value = Object.hasOwn(stagedFields, key) ? stagedFields[key] : value;
    appendField(form, fieldLabel(key), input, `cluster-${cluster}`);
  }
  const verifyInput = document.createElement("textarea");
  verifyInput.name = "verification";
  verifyInput.value = staged.verification || "";
  appendField(form, t("verification", "Verification result or evidence"), verifyInput, `cluster-${cluster}`);
  const preview = document.createElement("pre");
  preview.textContent = proposal.markdown;
  form.append(preview);
  const actions = document.createElement("div");
  actions.className = "actions";
  const previewButton = document.createElement("button");
  previewButton.type = "button";
  previewButton.textContent = t("preview", "Preview");
  previewButton.addEventListener("click", () => previewOperation(mergeOperation(proposal, "candidate", form), preview, form));
  actions.append(previewButton);
  for (const [label, status] of [[t("mergeCandidate", "Merge as candidate"), "candidate"], [t("mergeVetted", "Merge as vetted"), "vetted"]]) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.addEventListener("click", () => stageMerge(proposal, status, form));
    actions.append(button);
  }
  const keep = document.createElement("button");
  keep.type = "button";
  keep.textContent = t("keepSeparate", "Keep separate");
  keep.addEventListener("click", () => stageKeepSeparate(cluster));
  actions.append(keep);
  form.append(actions);
  editor.append(form);
}

async function stageMerge(proposal, status, form) {
  const operation = mergeOperation(proposal, status, form);
  if (!previewMatches(form, operation)) {
    await previewBeforeStage(operation, form.querySelector("pre"), form);
    return;
  }
  try {
    const result = await api("/api/draft", {method: "POST", body: JSON.stringify({expected_revision: state.draft.revision, operation})});
    state.draft = result;
    state.summary = result.summary;
    delete form.dataset.previewOperation;
    renderSummary();
    setStatus(t("staged", "Decision staged."));
  } catch (error) { reportFormError(form, error); }
}

function mergeOperation(proposal, status, form) {
  const field_changes = {};
  for (const key of Object.keys(proposal.fields || {})) field_changes[key] = form.elements[key].value;
  const operation = {action: "merge", cluster: proposal.cluster, field_changes, status};
  if (form.elements.verification.value) operation.verification = form.elements.verification.value;
  return operation;
}

async function stageKeepSeparate(cluster) {
  try {
    const operation = {action: "keep_separate", cluster};
    const result = await api("/api/draft", {method: "POST", body: JSON.stringify({expected_revision: state.draft.revision, operation})});
    state.draft = result;
    state.summary = result.summary;
    renderSummary();
    setStatus(t("staged", "Decision staged."));
  } catch (error) { setErrorStatus(error); }
}

async function stage(record, action, form) {
  const operation = candidateOperation(record, action, form);
  if ((action === "replace" || action === "vet") && !previewMatches(form, operation)) {
    await previewBeforeStage(operation, form.querySelector("pre"), form);
    return;
  }
  try {
    const result = await api("/api/draft", {method: "POST", body: JSON.stringify({expected_revision: state.draft.revision, operation})});
    state.draft = result;
    state.summary = result.summary;
    delete form.dataset.previewOperation;
    renderSummary();
    setStatus(t("staged", "Decision staged."));
  } catch (error) { reportFormError(form, error); }
}

function candidateOperation(record, action, form) {
  const fields = {};
  for (const [key, original] of editableEntries(record)) {
    if (form.elements[key].value !== original) fields[key] = form.elements[key].value;
  }
  const operation = {action, record_id: record.id};
  if (action === "replace" || action === "vet") operation.fields = fields;
  if (form.elements.verification.value) operation.verification = form.elements.verification.value;
  return operation;
}

function previewMatches(form, operation) {
  return form.dataset.previewOperation === JSON.stringify(operation);
}

async function previewOperation(operation, previewNode, form = null) {
  try {
    if (form) clearFormErrors(form);
    const result = await api("/api/preview", {method: "POST", body: JSON.stringify({operation})});
    previewNode.textContent = result.markdown;
    if (form) form.dataset.previewOperation = JSON.stringify(operation);
    setStatus(t("previewUpdated", "Preview updated; no decision was staged."));
    return true;
  } catch (error) {
    if (form) reportFormError(form, error);
    else setErrorStatus(error);
  }
  return false;
}

async function previewBeforeStage(operation, previewNode, form) {
  if (await previewOperation(operation, previewNode, form)) {
    setStatus(t("previewBeforeStage", "Review the final preview, then choose the same action again to stage it."));
  }
}

function renderSummary() {
  const summary = {};
  for (const key of ["added", "replaced", "promoted", "removed", "merged", "deferred", "undecided"]) {
    summary[t(`summary.${key}`, key)] = (state.summary && state.summary[key]) || [];
  }
  document.querySelector("#summary").textContent = JSON.stringify(summary, null, 2);
}

function formatResult(result) {
  if (result.summary) {
    state.summary = result.summary;
    renderSummary();
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
    state = await api("/api/refresh", {method: "POST", body: JSON.stringify({record_ids: conflictRecords, expected_revision: state.draft.revision})});
    conflictRecords = [];
    document.querySelector("#refresh").hidden = true;
    renderNavigation();
    renderEditor();
    renderSummary();
    setStatus(t("refreshed", "Conflicted records refreshed; review them again."));
  } catch (error) { setErrorStatus(error); }
}

document.querySelector("#apply").addEventListener("click", () => finish("/api/apply"));
document.querySelector("#cancel").addEventListener("click", () => finish("/api/cancel"));
document.querySelector("#discard").addEventListener("click", () => finish("/api/discard"));
document.querySelector("#refresh").addEventListener("click", refreshConflicts);
api("/api/session").then(async value => {
  state = value;
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
  renderNavigation();
  renderEditor();
  renderSummary();
  setStatus(t("ready", "Ready."));
}).catch(error => setErrorStatus(error));
