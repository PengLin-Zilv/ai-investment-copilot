import requests


def send_discord_message(markdown_message: str, webhook_url: str) -> None:
    """Send one markdown message to a Discord channel webhook."""

    response = requests.post(webhook_url, json={"content": markdown_message}, timeout=10)
    if response.status_code < 200 or response.status_code >= 300:
        raise RuntimeError(f"Failed to send message to Discord: {response.text}")
