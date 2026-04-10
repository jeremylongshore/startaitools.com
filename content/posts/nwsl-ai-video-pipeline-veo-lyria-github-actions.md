+++
title = 'Building an AI Video Pipeline with Vertex AI Veo, Lyria, and GitHub Actions'
slug = 'nwsl-ai-video-pipeline-veo-lyria-github-actions'
date = 2025-11-08T10:00:00-06:00
draft = false
tags = ["vertex-ai", "veo", "lyria", "video-generation", "github-actions", "ci-cd", "ffmpeg", "nwsl"]
categories = ["Technical Deep-Dive"]
description = "An NWSL documentary video pipeline using Vertex AI Veo for video, Lyria for music, and GitHub Actions for CI/CD. 23 commits, 53K+ lines, and every Lyria workaround nobody documented."
+++

## The Goal

Build a CI/CD pipeline that produces documentary-style video content about NWSL soccer. Not a one-off script. A repeatable, trigger-on-push system that generates video segments, scores them with AI music, assembles the final cut, and watermarks the output.

The media APIs are Vertex AI Veo (video generation) and Vertex AI Lyria (music generation). The orchestration is GitHub Actions. The assembly is ffmpeg. Over 23 commits and 53,000+ lines, the pipeline went from a blank repo to a working end-to-end system.

Most of those 53K lines are canon documents -- 60+ files covering every design decision, every API quirk, every workaround. When the platform APIs are this new, documentation is survival.

## Veo: The Easy Part

Vertex AI Veo generates video from text prompts. The API is straightforward:

```python
from google.cloud import aiplatform

response = aiplatform.gapic.PredictionServiceClient().predict(
    endpoint=VEO_ENDPOINT,
    instances=[{"prompt": segment_prompt}],
    parameters={"duration_seconds": 8, "aspect_ratio": "16:9"},
)
```

Each segment generates an 8-second clip. The documentary is structured as 9 segments: intro, 7 topic segments (player profiles, game highlights, team culture), and outro. Veo handles each segment independently. Quality is good enough for documentary style -- slow pans, atmospheric shots, not action footage.

The real work was prompt engineering for visual consistency. Each segment needs to match a visual style guide: same color temperature, same pacing, same framing conventions. I wrote a canon style document that every prompt references. The prompts don't say "generate a video of a soccer player." They say "twilight exterior, anamorphic lens, cool blue-orange color grade, slow dolly toward subject, NWSL match-day atmosphere."

Consistency across segments requires consistency across prompts. The canon enforces it.

## Lyria: The Hard Part

Lyria generates music. On paper. In practice, Lyria has undocumented API behavior that consumed most of the debugging time in this project.

### Endpoint Discovery

The first problem: which endpoint to call. Vertex AI documentation references a `predict` endpoint for media generation. Lyria does not use `predict`. It uses `predictLongRunning`, which returns a long-running operation (LRO) that you poll for completion.

This is not in the quickstart guide. I found it by reading the REST API reference for the `imagegeneration` model family (which Lyria shares infrastructure with) and testing endpoints systematically.

```python
# This does NOT work for Lyria
response = client.predict(endpoint=LYRIA_ENDPOINT, instances=[...])

# This works
operation = client.predict_long_running(
    endpoint=LYRIA_ENDPOINT,
    instances=[{"prompt": music_prompt}],
    parameters={"duration_seconds": 30},
)
```

### The 30-Second Limit

Lyria generates a maximum of 30 seconds of audio per request. The documentary segments need 60 seconds of music each. The workaround: two sequential API calls per segment, then concatenate with ffmpeg.

```python
async def generate_segment_music(prompt: str) -> bytes:
    """Generate 60s of music using two 30s Lyria calls."""
    part_1 = await lyria_generate(prompt, duration=30)
    part_2 = await lyria_generate(prompt + " continuation", duration=30)
    return concatenate_audio(part_1, part_2)
```

The `+ " continuation"` in the second prompt is crude but effective. Without it, Lyria generates two independent 30-second pieces that sound like different songs. With the continuation hint, the second piece at least starts in the same key and tempo. Not seamless, but a crossfade hides the seam.

### Bounded LRO Polling

Long-running operations need polling. Lyria's LROs take anywhere from 15 seconds to 4 minutes. Unbounded polling is a CI/CD killer -- a stuck LRO will hang your GitHub Actions job until the 6-hour timeout.

The polling implementation uses bounded exponential backoff:

```python
async def poll_lro(operation_name: str, max_wait: int = 300) -> dict:
    """Poll a Lyria LRO with bounded backoff. Fail after max_wait seconds."""
    elapsed = 0
    interval = 2

    while elapsed < max_wait:
        op = client.get_operation(name=operation_name)
        if op.done:
            if op.error.code:
                raise LyriaError(f"LRO failed: {op.error.message}")
            return op.response
        await asyncio.sleep(interval)
        elapsed += interval
        interval = min(interval * 1.5, 30)  # Cap at 30s intervals

    raise TimeoutError(f"LRO {operation_name} exceeded {max_wait}s")
```

The 300-second cap means a truly stuck LRO fails fast and the pipeline moves on with a fallback (silence + subtitle explaining "music generation timed out"). Better to ship with a gap than hang the entire CI run.

## ffmpeg: Assembly and Watermark

The 9 segments need assembly into a final video with transitions, watermark overlay, and synchronized audio. ffmpeg handles all of this, but getting ffmpeg installed and working in GitHub Actions was its own debugging session.

### The Octal Error

The shell script that drives ffmpeg assembly had a syntax error that only appeared in GitHub Actions:

```bash
# This fails in strict bash
SEGMENT_COUNT=09  # bash interprets 09 as invalid octal
```

Numbers with leading zeros are octal literals in bash. `09` is not valid octal. Locally, my shell was lenient. GitHub Actions uses strict bash. The fix:

```bash
SEGMENT_COUNT=9  # no leading zero
```

Fifteen minutes of debugging for a single character. The error message was `value too great for base (error token is "09")` which at least pointed directly at the problem.

### The Assembly Pipeline

Each segment gets assembled with a crossfade transition:

```bash
ffmpeg -i segment_01.mp4 -i segment_02.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=7.5" \
  -c:v libx264 -preset fast merged_01_02.mp4
```

The watermark is a PNG overlay positioned in the bottom-right corner with 30% opacity. Applied as the final step after all segments are merged, so the watermark is consistent across the entire video.

The complete assembly script chains 8 crossfade merges, applies the watermark, mixes in the Lyria audio tracks, and outputs a single MP4. Total runtime in GitHub Actions: 4-7 minutes depending on runner performance.

## The CI/CD Pipeline

The GitHub Actions workflow triggers on push to the `content/` directory. When a new segment prompt or style update is committed:

1. **Validate** -- lint prompt files, check canon consistency
2. **Generate Video** -- call Veo for each segment (parallel, 9 jobs)
3. **Generate Music** -- call Lyria for each segment (sequential, respecting rate limits)
4. **Assemble** -- run the ffmpeg assembly pipeline
5. **Archive** -- upload final video to Cloud Storage with timestamp

The video generation jobs run in parallel because Veo handles concurrent requests well. The music generation runs sequentially because Lyria rate-limits aggressively -- parallel calls return 429s.

```yaml
generate-video:
  strategy:
    matrix:
      segment: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    max-parallel: 9
  steps:
    - run: python generate_segment.py --segment ${{ matrix.segment }}

generate-music:
  needs: generate-video
  steps:
    - run: |
        for i in $(seq 1 9); do
          python generate_music.py --segment $i
          sleep 5  # rate limit buffer
        done
```

The `sleep 5` between music generation calls is ugly but necessary. Without it, Lyria returns 429 errors on the third or fourth call every time.

## Canon-Locked Production

The 60+ canon documents are not optional reading. They are the production specification. Every prompt references the style guide. Every ffmpeg command references the assembly spec. Every API call references the integration doc that describes the workaround.

When someone modifies a prompt six months from now, the canon tells them why the prompt says "continuation" and why the polling timeout is 300 seconds. Without the canon, the next developer removes the continuation hint, gets two mismatched audio pieces, and spends three hours debugging something I already solved.

Canon is not documentation. Canon is institutional memory encoded as files.

## Key Takeaways

**Lyria's API surface is not what the docs describe.** Use `predictLongRunning`, not `predict`. Budget for the 30-second limit and plan your audio architecture around 2-call generation.

**Bound every LRO poll.** Unbounded polling in CI/CD will eventually hang a job. Set a max wait, handle the timeout, and move on with a degraded output rather than a stuck pipeline.

**ffmpeg in CI needs defensive scripting.** No leading zeros in numeric variables. Explicit codec flags. Test your assembly script in the same bash mode as your CI runner.

**Canon documents pay for themselves when the APIs are new.** Veo and Lyria have almost no community documentation. Every workaround you discover and write down saves the next person (or future you) hours of endpoint testing.

---

**Related Posts:**
- [Building Production CI/CD: Documentation to Deployment](/posts/building-production-ci-cd-documentation-to-deployment/) -- CI/CD pipeline patterns that informed this GitHub Actions architecture
- [Marketplace CI Hardening: Sync Guard and Plugin Scaffold](/posts/marketplace-ci-hardening-sync-guard-plugin-scaffold/) -- CI governance patterns used in the validation stage
- [GCR to Artifact Registry Deploy Workflow Migration](/posts/gcr-to-artifact-registry-deploy-workflow-migration/) -- Another CI/CD debugging session with Google Cloud tooling
