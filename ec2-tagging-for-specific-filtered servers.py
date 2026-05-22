import os
import re
import logging
import boto3
from botocore.exceptions import ClientError

# Config via env vars
TAG_KEY = os.getenv("TAG_KEY", "NBHI-CostCenter-Application")
TAG_VALUE = os.getenv("TAG_VALUE", "DATABRICKS")
NAME_PATTERN = os.getenv("NAME_PATTERN", r"^workerenv-.*")  # regex, case-insensitive
TARGET_STATES = os.getenv("TARGET_STATES", "running,pending").split(",")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

name_regex = re.compile(NAME_PATTERN, re.IGNORECASE)

def get_tag_value(tags, key):
    if not tags:
        return None
    for t in tags:
        if t.get("Key") == key:
            return t.get("Value")
    return None

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

def tag_instances(ec2_client, instance_ids):
    # EC2 create_tags supports many resources; keep safe batch size (e.g., 100)
    for chunk in chunk_list(instance_ids, 100):
        try:
            ec2_client.create_tags(
                Resources=chunk,
                Tags=[{"Key": TAG_KEY, "Value": TAG_VALUE}]
            )
            logger.info("Tagged instances: %s", chunk)
        except ClientError as e:
            logger.exception("Failed to tag instances %s: %s", chunk, e)
            raise

def lambda_handler(event, context):
    ec2 = boto3.client("ec2")
    paginator = ec2.get_paginator("describe_instances")
    filters = [{"Name": "instance-state-name", "Values": TARGET_STATES}]

    to_tag = []
    try:
        for page in paginator.paginate(Filters=filters):
            for reservation in page.get("Reservations", []):
                for inst in reservation.get("Instances", []):
                    instance_id = inst.get("InstanceId")
                    tags = inst.get("Tags", []) or []
                    name_value = get_tag_value(tags, "Name") or ""
                    # Check Name pattern
                    if name_regex.match(name_value):
                        current_cost_value = get_tag_value(tags, TAG_KEY)
                        # Tag if missing or different
                        if current_cost_value != TAG_VALUE:
                            logger.info(
                                "Instance %s matched name '%s' and needs tag (current: %s).",
                                instance_id, name_value, current_cost_value
                            )
                            to_tag.append(instance_id)
                        else:
                            logger.debug("Instance %s already has correct tag.", instance_id)
        if to_tag:
            logger.info("Total instances to tag: %d", len(to_tag))
            tag_instances(ec2, to_tag)
            logger.info("Tagging completed for %d instances.", len(to_tag))  # optional confirmation

        else:
            logger.info("No instances requiring tagging found.")
    except ClientError as e:
        logger.exception("Error describing instances: %s", e)
        raise