const rawApiBase = import.meta.env.VITE_API_URL || '/api';
const API_BASE = rawApiBase.replace(/\/+$/, '');

function newRequestId() {
  return (crypto.randomUUID && crypto.randomUUID()) || String(Date.now());
}

// Centralized API helper
async function call(path, options = {}) {
  const requestId = options.requestId || newRequestId();
  const headers = { 'X-Request-Id': requestId, ...(options.headers || {}) };
  const res = await fetch(API_BASE + path, { ...options, headers });
  const data = await res.json().catch(() => ( {} ));
  if (!res.ok) {
    const err = new Error(data.error || `Request failed (${res.status})`);
    err.name = res.status === 0 ? 'NetworkError' : err.name;
    throw err;
  }
  if (data && typeof data === 'object') {
    data.requestId = data.requestId || data.metrics?.requestId || requestId;
  }
  return data;
}

const json = (method, body, headers = {}) => ({
  method,
  headers: { 'Content-Type': 'application/json', ...headers },
  body: JSON.stringify(body)
});

export const api = {
  // Customer CRUD
  customers: () => call('/customers'),
  addCustomer: (c) => call('/customers', json('POST', c)),
  updateCustomer: (id, data) => call(`/customers/${id}`, json('PUT', data)),
  deleteCustomer: (id) => call(`/customers/${id}`, { method: 'DELETE' }),

  // Archived handling
  listArchived: () => call('/customers/archived/list'),
  restoreCustomer: (id) => call(`/customers/${id}/restore`, { method: 'PUT' }),

  // Ledger & drafts
  ledger: (id) => call(`/customers/${id}/ledger`),
  draftFromText: (text, signal) => call('/draft/text', { ...json('POST', { text }), signal }),
  draftFromAudio: async (wavBlob, signal) => {
    const t0 = performance.now();
    const form = new FormData();
    form.append('audio', wavBlob, 'clip.wav');
    const data = await call('/draft/audio', { method: 'POST', body: form, signal });
    const uploadMs = Math.round(performance.now() - t0);
    return {
      ...data,
      clientTransport: { upload_ms: uploadMs }
    };
  },

  // Confirm and reverse ledger entries
  confirm: (entry, key) => call('/ledger', json('POST', entry, { 'Idempotency-Key': key })),
  reverse: (id, reason) => call(`/ledger/${id}/reverse`, json('POST', { reason })),

  // WhatsApp message generation (proxy to AI service)
  generateWhatsAppMessage: (customerId, language = 'english') =>
    call(`/customers/${customerId}/whatsapp-message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language })
    })
};

export const rupees = (paise) => '\u20B9' + (paise / 100).toLocaleString('en-IN', { minimumFractionDigits: paise % 100 ? 2 : 0 });
