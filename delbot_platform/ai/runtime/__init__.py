"""
Runtime entrypoints for AI services.

Each module in this package acts as the executable entrypoint
for a PlatformService.

Platform Launchers should invoke these modules instead of
calling AI runtimes (vLLM, Infinity, PaddleOCR, Whisper)
directly.
"""