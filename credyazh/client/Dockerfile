# ─── CredYazh Client — Dockerfile ────────────────────────────────────────────
# React 18 + Vite PWA
# Stage 1: build the static bundle
# Stage 2: serve with Nginx on Port 80

# ── Stage 1: Build ────────────────────────────────────────────────────────────
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies (layer cache)
COPY package.json .
RUN npm install

# Copy source and build
COPY . .

# VITE_API_URL is injected at build time via --build-arg / compose build args
ARG VITE_API_URL=/api
ARG VITE_YAZH_TOUR_ENABLED=true
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_YAZH_TOUR_ENABLED=$VITE_YAZH_TOUR_ENABLED

RUN npm run build

# ── Stage 2: Serve with Nginx ─────────────────────────────────────────────────
FROM nginx:alpine

# Remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy built React app
COPY --from=builder /app/dist /usr/share/nginx/html

# Custom Nginx config: proxy /api → Express server, serve SPA for all other routes
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

