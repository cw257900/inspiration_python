#!/usr/bin/env bash

# Chunking and embedding are optional.

export UNSTRUCTURED_API_KEY="YvJqMBMJbcnXPXpGctLS1G6IFa2uJQ"
export UNSTRUCTURED_API_URL="https://api.unstructuredapp.io/general/v0/general"
export LOCAL_FILE_INPUT_DIR=/Users/Connie/Desktop/connie/inspiration_python/PlugIns/data/
export LOCAL_FILE_OUTPUT_DIR=/Users/Connie/Desktop/connie/inspiration_python/PlugIns/example_outputs/

unstructured-ingest \
  local \
    --input-path $LOCAL_FILE_INPUT_DIR \
    --partition-by-api \
    --api-key $UNSTRUCTURED_API_KEY \
    --partition-endpoint $UNSTRUCTURED_API_URL \
    --strategy hi_res \
    --chunking-strategy by_title \
    --embedding-provider huggingface \
    --additional-partition-args="{\"split_pdf_page\":\"true\", \"split_pdf_allow_failed\":\"true\", \"split_pdf_concurrency_level\": 15}" \
  local \
    --output-dir $LOCAL_FILE_OUTPUT_DIR
