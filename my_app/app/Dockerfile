# Use an official Node runtime as a parent image
FROM node:16.0.0-alpine3.13

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files into the container
COPY ./ /app/

# Install any needed packages specified in package.json
RUN npm install


# Build the production-ready version of the application
RUN npm run build

# Serve the application using a lightweight web server
FROM nginx:1.21.0-alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]