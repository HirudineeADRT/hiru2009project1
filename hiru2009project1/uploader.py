import boto3
s3 = boto3.client("s3")
from wand.image import Image
from google.cloud import storage

client = storage.Client()

THUMBNAIL_BUCKET = 'hirutest01'

def handler(request):
    
    bucket = client.get_bucket('hirutest02')
    blob = bucket.get_blob('name.png')
    imagedata = blob.download_as_string()
    # Create a new image object and resample it
    newimage = Image(blob=imagedata)
    newimage.sample(200,200)
    # Upload the resampled image to the other bucket chnage
    bucket = client.get_bucket(THUMBNAIL_BUCKET)
    newblob = bucket.blob('thumbnail-' + 'name')     
    newblob.upload_from_string(newimage.make_blob())
    # return "Successfully executed"

    try:
        data = s3.put_object(
            Body=newimage.make_blob(),
            Bucket="hirudinee0508",
            Key="fromGCP"
        )
        
        """
        data = {
            "ETag": "\"6805f2cfc46c0f04559748bb039d69ae\"",
            "VersionId": "pSKidl4pHBiNwukdbcPXAIs.sshFFOc0"
        }
        """
    except BaseException as e:
        print("error message"+e)
    
