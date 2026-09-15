# Streaming Audio

Stream audio chunks as they're generated for lower latency.

## Model Selection for Streaming

| Model | Latency | Use Case |
|-------|---------|----------|
| `eleven_flash_v2_5` | ~75ms | Lowest latency, 32 languages |
| `eleven_flash_v2` | ~75ms | Lowest latency, English only |
| `eleven_turbo_v2_5` | Low | Balanced quality/speed |

## Python Streaming

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

audio_stream = client.text_to_speech.stream(
    text="This is a streaming example with ultra-low latency.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_flash_v2_5"
)

with open("output.mp3", "wb") as f:
    for chunk in audio_stream:
        f.write(chunk)
```

### Real-Time Playback

```python
import subprocess

def play_stream(audio_stream):
    process = subprocess.Popen(
        ["ffplay", "-nodisp", "-autoexit", "-"],
        stdin=subprocess.PIPE
    )
    for chunk in audio_stream:
        process.stdin.write(chunk)
    process.stdin.close()
    process.wait()

audio_stream = client.text_to_speech.stream(
    text="Playing this audio in real-time.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_flash_v2_5"
)
play_stream(audio_stream)
```

## JavaScript Streaming

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createWriteStream } from "fs";
import { Readable } from "stream";

const client = new ElevenLabsClient();

const audioStream = await client.textToSpeech.convert("JBFqnCBsd6RMkjVDRZzb", {
  text: "Streaming audio in JavaScript.",
  modelId: "eleven_flash_v2_5",
});

// Write to file (convert() returns a web ReadableStream — bridge to a Node stream first)
Readable.fromWeb(audioStream).pipe(createWriteStream("output.mp3"));

// Or process chunks
for await (const chunk of audioStream) {
  console.log(`Received ${chunk.length} bytes`);
}
```

## WebSocket Streaming

For text-streaming input where you send text chunks as they arrive (e.g., from an LLM).

### Connection

```
wss://api.elevenlabs.io/v1/text-to-speech/{voiceId}/stream-input?model_id={modelId}
```

**Note:** WebSockets are unavailable for the `eleven_v3` model. Use `eleven_flash_v2_5` for lowest latency.

### Message Flow

1. **Initialize** - Send voice settings and configuration
2. **Send text** - Stream text chunks as they arrive
3. **Close** - Send empty string to signal completion
4. **Receive** - Process audio chunks as they're generated

### Authenticated WebSocket transport

Have the user's application supply an already authenticated connection through its private credential integration. This reference deliberately does not load credential files, read process credentials, or construct a key-bearing handshake. Implement the official handshake in the user's approved application integration, never in chat or generated shell arguments.

After the connection is ready, use the message protocol below. Bound every session to the approved duration and cost, close it on completion or error, and return sanitized errors. Preserve the chunk scheduling, model constraints, output decoding and alignment behavior documented here. For a first production clip, prefer the SDK streaming examples above; the low-level transport is optional.

### Input Messages

**Initialization (first message):**

```json
{
  "text": " ",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.8,
    "use_speaker_boost": false
  },
  "generation_config": {
    "chunk_length_schedule": [120, 160, 250, 290]
  }
}
```

**Text chunks:**

```json
{ "text": "Your text content here" }
```

**Force flush (generate audio immediately):**

```json
{ "text": "End of sentence.", "flush": true }
```

**Close connection:**

```json
{ "text": "" }
```

### Output Messages

**Audio chunk:**

```json
{
  "audio": "base64_encoded_audio_data"
}
```

**Stream complete:**

```json
{
  "isFinal": true
}
```

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `chunk_length_schedule` | Array of character counts that trigger audio generation. The model waits until it has this many characters before generating audio, which improves quality but adds latency. Lower values = faster response, higher values = better prosody. Example: `[120, 160, 250, 290]` means generate after 120 chars, then after 160 more, etc. |
| `flush` | Set `true` to force immediate audio generation without waiting for the character threshold. Use at the end of sentences or when you need audio NOW. |
| `voice_settings` | Adjustable per-message: `stability`, `similarity_boost`, `use_speaker_boost` |

### Important Notes

- **Inactivity timeout**: Connection closes after 20 seconds without activity. Send a space `" "` to keep alive.
- **TTFB (Time to First Byte)**: How long until audio starts playing. Affected by `chunk_length_schedule` - the model waits for enough text before generating.
- **Model limitation**: WebSockets are unavailable for `eleven_v3`.
- **Best practice**: Use `flush: true` at conversation turn endings to ensure the buffered text gets spoken.
- **Alignment data**: Word-level timestamps available via `alignment` field for lip-sync or captions.

## Best Practices

1. **Use Flash models** for real-time:
   - `eleven_flash_v2_5` for multilingual (~75ms)
   - `eleven_flash_v2` for English-only (~75ms)

2. **Buffer audio** before playback to prevent choppy output

3. **Handle disconnections** gracefully in WebSocket streams

4. **Choose output format based on use case**:
   - `pcm_24000` - lowest latency processing
   - `mp3_44100_128` - direct playback
   - `ulaw_8000` - telephony/Twilio integration
