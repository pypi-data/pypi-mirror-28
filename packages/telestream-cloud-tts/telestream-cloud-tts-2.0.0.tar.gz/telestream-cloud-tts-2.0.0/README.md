# Telestream Cloud Timed Text Speech Python SDK

This library provides a low-level interface to the REST API of Telestream Cloud, the online video encoding service.

## Requirements.

Python 2.7 and 3.4+

## Getting Started
### Initialize client

```python
import time
import telestream_cloud_tts
from telestream_cloud_tts.rest import ApiException
from pprint import pprint

configuration = telestream_cloud_tts.Configuration()
configuration.api_key['X-Api-Key'] = 'YOUR_API_KEY'
api_instance = telestream_cloud_tts.TtsApi(telestream_cloud_tts.ApiClient(configuration))
project_id = 'project_id_example'
```

### Create a new project

```python
project = api_instance.create_project(telestream_cloud_tts.Project(name = "Example project name"))
```

### Create a job from source URL
```
job = api_instance.create_job(project_id, telestream_cloud_tts.Job("http://url/to/file.mp4"))
pprint(job)
```

### Create a job from file
```
upload = telestream_cloud_tts.Uploader(project_id, api_instance, "/path/to/file.mp4", "", {})
upload.setup()
job_id = upload.start()
print(job_id)
```

## Documentation for API Endpoints

All URIs are relative to *https://api.cloud.telestream.net/tts/v1.0*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*TtsApi* | [**corpora**](docs/TtsApi.md#corpora) | **GET** /projects/{projectID}/corpora | Returns a collection of Corpora
*TtsApi* | [**corpus**](docs/TtsApi.md#corpus) | **GET** /projects/{projectID}/corpora/{name} | Returns the Corpus
*TtsApi* | [**create_corpus**](docs/TtsApi.md#create_corpus) | **POST** /projects/{projectID}/corpora/{name} | Creates a new Corpus
*TtsApi* | [**create_job**](docs/TtsApi.md#create_job) | **POST** /projects/{projectID}/jobs | Creates a new Job
*TtsApi* | [**create_project**](docs/TtsApi.md#create_project) | **POST** /projects | Creates a new Project
*TtsApi* | [**delete_corpus**](docs/TtsApi.md#delete_corpus) | **DELETE** /projects/{projectID}/corpora/{name} | Creates a new Corpus
*TtsApi* | [**delete_job**](docs/TtsApi.md#delete_job) | **DELETE** /projects/{projectID}/jobs/{id} | Deletes the Job
*TtsApi* | [**delete_project**](docs/TtsApi.md#delete_project) | **DELETE** /projects/{projectID} | Deletes the Project
*TtsApi* | [**job**](docs/TtsApi.md#job) | **GET** /projects/{projectID}/jobs/{id} | Returns the Job
*TtsApi* | [**job_result**](docs/TtsApi.md#job_result) | **GET** /projects/{projectID}/jobs/{id}/result | Returns the Job Result
*TtsApi* | [**jobs**](docs/TtsApi.md#jobs) | **GET** /projects/{projectID}/jobs | Returns a collection of Jobs
*TtsApi* | [**project**](docs/TtsApi.md#project) | **GET** /projects/{projectID} | Returns the Project
*TtsApi* | [**projects**](docs/TtsApi.md#projects) | **GET** /projects | Returns a collection of Projects
*TtsApi* | [**train_project**](docs/TtsApi.md#train_project) | **POST** /projects/{projectID}/train | Queues training
*TtsApi* | [**update_project**](docs/TtsApi.md#update_project) | **PUT** /projects/{projectID} | Updates an existing Project
*TtsApi* | [**upload_video**](docs/TtsApi.md#upload_video) | **POST** /projects/{projectID}/jobs/upload | Creates an upload session


## Documentation For Models

 - [CorporaCollection](docs/CorporaCollection.md)
 - [Corpus](docs/Corpus.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [ExtraFile](docs/ExtraFile.md)
 - [Fragment](docs/Fragment.md)
 - [FragmentVariant](docs/FragmentVariant.md)
 - [Job](docs/Job.md)
 - [JobResult](docs/JobResult.md)
 - [JobsCollection](docs/JobsCollection.md)
 - [Project](docs/Project.md)
 - [ProjectsCollection](docs/ProjectsCollection.md)
 - [Result](docs/Result.md)
 - [UploadSession](docs/UploadSession.md)
 - [VideoUploadBody](docs/VideoUploadBody.md)


## Documentation For Authorization


## apiKey

- **Type**: API key
- **API key parameter name**: X-Api-Key
- **Location**: HTTP header


## Author

cloudsupport@telestream.net

