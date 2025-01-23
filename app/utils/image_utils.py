import os
import requests


def download_image(image_url: str, product_name: str) -> str:
    if not image_url or not image_url.startswith(("http://", "https://")):
        print(f"Skipping unsupported URL: {image_url}")
        return "N/A"
    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    filename = f"{product_name.replace(' ', '_')}.jpg"
    path = os.path.join("images", filename)
    os.makedirs("images", exist_ok=True)

    with open(path, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

    return path