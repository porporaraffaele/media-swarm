"""Toolkit for Nano Banana image generation (Google Gemini Image API).

Primary image generation model. Falls back to Flux if unavailable.
"""

import json
import logging
import os

import httpx
from agno.tools import Toolkit

logger = logging.getLogger(__name__)


class NanoBananaTools(Toolkit):
    """Image generation toolkit using Nano Banana / Google Gemini Image API."""

    def __init__(self, api_key: str | None = None):
        super().__init__(name="nano_banana_tools")
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.register(self.generate_image)

    def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        style: str = "default",
    ) -> str:
        """Generate an image using Nano Banana (Google Gemini Image API).

        Args:
            prompt: Detailed description of the image to generate.
            width: Image width in pixels (default 1024).
            height: Image height in pixels (default 1024).
            style: Style hint (default, photorealistic, illustration, digital_art).

        Returns:
            JSON string with generation result or error.
        """
        if not self.api_key:
            return json.dumps({"status": "error", "message": "GOOGLE_API_KEY not configured"})

        full_prompt = f"Generate an image: {prompt}"
        if style != "default":
            full_prompt += f" Style: {style}."

        try:
            response = httpx.post(
                f"{self.base_url}/models/gemini-2.0-flash-exp:generateContent",
                params={"key": self.api_key},
                json={
                    "contents": [{"parts": [{"text": full_prompt}]}],
                    "generationConfig": {
                        "responseModalities": ["TEXT", "IMAGE"],
                        "imageDimensions": {"width": width, "height": height},
                    },
                },
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return json.dumps(
                {
                    "status": "success",
                    "model": "nano_banana",
                    "prompt": prompt,
                    "dimensions": f"{width}x{height}",
                    "response": data,
                }
            )
        except Exception as e:
            logger.error(f"Nano Banana generation failed: {e}")
            return json.dumps({"status": "error", "message": str(e)})
