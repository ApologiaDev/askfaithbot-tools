# Setting Up the Project in AWS

## Create your admin account

1. Login the root account.
2. Go to "IAM".
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