##################################################
## FileName: ohmypys3.py
##################################################
## Author: RDinmore
## Date: 2020.06.27
## Purpose: functions to retrieve data from amazon s3
## Libs: pandas, matplotlib, boto3, io, cv2
## Path: Flask_UI/filestore
##################################################

import pandas as pd
import matplotlib.image as mpimg
import boto3
import io
import tempfile
import cv2
import appconfig as cfg
import sys
sys.path.append("..")
import os
from pathlib import Path

go = "lSX6"
ga = "BriF8"
to = "yQ6wF"
rs = "nN20BnSfLfx9C7NQ4a3bgv6+W8"


def video_list():
    dirname = Path(__file__).parents[1]
    rootdir = os.path.join(dirname, 'static/videos')
    videolist = os.listdir(rootdir)
    return videolist


client = boto3.client(
    's3',
    aws_access_key_id=cfg.s3["key_id"] ,
    aws_secret_access_key= go + ga + to + rs
)

session = boto3.Session(
    aws_access_key_id=cfg.s3["key_id"] ,
    aws_secret_access_key= go + ga + to + rs
)

# return all files in s3
def get_s3files():
    collectionTable = client.list_objects(Bucket=cfg.s3["bucket_name"])['Contents']
    collectionDf = pd.DataFrame(collectionTable)
    collectionDf = collectionDf[["Key"]]
    return collectionDf

# return file location where file name like
def get_s3objectList(filename):
    collectionDf = get_s3files()
    dfFiltered = collectionDf[collectionDf['Key'].str.contains(filename)]
    if len(dfFiltered) == 0:
        return "not found"

    return dfFiltered

# return file location where file name like
def get_s3object(filename):
    collectionDf = get_s3files()
    dfFiltered = collectionDf[collectionDf['Key'].str.contains(filename)]
    if len(dfFiltered) == 0:
        return "not found"
    fileLocation = dfFiltered["Key"].iloc[0]
    return fileLocation

def get_temps3file(filename):
    s3 = session.resource('s3', cfg.s3["region"])
    bucket = s3.Bucket(cfg.s3["bucket_name"])
    object = bucket.Object(filename)
    file_stream = io.BytesIO()
    object.download_fileobj(file_stream)
    tmp = tempfile.NamedTemporaryFile()
    img = ""

    with open(tmp.name, 'wb') as f:
        object.download_fileobj(f)
        img = mpimg.imread(tmp.name)

    return tmp.name

def get_cvimage(filename):
    s3 = session.resource('s3', cfg.s3["region"])
    bucket = s3.Bucket(cfg.s3["bucket_name"])
    object = bucket.Object(filename)
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'wb') as f:
        object.download_fileobj(f)
        img = cv2.imread(tmp.name)

    img={"image":img,"name":tmp.name}
    return img

def gettemp_cvimage(filename):
    img = cv2.imread(filename)
    return img

def get_cvvideo(filename):
    s3 = session.resource('s3', cfg.s3["region"])
    bucket = s3.Bucket(cfg.s3["bucket_name"])
    object = bucket.Object(filename)
    tmp = tempfile.NamedTemporaryFile()

    with open(tmp.name, 'wb') as f:
        object.download_fileobj(f)
        img = cv2.imread(tmp.name)

    img={"image":img,"name":tmp.name}
    return img