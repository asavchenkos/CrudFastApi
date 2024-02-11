
# Start from a Python image.
FROM python:latest

# Set the working directory.
WORKDIR /usr/src/fastApiCRUD

# Install dependencies.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Nginx.
RUN apt-get update && apt-get install -y nginx

# Remove the default Nginx configuration file.
RUN rm /etc/nginx/sites-enabled/default
RUN rm /etc/nginx/sites-available/default

# Copy the Nginx configuration file.
# This file should be in the same directory as your Dockerfile.
COPY nginx.conf /etc/nginx/sites-enabled/
COPY nginx.conf /etc/nginx/sites-available/
RUN mkdir logs


# Copy the rest of your app's source code.
COPY . .

# Start Nginx and your app.
CMD service nginx start && python -m app.main


