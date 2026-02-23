"""Toolkit for Flux image generation (fallback).

Fallback image generation when Nano Banana is unavailable.
Uses Flux API via available providers.
"""

import json
import logging
import os

import httpx
from agno.tools import Toolkit

logger = logging.getLogger(__name__)


class FluxTools(Toolkit):
    """Image generation toolkit using Flux (fallback)."""

    def __init__(self, api_key: str | None = None):
        super().__init__(name="flux_tools")
        self.api_key = api_key or os.getenv("FLUX_API_KEY", "")
        self.base_url = "https://api.us1.bfl.ai/v1"
        self.register(self.generate_image)

    def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
    ) -> str:
        """Generate an image using Flux API.

        Args:
            prompt: Detailed description of the image to generate.
            width: Image width in pixels (default 1024).
            height: Image height in pixels (default 1024).

        Returns:
            JSON string with generation result or error.
        """
        if not self.api_key:
            return json.dumps({"status": "error", "message": "FLUX_API_KEY not configured"})

        try:
            response = httpx.post(
                f"{self.base_url}/flux-pro-1.1",
                headers={"x-key": self.api_key},
                json={
                    "prompt": prompt,
                    "width": width,
                    "height": height,
                },
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return json.dumps(
                {
                    "status": "success",
                    "model": "flux",
                    "prompt": prompt,
                    "dimensions": f"{width}x{height}",
                    "response": data,
                }
            )
        except Exception as e:
            logger.error(f"Flux generation failed: {e}")
            return json.dumps({"status": "error", "message": str(e)})
