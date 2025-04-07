#!/bin/bash
# Script to deploy the model API to Google Cloud Run

# Set variables
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
REPOSITORY="drug-discovery"
IMAGE_NAME="drug-discovery-api"
TAG="latest"

# Build the Docker image locally
docker build -t $IMAGE_NAME:$TAG ./api

# Configure Docker to use Google Container Registry
gcloud auth configure-docker gcr.io

# Tag the image for Google Container Registry
docker tag $IMAGE_NAME:$TAG gcr.io/$PROJECT_ID/$IMAGE_NAME:$TAG

# Push the image to Google Container Registry
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:$TAG

# Deploy to Cloud Run
gcloud run deploy drug-discovery-api \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME:$TAG \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --cpu 4 \
  --memory 16Gi \
  --timeout 3600