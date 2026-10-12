# React

## Purpose and Applicability

Apply when affected behavior uses React components, hooks, effects, rendering or framework lifecycle. Dependencies/extensions identify candidates; inspect actual imports, call paths, rendering and framework/version guarantees. A React dependency alone does not make every TypeScript file React behavior.

## Non-Applicability and False Positives

Do not mandate effects, memoization, local state, AbortController or cleanup when actual ownership and lifecycle do not require them. TypeScript/JavaScript language details are loaded separately only when relevant.

## Necessary Evidence and Completion

Trace props/state producers into rendering/effects, including closure inputs, dependency changes and mount/unmount or cancellation paths that matter. Record current contract or maintenance benefit, contrary framework evidence and completion. Stop after relevant behavior is established.

## Checkpoints

### REACT-HOOKS

Check applicable Rules of Hooks, effect dependencies, stale closure behavior and cleanup against actual component/lifecycle paths. Derived state and effect use are maintenance candidates only with a present demonstrated problem; missing required behavior can activate checks even before a hook is implemented.

## Conditional Scoring Examples

The retained advisory exemplars below calibrate only substantiated, applicable findings. They never create obligations or defect priorities; common.md controls evidence and false positives.

> Apply these **in addition to** the applicable base exemplars in [TypeScript](../languages/typescript.md) or [JavaScript](../languages/javascript.md).

**Axis 3 — Mandatory Subsection: Hooks Compliance**:

- `useEffect` with incomplete dependency array: **-8**
- Derived state stored as separate `useState` (should be computed): **-8**
- Unnecessary `useEffect` when `useMemo` or direct computation suffices: **-5**
- Stale closure risk in async/event handler: **-8**
- Missing `useEffect` cleanup for subscriptions/timers: **-8**

**Axis 4 — Architecture (React-specific)**:

- Component exceeding 200 lines: **-5**
- Business logic not extracted to custom Hook: **-8**
- Multiple primary components in one file: **-8**
- Missing loading/error state for async operation: **-5**
- Prop drilling more than 3 levels deep: **-5**
- Unnecessary global/lifted state: **-8**
- Unmemoized expensive computation in render: **-8**
- Object/function created in render without `useCallback`/`useMemo`: **-5**
- Missing `React.memo` for frequently re-rendered component: **-5**
- Race condition in async operation: **-10**
