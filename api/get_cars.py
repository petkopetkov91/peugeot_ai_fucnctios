import requests
import xml.etree.ElementTree as ET
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def handler():
    url = "https://sale.peugeot.bg/ecommerce/fb/product_feed.xml"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    root = ET.fromstring(response.content)
    ns = {"g": "http://base.google.com/ns/1.0"}

    cars = []
    for item in root.findall(".//item"):
        availability = item.find("g:availability", ns)
        if availability is not None and availability.text.lower() == "in stock":
            title = item.find("g:title", ns).text.strip()
            description = item.find("g:description", ns).text.strip()
            link = item.find("g:link", ns).text.strip()
            image_link = item.find("g:image_link", ns).text.strip()

            cars.append({
                "model": title,
                "price": description,
                "image": image_link,
                "url": link
            })

    return JSONResponse(content=cars)
