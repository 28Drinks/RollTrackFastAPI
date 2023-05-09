# Use an official Python runtime as a parent image
FROM python:3.10.4-slim-buster

ENV MONGO_DETAILS="mongodb+srv://elias:EineMate123@test.b8l0oo5.mongodb.net/rollbots?retryWrites=true&w=majority"

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./ /app

# Expose the port that the application runs on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
