from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests
import os


app = Flask(__name__)
CORS(app)


def extract_images_from_url(url, word):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        images = []
        # search_words = [' ' +word.lower()+' ' for word in search_text.split()]

        if word in soup.title.string.lower():
            # print("1")
            for img in soup.find_all("img"):
                images.append(
                    {
                        "src": img.get("src"),
                        "alt": img.get("alt", ""),
                        "title": img.get("title", ""),
                    }
                )
        else:
            for img in soup.find_all("img"):
                if (
                    word in img.get("alt", "").lower()
                    or word in img.get("title", "").lower()
                ):
                    # print(img.get('src'))
                    # print("2")
                    images.append(
                        {
                            "src": img.get("src"),
                            "alt": img.get("alt", ""),
                            "title": img.get("title", ""),
                        }
                    )
            if images == []:
                # print("3")
                paragraphs = soup.find_all(
                    "p", string=lambda text: word in text.lower()
                )
                for paragraph in paragraphs:
                    if paragraph:
                        for img in paragraph.find_previous_siblings("img"):
                            images.append(
                                {
                                    "src": img.get("src"),
                                    "alt": img.get("alt", ""),
                                    "title": img.get("title", ""),
                                }
                            )
                        for img in paragraph.find_next_siblings("img"):
                            images.append(
                                {
                                    "src": img.get("src"),
                                    "alt": img.get("alt", ""),
                                    "title": img.get("title", ""),
                                }
                            )

        return images
    except Exception as e:
        return []


def save_image(image_url, filename):
    try:
        original_image_url = image_url.replace("/220px-", "/")
        print("save")
        print(image_url)

        print(requests.get(original_image_url))
        response = requests.get(original_image_url)
        response.raise_for_status()
        image_path = os.path.join("images", filename)
        with open(image_path, "wb") as file:
            file.write(response.content)
    except Exception as e:
        pass


@app.route("/get_images", methods=["POST"])
def get_images():
    data = request.get_json()
    sites = data.get("sites", [])
    search_text = data.get("search_text")
    if not sites or not search_text:
        return jsonify({"error": "sites and search_text are required parameters"}), 400

    search_results = []
    i = 0
    images1 = []
    images2 = []
    images3 = []
    for site in sites:
        url = site.get("url")
        images1.extend(extract_images_from_url(url, " "+search_text+" "))
        if len(search_text.split()) > 1:
            images2.extend(
                extract_images_from_url(url, " " + search_text.split()[1] + " ")
            )
            images3.extend(
                extract_images_from_url(url, " " + search_text.split()[0] + " ")
            )

    if len(search_text.split()) > 1:
        images = images1 + images2 + images3
    else:
        images = images1
    unique_images = set()
    filtered_images = []
    for json_item in images:
        url = json_item["src"]
        if url not in unique_images:
            unique_images.add(url)
            filtered_images.append(json_item)

    for image in filtered_images:
        i += 1

        search_result = {
            "id": i,
            "search_text": search_text,
            "website": url,
            "url": image["src"],
            "title": image["title"],
            "description": image["alt"],
            "choix": 0,
        }
        search_results.append(search_result)
        # save_image(image['src'], f'{image["alt"]}{i}.jpg')
    return jsonify({"search_results": search_results})


if __name__ == "__main__":
    app.run(debug=True)
