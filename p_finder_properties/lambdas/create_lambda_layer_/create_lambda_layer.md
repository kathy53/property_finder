# Creation of a lambda layer
The layers are used to aggregate packages or requirements of a given runtime
Here we are going to use lxml for Python 3.8

First try. 
Using a venv, but then an error rose
"`GLIBC_2.22' not found (required by..."
Solution: use an AWS image
1. Create a docker container based on an AWS docker image for a specific runtime. 

In this case the image was based on python3.8
https://hub.docker.com/r/amazon/aws-lambda-python

Here, the public.ecr.aws/lambda/python:3.8 image was used. 

But may be it should be amazon/aws-lambda-python

2. Install the requierements inside the container in a specific dir

the relative rute of the parent dir is python/lib/python3.8/site-packages/

3. Compress the python dir

    **Consult the instruc file for the above steps**

4. Load into the AWS layers section

5. If necessary, delete the Add the layer to the lambda function


Sources
https://docs.aws.amazon.com/lambda/latest/dg/packaging-layers.html
https://docs.aws.amazon.com/lambda/latest/dg/adding-layers.html
 
    