"""Toolkit for Seedance 2.0 video generation (ByteDance via Fal.ai).

Primary video generation model. Falls back to Runway if unavailable.
"""

import json
import logging
import os

import httpx
from agno.tools import Toolkit

logger = logging.getLogger(__name__)


class SeedanceTools(Toolkit):
    """Video generation toolkit using Seedance 2.0 via Fal.ai."""

    def __init__(self, api_key: str | None = None):
        super().__init__(name="seedance_tools")
        self.api_key = api_key or os.getenv("SEEDANCE_API_KEY", "")
        self.base_url = "https://queue.fal.run/fal-ai/seedance-2"
        self.register(self.generate_video)
        self.register(self.check_video_status)

    def generate_video(
        self,
        prompt: str,
        duration_seconds: int = 5,
        resolution: str = "1080p",
        aspect_ratio: str = "16:9",
    ) -> str:
        """Generate a video using Seedance 2.0.

        Args:
            prompt: Detailed scene description for video generation.
            duration_seconds: Video duration in seconds (max 15).
            resolution: Output resolution (720p, 1080p).
            aspect_ratio: Aspect ratio (16:9, 9:16, 1:1).

        Returns:
            JSON string with job ID for status polling, or error.
        """
        if not self.api_key:
            return json.dumps({"status": "error", "message": "SEEDANCE_API_KEY not configured"})

        try:
            response = httpx.post(
                self.base_url,
                headers={
                    "Authorization": f"Key {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "prompt": prompt,
                    "duration": duration_seconds,
                    "resolution": resolution,
                    "aspect_ratio": aspect_ratio,
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return json.dumps(
                {
                    "status": "queued",
                    "model": "seedance_2.0",
                    "request_id": data.get("request_id", ""),
                    "status_url": data.get("status_url", ""),
                    "prompt": prompt,
                }
            )
        except Exception as e:
            logger.error(f"Seedance generation failed: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def check_video_status(self, request_id: str) -> str:
        """Check the status of a video generation job.

        Args:
            request_id: The request ID returned from generate_video.

        Returns:
            JSON string with status and video URL if complete.
        """
        try:
            response = httpx.get(
                f"https://queue.fal.run/fal-ai/seedance-2/requests/{request_id}/status",
                headers={"Authorization": f"Key {self.api_key}"},
                timeout=30,
            )
            response.raise_for_status()
            return json.dumps(response.json())
        except Exception as e:
            logger.error(f"Seedance status check failed: {e}")
            return json.dumps({"status": "error", "message": str(e)})
