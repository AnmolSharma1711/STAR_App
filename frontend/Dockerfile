# Stage 1: Build the React application
# Uses a lightweight Node.js base image (e.g., node:20-alpine, choose a recent stable version)
FROM node:20-alpine as builder

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and related files to leverage Docker cache
COPY package*.json ./

# Install dependencies. `npm ci` is generally preferred for clean installs in CI/CD environments
RUN npm ci --silent

# Copy the rest of the application code
COPY . .

# Build the React app for production (adjust the build command if using Vite or other tools)
RUN npm run build

# Stage 2: Serve the application with Nginx
# Uses a lightweight Nginx base image
FROM nginx:alpine as server

# Copy the built static files from the 'builder' stage to the Nginx serving directory
# The default build output folder is often 'build' or 'dist' (adjust if necessary)
COPY --from=builder /app/build /usr/share/nginx/html

# Optional: Copy a custom nginx configuration file for client-side routing and caching
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80, the default for web servers
EXPOSE 80

# Command to run Nginx and keep it running in the foreground so Docker can track it
CMD ["nginx", "-g", "daemon off;"]
