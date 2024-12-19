FROM nginx:alpine

RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

COPY ../frontend/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf

ENV VITE_WS_URL=wss://sunba.dev
