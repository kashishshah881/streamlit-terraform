import streamlit as st
import os
import json
import boto3

s3 = boto3.client('s3')
bucket_name = 'kashishshah-streamlit-deploy'
def convert(df):
    z = { k[0]: k[1] for k in df }
    return z


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

st.title("Aws instance creator")
dict1 = []
instance_name  = st.text_input("Enter an instance name")
region_name = option = st.selectbox('Which Region Do You Want to Deploy Your EC2 Instance',('us-east-1', 'us-east-2', 'us-west-1','us-west-2'))
instance_type = st.selectbox("What type of instance would you want?",('t2.nano','t2.micro','t2.small','t2.medium','t2.large','t2.xlarge'))
no_of_tags = st.text_input("How many tags would you like to define?")
counter = 1
if no_of_tags:
    st.write("define Key=value")
    for tag in range(0,int(no_of_tags)):
        x = "tag "+str(counter)
        var1 = st.text_input(x)
        counter=counter+1
        value = var1.split("=")
        dict1.append(value)
        
submit = st.button("Submit!")
if submit:
    my_bar = st.progress(0)
    tag = convert(dict1)
    tag.update({'Name':instance_name})
    st.write("Job Submitted!")
    my_bar.progress(10)
    f = open("index.tf.py", "w")
    d2 = "Provider('aws',profile='default',region='" + region_name + "') \n"
    d3 = "Resource('aws_instance', 'streamlit',ami='ami-0c94855ba95c71c99',instance_type='" + instance_type + "',tags=" + str(tag) + ") \n"
    L = ["from terraformpy import Resource,Provider \n", d2 , d3] 
    f.writelines(L)
    f.close()
    my_bar.progress(20)
    st.write("file writing completed!... Running Execution") 
    os.system("terraformpy plan --out=tf.plan")
    my_bar.progress(40)
    st.write("Script Complete...Deploying Architecture!")
    os.system('terraform apply tf.plan')
    my_bar.progress(80)
    st.write("Saving your configuration to S3")
    response = upload_file('terraform.tfstate', bucket_name)
    response = upload_file('main.tf.json',bucket_name)
    os.remove('index.tf.py')
    os.remove('main.tf.json')
    os.remove('terraform.tfstate')
    os.remove('terraform.tfstate.backup')
    os.remove('tf.plan')
    my_bar.progress(100)
    st.write("Job Completed!")
    st.baloon()
    
