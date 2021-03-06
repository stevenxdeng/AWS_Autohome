# AWS Autohome
Author: ***Hsien-wen "Steven" Deng***\
See my demo video [here](https://youtu.be/N7h2CPD9Ebs)

## Introduction
&nbsp;&nbsp;&nbsp;&nbsp;This is a Serverless solution of home automation with different types of IoT devices implemented in Amazon Web Services (AWS). In this case, two type of IoT devices are tested in this application, *light* and *Thermostat*. Users can interact with these devices through a client program. User can add, remove or switch a light, and set temperature for a thermostat.\
&nbsp;&nbsp;&nbsp;&nbsp;All the actions are taken place in AWS with a serverless architecture. As figure 1 shows, two DynamoDB databases (i.e. Device Database, Event Database) are deployed for devices and events. After the user making an action, the client program will deliver a message through Kinesis Data Stream (KDS) and trigger the Autohome Function. The Autohome function then updates both Device Database and Event Database, and publish a message using MQTT through AWS IoT Core. Devices subscribe to this MQTT topic can then act based on the message. In this case, there are no physical devices deployed, all the presentations only cover client side and cloud side. Nevertheless, physical devices connections are still possible as future extensions.\
\
There are two major components in this branch to help you build up Autohome:\
**Template**: The template includes a system of AWS services allows you to establish this application.\
**Client Program**: The client program is a Python script running to test the availability of your cloud application and interact with IoT devices.

![alt text](https://github.com/stevenxdeng/AWS_Autohome/blob/main/Autohome_Architecture.png?raw=true)\
Figure 1. Architecture review of Autohome

## Prerequisite
1. [Python 3.8](https://www.python.org/downloads/)
2. [AWS Account](https://aws.amazon.com/)\
   *AWS Educate may not be eligible due to lack of permission configuring CLI*
3. AWS User Credential 
   1) From AWS Console go to **IAM**
   2) Select to **users**
   3) Click **Add user**
   4) Select **Programmatic access** for the AWS access type to generate an access key ID and secret access key for use with the AWS API, CLI, SDK, and other development tools
   5) Select the created user and select **Security Credentials** tab
   6) Click **Create access key** and copy the access key ID and secret access key after a new user is created\
*For more details, please check: [AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)*
4. AWS CLI
   1) Download [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.htm) and install 
   2) Open CMD (Windows) or Terminal (Linux): `aws configure`
   3) Input **access key ID** and **secret access key** copied from 3
   4) Configure region (default "us-east-1")
   5) Configure output (default "json")\
*For more details, please check: [AWS CLI Configuration Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)*
   
## Build-up Application
1. From AWS Console go to **CloudFormation**
2. Click **Create stack**
3. Select **Upload a template file** and upload *Autohome_Template.json*
4. Input a name and click **Create stack**\
   *Check you AWS region to be US-EAST-1 (N. Virginia)*
## Test Application
1. Install boto3: `python -m pip install boto3`
2. Run *Autohome_Client.py*: `python Autohome_Client.py`(Linux / OS X)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`py Autohome_Client.py`(Windows)
3. Check the changes you applied
    1) Through **Client Program**: Select *4) See Device Database* or *5) See Event Database*
    2) Through **AWS**: You can use both *DynamoDB* and *IoT Core*
        1. **DynamoDB**
            1. From AWS Console go to **DynamoDB**
            2. Select **Tables**
            3. Enter **Autohome_collection** (*Device Database*) or **Autohome_logs** (*Event Database*)
            4. Select **items** to find applied changes
        2. **IoT Core**
            1. From AWS Console go to **IoT Core**
            2. Select **Test** then choose **MQTT test client**
            3. Select **Subscribe to a topic**
            4. In *Topic filter*, input `/autohome/topic`
            5. Click the **Subsribe** button
## Destroy Application
1. From AWS Console go to **CloudFormation**
2. Choose target stack
3. Delete target stack

## License
[**MIT**](https://github.com/stevenxdeng/AWS_Autohome/blob/main/LICENSE)
