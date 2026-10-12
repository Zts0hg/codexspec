### P-2026-1011-105126-3: Plugin root changes must cover every component path

- claim: When changing a plugin package root, revalidate component discovery and root-relative references against the same released source tree.
- type: pitfall
- scope/when: changing marketplace source roots, component paths, or plugin resource layout
- root-cause: A root-relative helper and an implicit hook location can become unavailable when the root moves. Keeping an older source tag while changing its root also loads older commands whose references still require the older layout.
- workaround: Exercise current bundle startup and standalone runtime behavior from an external plugin cache without the CLI. Publish the new tag first, then update source root, component paths, ref and version together; inspect referenced paths in that immutable tag rather than substituting the development checkout.
- lesson: Relative-path meaning depends on both the package root and the selected source version; publication must preserve their compatibility throughout the transition.
- evidence.facts: Two integration regressions preceded the synchronized helper reference and explicit hook declaration; 118 checks then passed. A subsequent raw Git probe showed that moving the root while retaining v0.7.23 made its command's helper reference unavailable. The release-layout regression failed before the preceding tag's metadata was restored.
- evidence.state: The source-tag incompatibility was independently reproduced during feature delivery. After v0.7.24 was uploaded and tagged at 0ceea933bad70cd4d5e2ba5f04d76754a5721b75, all 26 standards and the nested helper/hooks were verified against that immutable tag. The release-layout regression passed for the new repository-root entry. Development bundle and published-entry checks are distinct; native plugin-host execution is not claimed. The generalized lesson has not been separately endorsed by a human.
- provenance: distill during PR preparation, 2026-10-12; derivation: inferred; confidence: high
- status: candidate
