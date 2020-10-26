# Copyright 2020. A. J. S.
# License: GPLv3

# below code for AWS Lambda

# Copyright 2013. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# boto3 offers two different styles of API - Resource API (high-level) and
# Client API (low-level). Client API maps directly to the underlying RPC-style
# service operations (put_object, delete_object, etc.). Resource API provides
# an object-oriented abstraction on top (object.delete(), object.put()).
#
# While Resource APIs may help simplify your code and feel more intuitive to
# some, others may prefer the explicitness and control over network calls
# offered by Client APIs. For new AWS customers, we recommend getting started
# with Resource APIs, if available for the service being used. At the time of
# writing they're available for Amazon EC2, Amazon S3, Amazon DynamoDB, Amazon
# SQS, Amazon SNS, AWS IAM, Amazon Glacier, AWS OpsWorks, AWS CloudFormation,
# and Amazon CloudWatch. This sample will show both styles.
#
# First, we'll start with Client API for Amazon S3. Let's instantiate a new
# client object. With no parameters or configuration, boto3 will look for
# access keys in these places:
#
#    1. Environment variables (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
#    2. Credentials file (~/.aws/credentials or
#         C:\Users\USER_NAME\.aws\credentials)
#    3. AWS IAM role for Amazon EC2 instance
#       (http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)

# Import the SDK
import boto3
import uuid
import urllib
import requests
import sys
import re
from time import sleep
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
import random
import os
import json
import time
import urllib
from lxml import etree
import hashlib
from random import randrange
from os.path import basename
import ast
from urllib.parse import unquote
from urllib.request import urlopen
import urllib.parse as urlparse
from urllib.parse import parse_qs
import unidecode
import pandas as pd
from os.path import basename
import urllib.request

FLICKR_URL = 'https://www.flickr.com/search/'
GLOBAL_URL = 'https://www.equibase.com/static/foreign/entry/index.html'


class FlickrObject(object):
    def __init__(self, search_term):
        self.search_term = search_term
        self.encoded = urllib.parse.quote(self.search_term, safe='')
        self.landing = FLICKR_URL+'?text='+self.encoded+'&view_all=1&license=4%2C5%2C9%2C10'

        self.r = requests.get(self.landing, timeout=5)

        self.soup = BeautifulSoup(self.r.content, features='lxml')
        # self.image_div = self.soup.select('div.main.search-photos-results')
        # self.images_links = self.image_div[0].select('div.photo-list-photo-view > a')


        self.script_loc = self.soup.select('script.modelExport')[0]
        # https://www.flickr.com/photos/cools/28181645182/


        self.json = re.search("(\{\"legend\"\:)(.+)(\n)", str(self.soup.html)).group(0)
        self.json = json.loads(self.json.strip()[:-1])

        self.df = pd.json_normalize(self.json['main']['search-photos-lite-models'][0]['photos']['_data'])
        
        
    def gather(self, count):
        self.count = count
        print('Fetching %s Photos'%self.count)
        for image_count in range(0, self.count):
            imageObj = self.images_links[image_count]

# turn off when read
TESTMODE = True


def main():
    if not TESTMODE:
        if len(sys.argv) < 4:
            print("Error: Missing arguments, e.g. flickr-unofficial-api.py 'California Fires' 'bucket_name' 8")
            exit(1)
        elif len(sys.argv) > 4:
            print("Error: Quote the search term 'like this'")
            exit(1)
        elif len(sys.argv) == 4:
            search_term = sys.argv[1]
            bucket_name = sys.argv[2]
            count_required = sys.argv[2]
        else:
            print("Shouldnt be here.")
            exit(1)
    else:
        search_term = 'California Fires'
        bucket_name = 'art-ideas'
        count_required = 5
        flickrObj = FlickrObject(search_term)
        # flickrObj.gather(count_required)
        s3client = boto3.client('s3')
        list_buckets_resp = s3client.list_buckets()
        for bucket in list_buckets_resp['Buckets']:
            if bucket['Name'] == bucket_name:
                print('(Bucket) --> {} - there since {}'.format(
                    bucket['Name'], bucket['CreationDate']))

        photo_list = flickrObj.df['sizes.l.url'].to_list()
        
        for photo_url in photo_list:
            if photo_url == 'nan':
                continue
            photo_url = 'https://'+photo_url[2:]
            object_key = basename(photo_url)
            urllib.request.urlretrieve(photo_url, object_key)
        

            print('Uploading some data to {} with key: {}'.format(
                bucket_name, object_key))
            s3client.put_object(Bucket=bucket_name, Key=object_key, Body=object_key)
            url = s3client.generate_presigned_url(
                'get_object', {'Bucket': bucket_name, 'Key': object_key}
            )
            print('\nTry this URL in your browser to download the object:')
            print(url)
        # First, create the service resource object
        s3resource = boto3.resource('s3')
        # Now, the bucket object
        bucket = s3resource.Bucket(bucket_name)
        # Then, the object object
        obj = bucket.Object(object_key)
        print('Bucket name: {}'.format(bucket.name))
        print('Object key: {}'.format(obj.key))
        print('Object content length: {}'.format(obj.content_length))
        print('Object body: {}'.format(obj.get()['Body'].read()))
        print('Object last modified: {}'.format(obj.last_modified))


if __name__ == '__main__':
    main()



# Using the client, you can generate a pre-signed URL that you can give
# others to securely share the object without making it publicly accessible.
# By default, the generated URL will expire and no longer function after one
# hour. You can change the expiration to be from 1 second to 604800 seconds
# (1 week).


# As we've seen in the create_bucket, list_buckets, and put_object methods,
# Client API requires you to explicitly specify all the input parameters for
# each operation. Most methods in the client class map to a single underlying
# API call to the AWS service - Amazon S3 in our case.
#
# Now that you got the hang of the Client API, let's take a look at Resouce
# API, which provides resource objects that further abstract out the over-the-
# network API calls.
# Here, we'll instantiate and use 'bucket' or 'object' objects.


# Buckets cannot be deleted unless they're empty. Let's keep using the
# Resource API to delete everything. Here, we'll utilize the collection
# 'objects' and its batch action 'delete'. Batch actions return a list
# of responses, because boto3 may have to take multiple actions iteratively to
# complete the action.

# Now that the bucket is empty, let's delete the bucket.



# For more details on what you can do with boto3 and Amazon S3, see the API
# reference page:
# https://boto3.readthedocs.org/en/latest/reference/services/s3.html






