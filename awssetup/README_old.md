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

## Create and Configure a VPC

Login with your admin account you just created.

1. Go to VPC.
2. Click "Your VPCs".
3. Click "Create VPC".
4. Choose the radio button "VPC and more".
5. Enter a name for name tag auto-generation.
6. Click other things according to your preference, or simply go to the next step.
7. Click "Create VPC".

After a while, the VPC is created. Then create an endpoint for Bedrock runtimes.

1. Click "Endpoints".
2. Enter a name tag for the endpoint.
3. Choose the radio button "com.amazonaws.us-east-1.bedrock-runtime".
4. In the select box under VPC, choose the VPC you just created.
5. Choose one private subnets.
6. Choose security group that is available.
7. Click "Create endpoint".

## Create EFS

First create the file system.

1. Go to EFS. Click "File systems". Then click "Create file system".
2. Give a name to the file system. And choose the VPC you created. Click "Create".

Then create the access points.

1. Click "Access points". Click "Create access point".
2. Choose the EFS file system you just created.
3. Give it a name.
4. Set the root directory path to be "/lambda". 
5. Under POSIX user, set User ID to be "1001", Group ID to be "1001", Secondaruy group IDs to be "0".
6. Under Root directory creation permissions, set Owner user ID to be "1001", Owner Group ID to be "1001", and Permissions to be "777".
7. Click "Create access point".

## Create an EC2 instance 

Now we create an EC2 instance for file transfer. 

1. Go to EC2. 
2. Click "Instances". Click "Launch instances".
3. Give a name. Choose "Amazon Linux"... any free tier would work. Use "t2.micro".
4. Create new key pair if there is none or you want a new one. Otherwise, choose an existing key pair.
5. Use existing security group.
6. In Network Settings, set the VPC to be the one you just created.
7. Remember to add security groups for SSH, HTTP, HTTPS, and set source to be "0.0.0.0/0". 
8. Enable "Auti-assign public IP". Select both default security groups. 
9. Set storage to be 64GiB. 
10. In Storage (volumes), click "Advanced". Click "Show Details" in File systems 
11. Click the radio button "EFS". Choose the EFS you just created. Set mount point to be "/mnt/efs/fs1". 
12. Click "Launch instance".

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

## Creating Lambda function for deplying database 

1. Go to AWS Lambda. If it is the first time, click "Create a function".
2. Choose radio button "Author from scratch". Put a function name.
3. Choose Python 3.x to be the runtime.