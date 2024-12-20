
# Use an official Node.js runtime as a base image
FROM node:20
WORKDIR /usr/src/app
 
# Copy package
COPY package*.json ./

# Strict SSL to false and setting npm registry
RUN npm config set strict-ssl false 
RUN npm config set registry https://registry.npmjs.org/

# Install dependencies
RUN npm install --legacy-peer-deps
 
# Copy the local code to the container
COPY . .

RUN rm -r /usr/src/app/node_modules/@fortawesome/

RUN mv ./@fortawesome/ /usr/src/app/node_modules/

EXPOSE 4200
 
# Define the command to run the application
# CMD ["ng", "serve", "--host", "0.0.0.0", "--port", "4200"]

CMD ["npm", "start"]