# MOI Atomic Pipeline API

## Overview

The MOI Atomic Pipeline API is an asynchronous file-processing pipeline that supports parsing, analysis, and other operations on uploaded files. It is asynchronous: submitting a job returns a `job_id` that you use later to query results.

### API list

This document covers the following endpoints:

| API | Method | Endpoint | Purpose |
|---|---|---|---|
| Submit a file-processing job | POST | `/v1/genai/pipeline` | Submit files for processing — supports remote URLs, local uploads, or a mix of both |
| Get job status | GET | `/v1/genai/jobs/{job_id}` | Query a submitted job's status and per-file detail |
| Download job results | GET | `/byoa/api/v1/explore/volumes/any/files/{file_id}/raws` | Download the processed result archive (ZIP) |

---

## Submit a File-Processing Job

### Basics

- **Endpoint:** `https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline`
- **Method:** `POST`
- **Request format:**
  - `application/json` — for remote file URLs
  - `multipart/form-data` — for local file uploads
- **Response format:** `application/json`

### Submission modes

The endpoint supports three flexible submission modes:

**Mode 1: public file URLs**

- Use `application/json`
- Pass URLs in the `file_urls` parameter
- For files already accessible on the public network

**Mode 2: local file uploads**

- Use `multipart/form-data`
- Upload local files as form parts
- Send both `payload` and `files` fields
- For files on your local disk

**Mode 3: hybrid**

- **Mix local files and remote URLs in a single request**
- Use `multipart/form-data`
- In `payload`, set both `file_urls` (remote) and `file_names` (local)
- Upload local file content as `files` parts alongside
- The API processes everything (remote + local) in one job and returns a single `job_id`

### Headers

| Name | Type | Required | Description |
|---|---|---|---|
| Content-Type | String | depends | Remote URL mode: `application/json`<br>Local upload mode: `multipart/form-data` |
| moi-key | String | yes | API key for authentication |

**Examples:**

Remote URL mode:

```
Content-Type: application/json
moi-key: YOUR-MOI-KEY
```

Local upload mode:

```
moi-key: YOUR-MOI-KEY
```

Note: when using `-F`, curl sets `Content-Type: multipart/form-data` for you.

### Request parameters

**Mode 1: remote file URLs**

Send a JSON body directly:

| Name | Type | Required | Description |
|---|---|---|---|
| file_urls | Array[String] | yes | URL list of files to process; HTTP/HTTPS supported |
| file_names | Array[String] | no | Keep as empty array `[]` |
| meta | Array | no | Metadata for extra processing parameters or identifiers |
| steps | Array[Object] | yes | Processing-step configuration; defines the operations applied to the files |
| steps[].node | String | yes | Processing-node name, e.g. `ParseNode` |
| steps[].parameters | Object | yes | Per-node configuration; pass `{}` for defaults |

**Mode 2: local file uploads**

Use `multipart/form-data` with these fields:

| Name | Type | Required | Description |
|---|---|---|---|
| payload | String | yes | JSON string with the configuration |
| payload.file_names | Array[String] | yes | Names of the uploaded files; must match the actual upload field names |
| payload.meta | Array | no | Metadata |
| payload.steps | Array[Object] | yes | Processing-step configuration |
| files | File | yes | Actual file content; multiple files are supported |

**Notes:**

- Pick one of the modes
- The `steps` array defines the pipeline; **steps run in order**
- For local uploads, names in `file_names` must match the names used in the `files` parts
- Nodes have ordering constraints — they must appear in the correct order

### Processing nodes

**Available nodes:**

| Node | Purpose | Input | Output |
|---|---|---|---|
| ParseNode | Parsing | Raw file | Structured data (text, tables, images) |
| ChunkNode | Chunking | Output of ParseNode | Text chunks |
| EmbedNode | Embedding | Output of ChunkNode | Vector embeddings |
| ExtractNode | Extraction | Raw file or another node's output | Targeted extraction |

**Allowed combinations** (must follow this order):

**1. Parse only**

```json
"steps": [
    {"node": "ParseNode", "parameters": {}}
]
```

Use case: parse a file to extract text, tables, and images.

**2. Parse + chunk**

```json
"steps": [
    {"node": "ParseNode", "parameters": {}},
    {"node": "ChunkNode", "parameters": {}}
]
```

Use case: parse a file then split the content into chunks for downstream processing.

**3. Parse + chunk + embed**

```json
"steps": [
    {"node": "ParseNode", "parameters": {}},
    {"node": "ChunkNode", "parameters": {}},
    {"node": "EmbedNode", "parameters": {}}
]
```

Use case: full document-vectorization pipeline, suitable for semantic search.

**4. Parse + chunk + embed + extract**

```json
"steps": [
    {"node": "ParseNode", "parameters": {}},
    {"node": "ChunkNode", "parameters": {}},
    {"node": "EmbedNode", "parameters": {}},
    {"node": "ExtractNode", "parameters": {}}
]
```

Use case: parse, vectorize, and pull out targeted information — full-fat document processing.

**5. Extract only**

```json
"steps": [
    {"node": "ExtractNode", "parameters": {}}
]
```

Use case: pull specific information directly out of a file without going through parsing.

**Per-node parameters:**

Each node accepts a `parameters` object to customize its behavior:

```json
{
    "node": "NodeName",
    "parameters": {
        // Node-specific parameters (optional)
        // For defaults, pass an empty object {}
    }
}
```

**Notes:**

- If you do not need custom behavior, pass `{}`
- Specific parameter sets vary per node — consult the API provider for details
- Different nodes accept different parameter keys

### Request examples

**Example 1: remote file URLs**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR-MOI-KEY" \
  -d '{
    "file_urls": [
        "http://www.pdf995.com/samples/pdf.pdf",
        "https://example.com/document.pdf"
    ],
    "file_names": [],
    "meta": [],
    "steps": [
        {
            "node": "ParseNode",
            "parameters": {}
        }
    ]
}'
```

**Notes:**

- `-H "Content-Type: application/json"` declares JSON mode
- `-d` carries the JSON body
- `file_urls` may contain multiple URLs
- `file_names` is an empty array
- The API processes all files and returns a single `job_id`

**Successful response:**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "job_id": "b55093a7-ff3c-42ca-a4fe-c4e72074e046"
    },
    "request_id": "969935d0-363e-4451-a5e3-f71f1d20101e"
}
```

**Example 2: upload local files**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "moi-key: YOUR-MOI-KEY" \
  -F "files=@/path/to/doc1.pdf" \
  -F "files=@/path/to/doc2.pdf" \
  -F 'payload={"file_names": ["doc1.pdf", "doc2.pdf"], "steps": [{"node": "ParseNode", "parameters": {}}]}'
```

**Notes:**

- `-F` selects multipart/form-data (no Content-Type header needed)
- Repeat `-F "files=@<path>"` for each file
- `files=@<path>` reads the file from disk; the `@` prefix is required
- All file fields use the same name `files`
- `payload` is a JSON string with the configuration
- The order of `file_names` should match the upload order
- Note: `files` parts go before `payload`

**Successful response:**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "job_id": "cd072050-ce02-406b-8f28-595f2c86eaaa"
    },
    "request_id": "b6528fde-ebc3-461b-8015-1b7b97ec9c82"
}
```

**Example 3: hybrid (local + remote)**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "moi-key: YOUR-MOI-KEY" \
  -F "files=@local-report.pdf" \
  -F 'payload={"file_urls": ["http://www.pdf995.com/samples/pdf.pdf"], "file_names": ["local-report.pdf"], "steps": [{"node": "ParseNode", "parameters": {}}]}'
```

**Notes:**

- ✅ **Local files and remote URLs in a single request**
- `file_urls` carries the remote files
- `file_names` carries the local file names
- `files` parts upload the local content
- The API processes all files (local + remote) under a single `job_id`

**Successful response:**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "job_id": "322fe48f-698d-4fbb-8851-1a2d9f8031ec"
    },
    "request_id": "ec636405-82ce-4331-902b-6810a83d17f0"
}
```

**Example 4: parse + chunk**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{
    "file_urls": ["http://example.com/document.pdf"],
    "file_names": [],
    "steps": [
        {"node": "ParseNode", "parameters": {}},
        {"node": "ChunkNode", "parameters": {}}
    ]
  }'
```

**Notes:**

- Parse first, then split into chunks
- For pipelines that process the document segment by segment

**Example 5: full vectorization pipeline**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{
    "file_urls": ["http://example.com/document.pdf"],
    "file_names": [],
    "steps": [
        {"node": "ParseNode", "parameters": {}},
        {"node": "ChunkNode", "parameters": {}},
        {"node": "EmbedNode", "parameters": {}}
    ]
  }'
```

**Notes:**

- Parse → chunk → embed
- Useful for semantic-search indexes and RAG systems
- Embeddings are ready for similarity search

**Example 6: full pipeline**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{
    "file_urls": ["http://example.com/document.pdf"],
    "file_names": [],
    "steps": [
        {"node": "ParseNode", "parameters": {}},
        {"node": "ChunkNode", "parameters": {}},
        {"node": "EmbedNode", "parameters": {}},
        {"node": "ExtractNode", "parameters": {}}
    ]
  }'
```

**Notes:**

- Parse → chunk → embed → extract
- The complete document-processing pipeline
- For workloads that need exhaustive document analysis

**Example 7: extract only**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{
    "file_urls": ["http://example.com/document.pdf"],
    "file_names": [],
    "steps": [
        {"node": "ExtractNode", "parameters": {}}
    ]
  }'
```

**Notes:**

- Extract specific fields directly from the file
- Skips parsing
- Best when you only need a small structured payload

### Response parameters

**Successful response:**

| Name | Type | Description |
|---|---|---|
| code | String | Status code; `OK` on success |
| msg | String | Status message; `OK` on success |
| data | Object | Response payload |
| data.job_id | String | Job ID — use it to query status and results |
| request_id | String | Unique request id for trace/debug |

**Successful response example:**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "job_id": "c66f4354-6833-4c75-8d34-d630024e5254"
    },
    "request_id": "d16e0fc2-50dd-4928-9eac-d55f88e0160c"
}
```

**Error response:**

```json
{
    "code": "ERROR_CODE",
    "msg": "Description of the error",
    "data": null,
    "request_id": "request id"
}
```

---

## Get Job Status

### Basics

- **Endpoint:** `https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/jobs/{job_id}`
- **Method:** `GET`
- **Request format:** URL path parameter
- **Response format:** `application/json`

### Headers

| Name | Type | Required | Description |
|---|---|---|---|
| moi-key | String | yes | API key for authentication |

### Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| job_id | String | yes | Job ID returned by the submission API |

### Response parameters

**Successful response:**

| Name | Type | Description |
|---|---|---|
| code | String | Status code; `OK` on success |
| msg | String | Status message; `OK` on success |
| data | Object | Response payload |
| data.status | String | Overall job status: `pending`, `processing`, `completed`, `failed` |
| data.files | Array[Object] | Per-file processing detail |
| data.files[].file_id | String | Unique file identifier |
| data.files[].file_name | String | File name |
| data.files[].file_type | Integer | File type code |
| data.files[].file_status | String | Per-file status: `pending`, `processing`, `completed`, `failed` |
| data.files[].error_message | String | Error message; empty string on success |
| data.files[].start_time | String | When processing started |
| data.files[].end_time | String | When processing finished |
| request_id | String | Unique request id |

### Request example

**Example: query job status**

```bash
curl -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/jobs/322fe48f-698d-4fbb-8851-1a2d9f8031ec" \
  -H "moi-key: YOUR-MOI-KEY"
```

**Notes:**

- HTTP `GET`
- `job_id` is part of the URL path
- Only the `moi-key` header is required

### Response examples

**Example 1: job completed**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "status": "completed",
        "files": [
            {
                "file_id": "019ad8c4-cf7e-75ca-afa1-5bd971ff9ed9",
                "file_name": "report.pdf",
                "file_type": 2,
                "file_status": "completed",
                "error_message": "",
                "start_time": "2025-12-01T07:16:11.000000+0000",
                "end_time": "2025-12-01T07:16:38.000000+0000"
            }
        ]
    },
    "request_id": "2934576f-246e-46cf-93d1-79a95fd52251"
}
```

**Example 2: multi-file job completed**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "status": "completed",
        "files": [
            {
                "file_id": "019ad8cb-3861-795c-99a6-03bdc37215ee",
                "file_name": "report.pdf",
                "file_type": 2,
                "file_status": "completed",
                "error_message": "",
                "start_time": "2025-12-01T07:23:38.000000+0000",
                "end_time": "2025-12-01T07:24:40.000000+0000"
            },
            {
                "file_id": "019ad8cb-3861-7963-8fa5-e2e6b66a265c",
                "file_name": "pdf.pdf",
                "file_type": 2,
                "file_status": "completed",
                "error_message": "",
                "start_time": "2025-12-01T07:23:39.000000+0000",
                "end_time": "2025-12-01T07:25:38.000000+0000"
            }
        ]
    },
    "request_id": "74983c96-98db-4e13-9d51-aee91dfcd163"
}
```

**Notes:**

- A hybrid submission contains both files: a local upload and a remote URL
- Each file carries its own `file_id`, status, and timing fields
- In this example both files were processed successfully

### Status semantics

**Overall job status:**

| Status | Meaning |
|---|---|
| pending | Submitted, waiting for processing |
| processing | Job is in progress |
| completed | All files completed |
| failed | Job failed |

**Per-file status:**

| Status | Meaning |
|---|---|
| pending | File waiting for processing |
| processing | File is being processed |
| completed | File processed successfully |
| failed | File processing failed; check `error_message` for the reason |

### Notes

1. **Polling interval:** poll every 3–5 seconds; avoid faster polling
2. **Processing time:**
   - Small files (<1MB) typically take seconds to a minute
   - Large files may take several minutes
   - Time depends on file size and complexity
3. **Error handling:** if `file_status` is `failed`, inspect `error_message` for the cause
4. **Time format:** all timestamps are UTC, formatted as `YYYY-MM-DDTHH:MM:SS.ffffff+0000`
5. **File order:** the `files` array preserves the submission order

### End-to-end example

```bash
# Step 1: submit a job
JOB_ID=$(curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{"file_urls": ["http://example.com/file.pdf"], "file_names": [], "steps": [{"node": "ParseNode", "parameters": {}}]}' \
  | jq -r '.data.job_id')

echo "Job ID: $JOB_ID"

# Step 2: wait a few seconds
sleep 5

# Step 3: query status
curl -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/jobs/$JOB_ID" \
  -H "moi-key: YOUR_API_KEY" \
  | jq '.'

# Step 4: decide based on status whether to keep polling
# - "completed": done
# - "processing": wait and query again
```

---

## Download Job Results

### Basics

- **Endpoint:** `https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/any/files/{file_id}/raws`
- **Method:** `GET`
- **Request format:** URL path parameter
- **Response format:** `application/zip`

### Headers

| Name | Type | Required | Description |
|---|---|---|---|
| Content-Type | String | recommended | `application/json` |
| moi-key | String | yes | API key for authentication |

### Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| file_id | String | yes | File ID from the `data.files[].file_id` field of the status API |

### Response

**Successful response:**

A **ZIP archive** containing all processing artifacts for the file.

**Archive layout:**

```
{file_name}-{file_id}/
├── {file_name}_parse.json         # Structured parse output
├── {file_name}.md                 # Extracted text in Markdown
├── tables/                        # Extracted tables (HTML)
│   ├── {table_id_1}.html
│   ├── {table_id_2}.html
│   └── ...
└── images/                        # Extracted images
    ├── {image_hash_1}.jpg
    ├── {image_hash_2}.jpg
    └── ...
```

**Files explained:**

| File / directory | Description |
|---|---|
| `{file_name}_parse.json` | Structured parse output; the full parsed document |
| `{file_name}.md` | Extracted text in Markdown — easy to read |
| `tables/*.html` | Extracted tables; one HTML file per table |
| `images/*.jpg` | Extracted images, named by content hash |

### Request examples

**Example 1: download the result**

```bash
curl -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/any/files/019ad8c4-cf7e-75ca-afa1-5bd971ff9ed9/raws" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR-MOI-KEY" \
  -o result.zip
```

**Notes:**

- `-o result.zip` saves the response as a ZIP file
- `file_id` comes from the status API response
- Unzip after download to inspect the contents

**Example 2: download and unzip**

```bash
# 1. Download
curl -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/any/files/019ad8c4-cf7e-75ca-afa1-5bd971ff9ed9/raws" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -o result.zip

# 2. Unzip
unzip result.zip

# 3. List the contents
ls -R
```

**Example 3: list ZIP contents without extracting**

```bash
curl -s -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/any/files/019ad8c4-cf7e-75ca-afa1-5bd971ff9ed9/raws" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -o result.zip && unzip -l result.zip
```

### Response example

**ZIP contents listing:**

```
Archive:  result.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     4463  12-01-2025 07:37   report.pdf-019ad8cb-.../report.pdf_parse.json
      940  12-01-2025 07:37   report.pdf-019ad8cb-.../tables/60d46443-0cec-4556-bf7d-bbff5812f9f5.html
      784  12-01-2025 07:37   report.pdf-019ad8cb-.../tables/3fef6f19-af8c-4791-b18f-a2747af88fa0.html
     3222  12-01-2025 07:37   report.pdf-019ad8cb-.../report.pdf.md
    33287  12-01-2025 07:37   report.pdf-019ad8cb-.../images/21ec307c62a48eecbc5f24cedd92eee95706024ab5f041cd17a463e78c377b2f.jpg
    38704  12-01-2025 07:37   report.pdf-019ad8cb-.../images/d0be52c9d88f4fe0f7a092863de5679e624a4529552fb863f0d1cdd5ff4fd7cc.jpg
    44015  12-01-2025 07:37   report.pdf-019ad8cb-.../images/de217bbf2728e9979cf88d0fc7a81ae5adb5695a329a9ad1863eb079dfd22c22.jpg
---------                     -------
   125415                     7 files
```

**Extracted layout:**

```
report.pdf-019ad8cb-3861-795c-99a6-03bdc37215ee/
├── report.pdf_parse.json  (4.4 KB)
├── report.pdf.md          (3.2 KB)
├── tables/
│   ├── 60d46443-0cec-4556-bf7d-bbff5812f9f5.html  (940 B)
│   └── 3fef6f19-af8c-4791-b18f-a2747af88fa0.html  (784 B)
└── images/
    ├── 21ec307c62a48eecbc5f24cedd92eee95706024ab5f041cd17a463e78c377b2f.jpg  (33 KB)
    ├── d0be52c9d88f4fe0f7a092863de5679e624a4529552fb863f0d1cdd5ff4fd7cc.jpg  (38 KB)
    └── de217bbf2728e9979cf88d0fc7a81ae5adb5695a329a9ad1863eb079dfd22c22.jpg  (44 KB)
```

### Notes

1. **`file_id` source:** call the status API first to obtain `file_id`
2. **Job state:** wait until job status is `completed` before fetching the archive
3. **Archive size:** depends on the source file; archives may include many images
4. **Completeness:** the archive contains every output from the ParseNode pipeline
5. **Image naming:** images use a content-hash file name to guarantee uniqueness
6. **Save location:** use `-o` to choose the path and file name
7. **Multi-file jobs:** if a job processed multiple files, fetch each archive with its own `file_id`
