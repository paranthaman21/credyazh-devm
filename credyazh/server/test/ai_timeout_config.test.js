import test from 'node:test';
import assert from 'node:assert/strict';
import { AI_TIMEOUT_MS } from '../src/aiClient.js';

test('Node-to-Python timeout exceeds the default 8s AI shared deadline', () => {
  assert.equal(Number.isFinite(AI_TIMEOUT_MS), true);
  assert.ok(AI_TIMEOUT_MS >= 10000, 'Express must outlive the 8000ms Python deadline');
});
