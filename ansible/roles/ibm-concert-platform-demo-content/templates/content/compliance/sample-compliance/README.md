#Sample data for IBM Concert compliance

This git repo includes multiple samples for running the compliance demo. 

---


## 1) download samples

## 2) execution of the samples in the below order 

  - Install the latest version of IBM Concert and create a sample app using SBOM.file 
  - creating of the application is required only if the sample application is not present in the IBM Concert. 
  ```
  sample_sbom_file.json
  ```

  ### a) adding the catalog 
  - Click on Dimensions and Compliance 
  - Click on catalogs and upload catalog 
  - from the compliance sample folder drag and drop file below from the samples folder and click on upload.
  ```
  NIST_SP-800-53_rev4_LOW-baseline-resolved-profile_catalog.json
  ``` 
  
  ### b) create / upload a profile
  - upload a profile using the curl command. 

   create a bearer token using the following command 

   ```
    curl -k -X 'POST' \
  'https://9.46.253.14:8000/roja/api/v1/login' \
  -H 'accept: application/json' \
  -H 'InstanceId: 0000-0000-0000-0000' \
  -H 'Content-Type: application/json' \
  -d '{
  "password": "<PUT_YOUR_PASSWORD>",
  "username": "<PUT_YOUR_USERNAME>"
}'
```

user this to upload the profile 
```
curl -k -X 'POST' \
  'https://9.46.253.14:12443/compliance/api/v1/import_profiles' \
  -H 'accept: application/json' \
  -H 'instanceId: 0000-0000-0000-0000' \
  -H 'Authorization: Bearer <TOKEN_GENERATED_FROM_ABOVE_COMAMND>' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@profileupload.json;type=application/json'

```
### b) create component definition using the below component definition files 

- To create component definition, we need three things 
- Application ID 
- Environment ID 
- Profile ID 

to get the application and environment UUIDS use the below curl command 

```curl -k -X 'GET' \
  'https://9.46.253.14:12443/roja/api/v1/applications' \
  -H 'accept: application/json' \
  -H 'instanceId: 0000-0000-0000-0000' \
  -H 'Authorization: Bearer <TOKEN_GENERATED_FROM_ABOVE_COMAMND>'
```
already valid profile id's are present in the component definition. 


### c) loading the resource definition / component files 

This is the one which maps the applications with the resources. 

In this sample we load 2 component definitions. Below are the samples in the below samples we need to map
the application_id,environment_id,profile_id,control_ids" form the above samples control id's are from the profile. 


```
curl -X 'POST' \
  'https://9.46.253.14:12443/compliance/api/v1/component_definitions' \
  -H 'accept: application/json' \
  -H 'instanceId: 0000-0000-0000-0000' \
  -H 'Authorization: Bearer <TOKEN_GENERATED_FROM_ABOVE_COMAMND>' \
  -H 'Content-Type: application/json' \
  -d '{
    "component_definition_id": "c89442f7-8a13-4d8a-aeec-406d5de888ba",
    "application_id": "37043cd7-3ec1-4213-b42f-f1bb29db8bd4", 
    "profile_id": "7eca4579-7ed9-4552-5da6-738126660be3",
    "title": "IAM User",
    "description": "Streamlined solution for organizing, storing, and accessing user data with enhanced performance and user-friendly interface.",
    "version": "2.0",
    "environment_id": "e9866102-cc86-475a-b12a-136a5c576dc8",
    "control_ids": [
        "42749fb4-8f56-4832-8ee2-f11e3630d242",
        "3db0affb-9543-4ae8-9bf5-380ee5a133af",
        "1acb6883-d52f-4354-9a80-6c2a973dc732",
        "d0e7dd35-cbee-4748-90d1-e7e5f1478755",
        "ab4b29ae-1ac2-405f-987a-d3c759964790",
        "12a2615f-5f37-4949-9166-05b4bd1f4184"
    ]
}'

```

sample2 

```
curl -X 'POST' \
  'https://9.46.253.14:12443/compliance/api/v1/component_definitions' \
  -H 'accept: application/json' \
  -H 'instanceId: 0000-0000-0000-0000' \
  -H 'Authorization: Bearer <TOKEN_GENERATED_FROM_ABOVE_COMAMND>' \
  -H 'Content-Type: application/json' \
  -d '{
   "component_definition_id": "c89442f7-8a13-4d8a-aeec-406d5de890ba",
    "application_id": "37043cd7-3ec1-4213-b42f-f1bb29db8bd4",
    "profile_id": "7eca4579-7ed9-4552-5da6-738126660be3",
    "title": "clould object storage",
    "description": "Streamlined solution for organizing, storing, and accessing user data with enhanced performance and user-friendly interface.",
    "version": "2.0",
    "environment_id": "e9866102-cc86-475a-b12a-136a5c576dc8",
    "control_ids": [
        "93078ed0-52bd-45d6-a324-d93d92bbe4c0",
        "474b35fd-c941-4eaf-bbea-ebad0c98dbf0",
        "fc164c75-6b58-49a8-9acc-6e65ff3a3eb6",
        "28c68778-26a5-472f-bcfc-d4740a9d1a81",
        "23cbd05a-3e2e-442d-a701-1e0cd9c14990",
        "65850759-0937-4335-a55b-b356ec79e887"
    ]
}'


```




### d) creating an assessment plan 

- The assesment plan can be created in IBM Concert UI . 
In the compliance section click on create new assement plan . select the app / env and profile where the component definition to create a sample assessment plan. 

alternatively you can use to API to create a assessment plan . below is the sample 
```
curl -X 'POST' \
  'https://9.46.253.14:12443/compliance/api/v1/component_definitions' \
  -H 'accept: application/json' \
  -H 'instanceId: 0000-0000-0000-0000' \
 -H 'Authorization: Bearer <TOKEN_GENERATED_FROM_ABOVE_COMAMND>' \
  -H 'Content-Type: application/json' \
  -d '{
    "profile_id": "7eca4579-7ed9-4552-5da6-738126660be3",
    "title": "My new assessment plan",
    "description": "My new assessment plan",
    "version": "1.0",
    "component_definition_ids": [
        "c89442f7-8a13-4d8a-aeec-406d5de890ba",
        "c89442f7-8a13-4d8a-aeec-406d5de999ba"
    ],
    "additional_control_ids": [],
    "start_date": "2024-05-14",
    "end_date": "2024-06-08"
}’

```

### e) loading the posture sample 

this will load the posture sample and the corresponding assessment results

```
curl -k -X POST https://9.46.253.14:12443/ingestion/roja/v1/ingest/upload_files \
  -H 'Content-Type: multipart/form-data' \
  -H 'Accept: application/json' \
  -H 'InstanceId: 0000-0000-0000-0000' \
  -H "Authorization: Bearer <TOKEN_GENERATED_FROM_ABOVE_COMAMND>"\
  -F "data_type=compliance"\
  -F "filename=@posture.json"
  ```

