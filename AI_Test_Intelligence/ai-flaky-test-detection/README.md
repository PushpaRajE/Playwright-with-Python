# AI Flaky Test Detection

## Problem
Some automated tests fail intermittently without code changes.

## Solution
This project detects flaky tests by analyzing recent execution history.

## Logic
If a test has both PASS and FAIL results in recent runs,
it is marked as flaky.

## Use Case
- Identify unstable tests
- Reduce false failures in CI pipelines
