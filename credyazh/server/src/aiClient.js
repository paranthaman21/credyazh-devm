import { randomUUID } from 'node:crypto';

const rawAiUrl = process.env.AI_SERVICE_URL || 'http://127.0.0.1:8000';
const AI_URL = rawAiUrl.replace(/\/+$/, '');

// Must exceed the Python shared deadline so Express can return a structured
// error/draft after the AI service stops. Default 10s = 8s AI budget + overhead.
export const AI_TIMEOUT_MS = Number(process.env.AI_CLIENT_TIMEOUT_MS) || 10000;

let aiDispatcher;
try {
  const { Agent } = await import('undici');
  aiDispatcher = new Agent({
    keepAliveTimeout: 30_000,
    keepAliveMaxTimeout: 60_000,
    connections: 8,
    pipelining: 1
  });
} catch {
  aiDispatcher = undefined;
}

function headers(requestId, extra = {}) {
  return {
    'X-Request-Id': requestId || randomUUID(),
    ...extra
  };
}

async function check(r) {
  if (!r.ok) {
    let detail = '';
    try { detail = (await r.json()).detail; } catch { /* ignore */ }
    const err = new Error(detail || `AI service error ${r.status}`);
    err.status = 502;
    throw err;
  }
  return r.json();
}

async function aiFetch(path, init) {
  const t0 = performance.now();
  const res = await fetch(`${AI_URL}${path}`, {
    ...init,
    dispatcher: aiDispatcher,
    signal: init.signal || AbortSignal.timeout(AI_TIMEOUT_MS)
  });
  const nodeToPythonMs = Math.round(performance.now() - t0);
  const json = await check(res);
  if (json && typeof json === 'object') {
    json.metrics = {
      ...(json.metrics || {}),
      node_to_python_ms: nodeToPythonMs
    };
  }
  return json;
}

export async function draftFromAudio(buffer, mimetype, requestId) {
  // Send raw WAV bytes. Python already accepts audio/*; this avoids a second Base64 pass.
  return aiFetch('/draft/audio', {
    method: 'POST',
    headers: headers(requestId, { 'Content-Type': mimetype || 'audio/wav' }),
    body: buffer
  });
}

export async function draftFromText(text, requestId) {
  return aiFetch('/draft/text', {
    method: 'POST',
    headers: headers(requestId, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({ text })
  });
}
