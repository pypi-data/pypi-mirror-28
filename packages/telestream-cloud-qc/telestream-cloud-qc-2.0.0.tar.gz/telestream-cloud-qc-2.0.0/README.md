# Telestream Cloud Quality Control Python SDK

This library provides a low-level interface to the REST API of Telestream Cloud, the online video quality service.

## Requirements.

Python 2.7 and 3.4+

## Getting Started
### Create new project and submit job

```python
# Create new project based on DPP V5 IMX template
project = client.create_project(options = {"template" : "dpp_v5_imx",
                                           "name" : "SampleProject" })

# Start new job and override some tests
client.create_job(project = project.id, data = {"url" : "https://samples.ffmpeg.org/mov/mp4/panda.mp4"
                                                "options" : {"file_tests" : {
                                                    "container_test" : {
                                                        "conatiner" : "Mp4",
                                                        "reject_on_error" : True},
                                                    "video_codec_test" : {
                                                        "video_codec" : "H264",
                                                        "video_profile" : "H264Main",
                                                        }
                                                }}
})
```


```python
# Create new project based on DPP V5 IMX template
project = client.create_project(options = {"template" : "dpp_v5_imx",
                                           "name" : "SampleProject" })

# Start new job with default template attributes
client.create_job(project = project.id, data = {"url" : "https://samples.ffmpeg.org/mov/mp4/panda.mp4"})
```

```python
# Create new project based on DPP V5 IMX template
project = client.create_project(options = {"template" : "ard_zdf_1_a",
                                           "name" : "SampleProject"})

# Start new job with PSE check enabled
client.create_job(project = project.id, data = {"url" : "https://samples.ffmpeg.org/mov/mp4/panda.mp4"
                                                "options" : {"video_tests" : {
                                                    "video_test" : [{
                                                        "flash_test":
                                                        {"checked": True,
                                                         "check_type" : "PSEStandard",
                                                         "check_for_extended": True,
                                                         "check_for_red": True,
                                                         "check_for_patterns": True,
                                                         "reject_on_error": True,
                                                         "do_correction": False}
                                                    }]
                                                }
                                                }
})
```

### Upload file to QC service

```python
import telestream_cloud_qc as qc

api_key = 'tcs_xxx'
project = 'tg01xxxxxxxxxxxx'
filepath = "/tmp/video.mp4"

client = qc.QcApi()
client.configuration.api_key['X-Api-Key'] = api_key

upload = qc.Uploader(project, client, filepath, profiles)
upload.setup()
video_id = upload.start()
```

## Documentation for API Endpoints

All URIs are relative to *https://api.cloud.telestream.net/qc/v1.0*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*QcApi* | [**cancel_job**](docs/QcApi.md#cancel_job) | **PUT** /projects/{project_id}/jobs/{job_id}/cancel.json | 
*QcApi* | [**create_job**](docs/QcApi.md#create_job) | **POST** /projects/{project_id}/jobs.json | Create a new job
*QcApi* | [**create_project**](docs/QcApi.md#create_project) | **POST** /projects.json | Create a new project
*QcApi* | [**get_job**](docs/QcApi.md#get_job) | **GET** /projects/{project_id}/jobs/{job_id}.json | Get QC job
*QcApi* | [**get_project**](docs/QcApi.md#get_project) | **GET** /projects/{project_id}.json | Get project by Id
*QcApi* | [**list_jobs**](docs/QcApi.md#list_jobs) | **GET** /projects/{project_id}/jobs.json | Get jobs form projects
*QcApi* | [**list_projects**](docs/QcApi.md#list_projects) | **GET** /projects.json | List all projects for an account
*QcApi* | [**modify_project**](docs/QcApi.md#modify_project) | **PUT** /projects/{project_id}.json | Modify project
*QcApi* | [**proxy**](docs/QcApi.md#proxy) | **GET** /projects/{project_id}/jobs/{job_id}/proxy.json | 
*QcApi* | [**remove_job**](docs/QcApi.md#remove_job) | **DELETE** /projects/{project_id}/jobs/{job_id}.json | 
*QcApi* | [**remove_project**](docs/QcApi.md#remove_project) | **DELETE** /projects/{project_id}.json | 
*QcApi* | [**signed_urls**](docs/QcApi.md#signed_urls) | **GET** /projects/{project_id}/jobs/{job_id}/signed-urls.json | 
*QcApi* | [**upload_video**](docs/QcApi.md#upload_video) | **POST** /projects/{project_id}/upload.json | Creates an upload session


## Documentation For Models

 - [Alert](docs/Alert.md)
 - [AudioStream](docs/AudioStream.md)
 - [Container](docs/Container.md)
 - [Data](docs/Data.md)
 - [Data1](docs/Data1.md)
 - [ExtraFile](docs/ExtraFile.md)
 - [Job](docs/Job.md)
 - [JobData](docs/JobData.md)
 - [JobDetails](docs/JobDetails.md)
 - [JobDetailsResult](docs/JobDetailsResult.md)
 - [JobsCollection](docs/JobsCollection.md)
 - [Media](docs/Media.md)
 - [Options](docs/Options.md)
 - [Project](docs/Project.md)
 - [Proxy](docs/Proxy.md)
 - [UploadSession](docs/UploadSession.md)
 - [VideoStream](docs/VideoStream.md)
 - [VideoUploadBody](docs/VideoUploadBody.md)


## Documentation For Authorization


## apiKey

- **Type**: API key
- **API key parameter name**: X-Api-Key
- **Location**: HTTP header


## Author

cloudsupport@telestream.net

