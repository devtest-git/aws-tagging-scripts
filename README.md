# AWS Resource Tagging Automation Toolkit

A collection of automation scripts and AWS Lambda functions to enforce consistent tagging across AWS resources such as EC2 instances and S3 buckets.

This project helps improve cost allocation, governance, and resource visibility by ensuring required tags are always present.

---

## 📦 Features

### EC2 Auto Tagging (Lambda - Python)

- Automatically tags EC2 instances based on Name pattern  
- Uses regex-based filtering for flexible matching  
- Runs in AWS Lambda (event-driven or scheduled)  
- Ensures required cost center tags are applied  

### S3 Bucket Tagging (Bash Script)

- Scans all S3 buckets in the AWS account  
- Adds missing `Name` tag automatically  
- Preserves existing tags  
- Uses AWS CLI + jq  

---

## 📁 Project Structure

```
aws-resource-tagging-automation/
│
├── ec2/
│   └── lambda_function.py
│
├── s3/
│   └── s3_bucket_tagger.sh
│
├── docs/
│   ├── ec2-tagging.md
│   ├── s3-tagging.md
│   └── architecture.md
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Requirements

### EC2 Lambda
- Python 3.9+
- boto3 (included in AWS Lambda runtime)

### S3 Script
- AWS CLI configured (`aws configure`)
- jq installed

---

## 🔐 IAM Permissions

### EC2 Lambda
- `ec2:DescribeInstances`
- `ec2:CreateTags`

### S3 Script
- `s3:ListAllMyBuckets`
- `s3:GetBucketTagging`
- `s3:PutBucketTagging`
- `s3:GetBucketLocation`

---

## 🚀 Usage

### Run S3 Tagging Script

```bash
bash s3/s3_bucket_tagger.sh
```

---

### Deploy EC2 Lambda

```bash
zip -r function.zip ec2/
```

Upload to AWS Lambda and configure environment variables.

---

## 🧠 How It Works

### EC2 Flow
- Lambda fetches EC2 instances  
- Filters by instance state  
- Matches Name tag using regex  
- Applies missing or incorrect tags  

### S3 Flow
- Lists all S3 buckets  
- Checks existing tags  
- Adds `Name` tag if missing  
- Preserves existing tag set  

---

## 🎯 Use Cases

- Cost allocation tagging enforcement  
- AWS resource governance  
- Compliance automation  
- Standardizing naming conventions  
- Reducing untagged resources  
```

---

## 🚀 Key takeaway

Markdown **always needs structure**:
- Blank lines between sections
- Proper `##` headings
- Bullet points (`-`)
- Code blocks (```)

---

If you want next step, I can also:
- make this README look **“GitHub trending project level”**
- add **badges (AWS, Python, Lambda, CI)**
- or create a **professional architecture diagram for it**
