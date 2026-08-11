# Audio Transcription Pipeline

A simple Python-based audio transcription pipeline that accepts audio files, converts spoken language into text, and returns segment-level timestamps.

## Overview

The implementation uses a Whisper-based speech-to-text API. The assessment focuses on building the transcription pipeline rather than training a speech recognition model from scratch.

The pipeline consists of three main steps:
 
1. Validate and accept an audio file.
2. Transcribe spoken language into text.
3. Return the transcription with segment-level timestamps.

## Project Structure

```text
audio-transcription-pipeline/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
└── src/
    ├── upload.py
    ├── transcription.py
    └── timestamps.py
```

## Implementation

### Audio File Handling

`src/upload.py` validates that the audio file exists and supports common audio formats:

* WAV
* MP3
* M4A

### Speech-to-Text

`src/transcription.py` sends the audio file to the Whisper-based transcription API and returns the resulting text.

### Segment Timestamps

`src/timestamps.py` requests structured transcription output and returns each segment with:

* Start time
* End time
* Transcribed text

Example:

```json
{
  "text": "Hello, welcome to the meeting.",
  "segments": [
    {
      "start": 0.0,
      "end": 2.15,
      "text": "Hello, welcome to the meeting."
    }
  ]
}
```

## Design Decisions

### Speech-to-Text Provider

I selected a Whisper-based API because the assessment allows the use of a speech-to-text API and the primary focus is on engineering the pipeline rather than training a model.

The transcription logic is isolated in separate modules so that the provider can be replaced later without changing the overall pipeline design.

### Audio Formats

The input layer validates the file extension before processing.

For a production implementation, I would additionally validate the MIME type, file size, codec, duration, and audio integrity. If a required format is not supported by the transcription provider, I would normalize the audio using FFmpeg.

### Long Audio Files

For long recordings, I would avoid keeping the entire transcription process inside a synchronous HTTP request.

For a production implementation, I would store the audio in object storage and create an asynchronous transcription job. Long recordings could be divided into manageable chunks with a small overlap between chunks to avoid losing words at boundaries. The resulting segments would then be merged while preserving their original timestamps.

### Concurrent Uploads

For concurrent uploads, I would use asynchronous job processing with a queue such as BullMQ, Amazon SQS, or RabbitMQ.

Workers could process transcription jobs concurrently while applying concurrency limits and rate limiting to avoid overwhelming the transcription provider. Workers could also scale horizontally as the workload increases.

### Storage

For a production implementation, I would store audio files in object storage such as Amazon S3 rather than directly on the application server.

The database would store metadata such as:

* File/object key
* Processing status
* Duration
* Language
* Transcript
* Segment timestamps
* Created/updated timestamps
* Error information

### Failure Recovery

Transient failures such as network errors, rate limits, or temporary provider failures should be retried using exponential backoff.

Jobs would have states such as:

```text
PENDING
PROCESSING
COMPLETED
FAILED
```

After a configurable retry limit, failed jobs could be moved to a dead-letter queue for investigation or manual retry.

Jobs should be idempotent so that retries do not create duplicate transcripts.

## API Design

For a production service, I would expose the pipeline through a REST API.

Example endpoints:

```text
POST /transcriptions
```

Accepts an audio file and creates a transcription job.

```text
GET /transcriptions/{id}
```

Returns the current processing status.

```text
GET /transcriptions/{id}/result
```

Returns the transcript and timestamps after processing is complete.

For long-running transcription, the upload endpoint should return a job ID rather than keeping the request open until transcription finishes.

## Security

The API key is loaded through an environment variable and should never be committed to source control.

Audio files and transcripts may contain sensitive information, so a production deployment should use appropriate encryption, access controls, retention policies, and secure deletion.

## Installation

Install the required dependency:

```bash
pip install -r requirements.txt
```

Configure the API key using an environment variable:

```text
OPENAI_API_KEY=your_api_key_here
```

The actual API key should never be committed to Git.

## Running

Example for validating an audio file:

```bash
python src/upload.py
```

Example for transcription:

```bash
python src/transcription.py
```

Example for transcription with segment timestamps:

```bash
python src/timestamps.py
```

The example scripts expect an audio file named `sample.mp3` in the working directory.

## Production Considerations

The assessment implementation is intentionally small. A production deployment would additionally include:

* Authentication and authorization
* File-size and request limits
* MIME-type validation
* Asynchronous job processing
* Object storage
* Persistent job tracking
* Retry and dead-letter handling
* Structured logging
* Monitoring and metrics
* Automated tests
* Storage lifecycle and cleanup policies
* Rate limiting
* Idempotency
