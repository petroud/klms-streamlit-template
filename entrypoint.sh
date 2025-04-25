#!/bin/bash
set -e

# Default to "app" if not provided
CONTEXT_PATH=${CONTEXT_PATH:-app}

# Replace placeholders in Nginx config
envsubst '${CONTEXT_PATH}' < templ.nginx.conf > /etc/nginx/nginx.conf

# Start both Streamlit and Nginx
streamlit run /app/app.py --server.baseUrlPath=$CONTEXT_PATH --server.headless=true --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false &
nginx -g 'daemon off;'
