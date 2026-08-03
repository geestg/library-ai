#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BU
#
# MVP Demo Dataset Validation
#
# MVP SAFE
# ==============================================================================

#
# Validate:
#
# Repository Dataset
#        |
#        v
# PDF Repository
#        |
#        v
# Global Metadata Dataset
#        |
#        v
# Abstract Metadata
#        |
#        v
# Chunk Dataset
#        |
#        v
# Knowledge Dataset
#
# Tidak melakukan:
# - migration
# - cleanup
# - restart service
# - delete data
# - exit
# - return
#
# Terminal remains open
# ==============================================================================


ROOT="/workspace/delbot"

REPOSITORY_DATA="$ROOT/delbot_platform/repository_data"

METADATA_FILE="$REPOSITORY_DATA/metadata/skripsi_dataset.json"

OUTPUT="$REPOSITORY_DATA/mapping/mvp_demo_dataset_validation.json"


echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.1BU Demo Dataset Validation"
echo "======================================================================"


python3 <<PYTHON

import os
import json
from datetime import datetime, timezone


root = "/workspace/delbot"

repository_data = os.path.join(
    root,
    "delbot_platform",
    "repository_data"
)


metadata_file = os.path.join(
    repository_data,
    "metadata",
    "skripsi_dataset.json"
)


checks = {}


checks["repository_data"] = os.path.exists(repository_data)

checks["metadata_directory"] = os.path.exists(
    os.path.dirname(metadata_file)
)


checks["global_metadata_dataset"] = os.path.exists(
    metadata_file
)


pdf_count = 0
chunk_count = 0
embedding_count = 0


if os.path.exists(repository_data):

    for current_root, dirs, files in os.walk(repository_data):

        for file in files:

            lower = file.lower()

            if lower.endswith(".pdf"):
                pdf_count += 1

            elif lower == "chunks.json":
                chunk_count += 1

            elif "embedding" in lower:
                embedding_count += 1



metadata_records = 0
abstract_available = False


if os.path.exists(metadata_file):

    try:

        with open(
            metadata_file,
            "r",
            encoding="utf-8"
        ) as f:

            metadata = json.load(f)


        if isinstance(metadata, list):

            metadata_records = len(metadata)


            for item in metadata:

                if isinstance(item, dict):

                    if item.get("abstract"):

                        abstract_available = True
                        break


        elif isinstance(metadata, dict):

            metadata_records = 1


            if metadata.get("abstract"):

                abstract_available = True


    except Exception:

        metadata_records = 0



checks["pdf_repository_available"] = pdf_count > 0

checks["metadata_record_available"] = metadata_records > 0

checks["abstract_metadata_available"] = abstract_available

checks["chunk_dataset_available"] = chunk_count > 0

checks["embedding_dataset_available"] = embedding_count > 0



flow = {

    "repository_ready":
        checks["repository_data"],

    "pdf_ready":
        checks["pdf_repository_available"],

    "academic_metadata_ready":
        checks["global_metadata_dataset"],

    "abstract_information_ready":
        checks["abstract_metadata_available"],

    "chunk_ready":
        checks["chunk_dataset_available"],

    "knowledge_ready":
        checks["embedding_dataset_available"]

}



result = {

    "timestamp":
        datetime.now(timezone.utc).isoformat(),

    "project":
        "DELBot MVP",

    "stage":
        "PR-5.1BU",

    "checks":
        checks,

    "dataset_statistics":
        {

            "pdf_count":
                pdf_count,

            "metadata_records":
                metadata_records,

            "abstract_available":
                abstract_available,

            "chunk_count":
                chunk_count,

            "embedding_count":
                embedding_count

        },


    "flow":
        flow,


    "demo_readiness":
        {

            "repository_demo_ready":
                flow["repository_ready"],

            "literature_metadata_demo_ready":
                flow["academic_metadata_ready"],

            "abstract_search_demo_ready":
                flow["abstract_information_ready"],

            "semantic_search_demo_ready":
                flow["chunk_ready"],

            "knowledge_base_demo_ready":
                flow["knowledge_ready"]

        },


    "status":

        "READY_MVP_DEMO_DATASET"

        if all(checks.values())

        else

        "INCOMPLETE_MVP_DEMO_DATASET"

}



output = "/workspace/delbot/delbot_platform/repository_data/mapping/mvp_demo_dataset_validation.json"


os.makedirs(
    os.path.dirname(output),
    exist_ok=True
)


with open(
    output,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=2
    )


print(
    json.dumps(
        result,
        indent=2
    )
)


PYTHON


echo
echo "======================================================================"
echo "Generated"
echo "/workspace/delbot/delbot_platform/repository_data/mapping/mvp_demo_dataset_validation.json"
echo "======================================================================"


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"


python3 -m compileall \
/workspace/delbot/delbot_platform/repository \
/workspace/delbot/delbot_platform/documents \
/workspace/delbot/delbot_platform/document_intelligence \
/workspace/delbot/delbot_platform/knowledge \
/workspace/delbot/delbot_platform/gateway \
/workspace/delbot/delbot_platform/research



echo
echo "======================================================================"
echo "PR-5.1BU COMPLETE"
echo "======================================================================"


echo
echo "NEXT"

echo "READY_MVP_DEMO_DATASET -> lanjut PR-5.1BV MVP Live Query Validation"

echo "INCOMPLETE_MVP_DEMO_DATASET -> audit dataset"


echo
echo "Terminal remains open"

