"""Toolkit for Runway video generation (fallback).

Fallback video generation when Seedance 2.0 is unavailable.
"""

import json
import logging
import os

import httpx
from agno.tools import Toolkit

logger = logging.getLogger(__name__)


class RunwayTools(Toolkit):
    """Video generation toolkit using Runway (fallback)."""

    def __init__(self, api_key: str | None = None):
        super().__init__(name="runway_tools")
        self.api_key = api_key or os.getenv("RUNWAY_API_KEY", "")
        self.base_url = "https://api.dev.runwayml.com/v1"
        self.register(self.generate_video)
        self.register(self.check_video_status)

    def generate_video(
        self,
        prompt: str,
        duration_seconds: int = 5,
        resolution: str = "1080p",
        aspect_ratio: str = "16:9",
    ) -> str:
        """Generate a video using Runway API.

        Args:
            prompt: Detailed scene description for video generation.
            duration_seconds: Video duration in seconds (5 or 10).
            resolution: Output resolution (720p, 1080p).
            aspect_ratio: Aspect ratio (16:9, 9:16).

        Returns:
            JSON string with task ID for status polling, or error.
        """
        if not self.api_key:
            return json.dumps({"status": "error", "message": "RUNWAY_API_KEY not configured"})

        try:
            response = httpx.post(
                f"{self.base_url}/image_to_video",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "X-Runway-Version": "2024-11-06",
                },
                json={
                    "model": "gen4_turbo",
                    "promptText": prompt,
                    "duration": duration_seconds,
                    "ratio": aspect_ratio,
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return json.dumps(
                {
                    "status": "queued",
                    "model": "runway_gen4_turbo",
                    "task_id": data.get("id", ""),
                    "prompt": prompt,
                }
            )
        except Exception as e:
            logger.error(f"Runway generation failed: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def check_video_status(self, task_id: str) -> str:
        """Check the status of a Runway video generation task.

        Args:
            task_id: The task ID returned from generate_video.

        Returns:
            JSON string with status and video URL if complete.
        """
        try:
            response = httpx.get(
                f"{self.base_url}/tasks/{task_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "X-Runway-Version": "2024-11-06",
                },
                timeout=30,
            )
            response.raise_for_status()
            return json.dumps(response.json())
        except Exception as e:
            logger.error(f"Runway status check failed: {e}")
            return json.dumps({"status": "error", "message": str(e)})
