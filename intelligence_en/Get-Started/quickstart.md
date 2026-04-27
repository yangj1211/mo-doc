# Quickstart: Create a MatrixOne Intelligence Instance

This guide walks you through creating and using a database instance end-to-end.

## Step 1: Create a MatrixOne Intelligence Account

### 1. Sign up

- Visit the [MatrixOne Intelligence sign-up page](https://matrixorigin.cn/moi-signup).
- Fill in your registration details and click **Sign up**.

**Note:** the email address you provide becomes your MatrixOne Intelligence account.

### 2. Activate your account

After you click sign-up, an activation email is sent to the address you provided. Follow the link in the email to complete activation.

### 3. Log in

Once activated, the system redirects you to the login page. The first time you log in, you will see the GenAI workspace and MatrixOne instance picker — choose an instance to enter the instance management console. On subsequent logins, your last selection is remembered; switch the GenAI workspace from the instance management page if needed.

## Step 2: Create a Serverless Instance

### 1. Open the create-instance page

On the **Database Instances** page, click **+ Create Instance**.

### 2. Configure the instance

- **Cloud provider:** pick the public cloud and region closest to you.
- **Access control:** set the initial password for the `admin` user.
- **Network policy:** we recommend allowlisting specific IPs.
- **Instance name:** name it yourself, or accept the auto-generated one.

### 3. Finish creation

Click **Create Serverless Instance**. After a few seconds, when the instance status turns green, the instance is ready.

## Step 3: Connect to the Instance

### 1. Open the database management console

On the instance card, click **Connect**, then choose **Connect via cloud console** to open the login page.

### 2. Enter admin credentials

On the login page, enter:

- **Username:** `admin`
- **Password:** the admin password you set when creating the instance

`admin` is the default. To log in as a non-admin user, see [Log in to an instance](../Instance-Mgmt/login-instance.md).

## Run the Sample Data

### 1. Load the TPC-H sample dataset

- In the upper-right corner of the console, click **Import data**.
- Choose **Try sample data > TPC-H benchmark**.
- Click **Import TPC-H data** to finish loading.

### 2. Query the TPC-H dataset

- Open the **SQL Editor** from the left menu.
- Pick **mo_sample_data_tpch_sf1** in the database dropdown above the editor.
- In the **Quick Tips** panel under **Import data**, click **Try it** — this copies a sample query into the editor. Click **Run** to execute it.

You have now created a Serverless instance and run a query against the sample dataset. We hope this tutorial was helpful.

If you need more help, please continue browsing the docs or contact support.
