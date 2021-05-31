# nginx image
FROM nginx:latest

# Delete all orginal config files, create static file directories and ssl lisence directory
RUN rm /etc/nginx/conf.d/default.conf \
&& mkdir -p /usr/share/nginx/html/static \
&& mkdir -p /usr/share/nginx/html/media \
&& mkdir -p /usr/share/nginx/ssl

# images chmod
RUN chown -R www-data:www-data /usr/share/nginx/html/media \
&& chmod -R 775 /usr/share/nginx/html/media

# add config file
ADD ./nginx.conf /etc/nginx/conf.d/

# turn-off daemon mode
CMD ["nginx", "-g", "daemon off;"]
