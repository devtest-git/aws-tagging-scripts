#!/bin/bash
buckets=$(aws s3api list-buckets --query "Buckets[].Name" --output text) 
for bucket in $buckets; do
  region=$(aws s3api get-bucket-location --bucket "$bucket" --query "LocationConstraint" --output text 2>/dev/null)
  [[ "$region" == "None" || "$region" == "null" || -z "$region" ]] && region="us-east-1"
  tags_json=$(aws s3api get-bucket-tagging --bucket "$bucket" --region "$region" --output json 2>/dev/null)

  # If bucket has no tags → directly add Name tag

  if [ -z "$tags_json" ]; then
      aws s3api put-bucket-tagging \
        --bucket "$bucket" \
        --region "$region" \
        --tagging "{\"TagSet\":[{\"Key\":\"Name\",\"Value\":\"$bucket\"}]}"
      echo "Added Name tag → $bucket"
      continue
  fi
 
  # Check if Name tag already exists
  if echo "$tags_json" | jq -e '.TagSet[] | select(.Key=="Name")' >/dev/null; then
      continue
  fi
 
  # Append Name tag only for missing ones
  updated=$(echo "$tags_json" | jq ".TagSet += [{\"Key\":\"Name\",\"Value\":\"$bucket\"}]")
  aws s3api put-bucket-tagging \
    --bucket "$bucket" \
    --region "$region" \
    --tagging "{\"TagSet\":$(echo "$updated" | jq -c '.TagSet')}"
  echo "Added Name tag → $bucket"
done