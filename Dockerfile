
# Start from a Python image.
FROM python:latest

# Set the working directory.
WORKDIR /usr/src/fastApiCRUD

# Install dependencies.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir logs


# Copy the rest of your app's source code.
COPY . .

# Start Nginx and your app.
CMD python -m app.main