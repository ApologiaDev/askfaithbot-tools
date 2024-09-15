# Setting Up the Project in AWS

## Create your admin account

1. Login the root account.
2. Go to IAM.
3. Go to "Users", and click "Create user".
4. Type your username. Check "Provide user access to the AWS Management Console".
5. Choose "I want to create an IAM user" radio button.
6. Create whatever your password and other related settings.
7. Click "Next".
8. Choose radio button "Attach policies directly".
9. Check "AdministratorAccess".
10. Click "Next".
11. Click "Create user".
12. Click "Download .csv file". Save this file to a safe folder in your local computer.

On the other hand, do not forget to create the access key.

1. Go to IAM, and the click "Users".
2. Click on the account you just created.
3. Click "Create access key".
4. Choose radio button "Command Line Interface (CLI)". Check "I understand the above recommendation and want to proceed to create an access key." Click "Next".
5. Type a tag value that you understand. Click "Crete access key".
6. The access tokens and secrets is on the page. And click "Download .csv file" for your future reference (recommended). 

Then after that, whenever login to AWS for admin access, use this account.

## Create an EC2 instance 

Now we create an EC2 instance for file transfer. 

1. Go to EC2. 
2. Click "Instances". Click "Launch instances".
3. Give a name. Choose "Amazon Linux"... any free tier would work. Use "t2.micro".
4. Create new key pair if there is none or you want a new one. Otherwise, choose an existing key pair.
5. Use existing security group.
6. Remember to add security groups for SSH, HTTP, HTTPS, and set source to be "0.0.0.0/0".
7. Set storage to be 64GiB.
8. Click "Launch instance".

After doing this, the EC2 instance is running. If you are not using it,
then you can stop the instance without terminating it.
Whenever you need to start the instance, you can login with the 
downloaded PEM file using `ssh`, like:

```bazaar
ssh -i <path of the PEM file> ec2-user@<public IPv4 address>
```

## Installing Git and Docker in the EC2 instance

Start the EC2 instance if it is not running. And login 
to the instance using `ssh` using the command above.

1. Enter `sudo yum update` and press Enter.
2. Enter `sudo yum install -y git` and press Enter.
3. Enter `sudo yum install -y docker` and press Enter.

## Clone the Git repository to the EC2 instance

In the instance, create ny directory you desired. And at
your desired location, clone the repository by running

```bazaar
git clone https://github.com/ApologiaDev/askfaithbot-tools.git
```

The clone needs to be done once only. Any changes can be updated by 
pulling the repository by `git pull`.

And we need to start the Docker engine by running

```bazaar
sudo systemctl start docker
```

Remember to add the access tokens and key secrets by 
running `sudo aws configure`. They tokens and key secrets can
be found in the .CSV file downloaded when you created
your admin account.

## Create an Elastic Container Registry (ECR) repository

1. Go to Amazon Elastic Container Service.
2. Click "Amazon ECR". It might display a page if it is your first time. If so, click "Create repository".
3. Put the name (e.g., "askfaithbot-ecr").
4. Click "Create".

The repository needs to be created only once. However, it can be 
updated many times as long as you need to. To push the repository,
click on the repository, and click "View Push Commands". There are
four command lines. They are the commands you need to run in the 
subdirectory "askfaithbot-rag-lambda" of the Git repository you just 
cloned to the EC2 instance. Remember to add "sudo" to every line (and there 
should be two "sudo"'s for the first command).

## Create an IAM Role for the Lambda Function

1. Go to IAM. 
2. Click "Roles".
3. Click "Create role".
4. Click the radio button "AWS service".
5. In the drop down meny "Service or use case", choose "Lambda".
6. Click "Next".
7. Check the following Permissions policies: 
   - AmazonBedrockFullAccess
   - AmazonVPCCrossAccountNetworkInterfaceOperations
   - AWSLambdaBasicExecutionRole
8. CLick "Next".
9. Give a role name.
10. Click "Create role".

## Create the Lambda Function

1. Go to AWS Lambda. If it is your first time, click "Create a function". 
2. Click "Container image".
3. Put a function name.
4. Under "Container image URl", click "Browse images".
5. Select the image repository you created above. And click on the image you created. Click "Select image".
6. Click radio button "Use an existing role". Choose the IAM Role you just created above.
7. Click "Create function".

After the function is created,

1. Click the tab "Configuration", go to "General configuration". Click "Edit". Set:
   - Timeout: more than 5 minutes.
   - Memory: 3008 MB
   - Ephemeral storage: 4096 MB
2. Click "Save".
3. Click "Environment variables". Click "Edit". Set the following environment variables:
   - QDRANT_URL: URL of your QDRant repository.
   - QDRANT_API_KEY: the API key
   - GPT4ALLMODELPATH: `/tmp/gpt4all`
4. Click "Save".