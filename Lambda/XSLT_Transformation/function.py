#This code will transform JSON to JSON using XSLT Transformation

import lxml.etree as ET
import boto3
import requests
import json

def lambda_handler(event, context):

    inputdata = event["data"]
    #marutiin = event
    data = inputdata.split("~~")

    template= "<root>"

    s31 = boto3.resource('s3')
    s3 = boto3.client('s3')

   #Reading of files, the files can be anywhere, I have kept it in S3, you can store it locally and simply give the local path 
    data1 = s3.get_object(Bucket='<bucket_name>', Key='<object_name>')
    contents1 = data1['Body'].read()

    '''2 files are involved, one .txt file and another .xsl file,both have been provided in the repo
    '''

    data2 = s3.get_object(Bucket='<bucket_name>', Key='<object_name>')
    contents2 = data2['Body'].read()


    keyarray = contents1.split(",")
    #print(keyarray)
    for indx,val in enumerate(keyarray):
     template = template+"<"+keyarray[indx]+">"+data[indx]+"</"+keyarray[indx]+">"
    template = template+"<actualdata>"+inputdata+"</actualdata></root>"
    print(template)
    tree = ET.fromstring(template)
    xmldata = ET.ElementTree(tree)
    xslt = ET.fromstring(contents2)
    transform = ET.XSLT(xslt)
    res = str(transform(xmldata))
    if event["key1"] == "HyundaiOem":
        url = 'https://2y8llsvxb2.execute-api.ap-south-1.amazonaws.com/prod/'
	payload = res
	print(payload)
	print(type(payload))
	headers = {'Content-Type': "application/json"}
        response = requests.post(url, data = payload, headers = headers)
       	print(response)
	print(response.text)
	print(type(response.text))

