FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

ARG DOMAIN

RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

COPY nginx.conf.template /etc/nginx/nginx.conf.template

COPY dist/ /usr/share/nginx/html/

RUN envsubst '${DOMAIN}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    nginx -t

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
