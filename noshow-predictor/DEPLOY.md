# Deploy to GCP (Cloud Run + Terraform)

Use Google Cloud Shell (console.cloud.google.com, the >_ icon). It already has
gcloud and terraform installed. Upload or git clone this project there.

## 0. Setup
```
export PROJECT_ID=your-project-id
export REGION=europe-west4
gcloud config set project $PROJECT_ID
```
The project needs billing enabled. Cloud Run scales to zero, so a demo costs
close to nothing, but destroy it when done (step 5).

## 1. Create the registry and enable APIs
```
cd terraform
terraform init
terraform apply -var="project_id=$PROJECT_ID"
```

## 2. Build and push the image
```
cd ..
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/noshow/noshow-predictor:v1
```

## 3. Deploy the service
```
cd terraform
terraform apply -var="project_id=$PROJECT_ID" \
  -var="image=$REGION-docker.pkg.dev/$PROJECT_ID/noshow/noshow-predictor:v1"
```
Terraform prints `service_url`.

## 4. Test
```
URL=$(terraform output -raw service_url)
curl $URL/health
curl -X POST $URL/predict -H "Content-Type: application/json" -d '{"route":"AMS-LHR","hour":8,"day_of_week":4,"month":6,"booked_passengers":180,"advance_booking_days":40,"flex_share":0.3,"connecting_share":0.2}'
```
Also open $URL/docs in a browser.

## 5. Clean up
```
terraform destroy -var="project_id=$PROJECT_ID"
```
