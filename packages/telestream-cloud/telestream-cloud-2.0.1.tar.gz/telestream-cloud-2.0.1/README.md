# Telestream Cloud API client

## Getting Started
### Obtain address for TCS api
In order to use TCS api client first you need to get `ApiKey`. Login to [website](https://cloud.telestream.net/console), go to *Flip* service and open *API Access* tab.
You account will be identified by unique *Api Key*, if it is unavailable click *Reset* button.
### Installation

You can install telestream-cloud using pip:

    pip install telestream-cloud

or directly from GitHub:

    pip install git+https://github.com/pandastream/telestream-cloud-python-sdk.git


### Usage
This example show uploading media file to flip service. If you want to use other service refer to [services](#services).

    import telestream_cloud_flip as flip

    api_key = 'tcs_xxx'
    factory = 'tg01xxxxxxxxxxxx'
    profiles = "h264,imx"
    filepath = "/tmp/video.mp4"

    client = flip.FlipApi()
    client.api_client.configuration.api_key['X-Api-Key'] = api_key

    upload = flip.Uploader(factory, client, filepath, profiles)
    upload.setup()
    video_id = upload.start()

## Services
Api client is divided into parts corresponding to services provided. Currently supported services include:
- [Flip](telestream_cloud_flip_sdk/README.md) - high-volume media transcoding to multiple formats
- [Timed Text Speech](telestream_cloud_tts_sdk/README.md) - automated captions and subtitles creation
- [Quality Control](telestream_cloud_qc_sdk/README.md) - automated quality control for file base media
