FROM nginx:latest

# Remove the entire conf.d directory to prevent default configurations
RUN rm -rf /etc/nginx/conf.d/*

# Copy your custom nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory for SSL certificates
RUN mkdir -p /home/naruto/nginx-certs

# Expose ports
EXPOSE 443 8000

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]