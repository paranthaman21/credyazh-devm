# ─── CredYazh Server — Dockerfile ────────────────────────────────────────────
# Node.js 18 LTS Express API (Port 4000)
# Serves: /api/customers  /api/ledger  /api/draft/*

FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY package.json .
RUN npm install --omit=dev

# Copy application source
COPY . .

# Expose Express port
EXPOSE 4000

# Start the server
CMD ["node", "src/index.js"]

