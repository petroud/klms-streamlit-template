FROM python:3.13
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --prefer-binary -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

# Install NGINX and gettext (for envsubst)
RUN apt-get update && \
    apt-get install -y nginx gettext-base && \
    apt-get clean

# Expose NGINX's port
EXPOSE 8080


# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]
