from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)
def extract_images_from_url(url, search_text):
    try:
        
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = []

        if search_text in soup.title.string:
            # If the string is found, extract image URLs
            for img in soup.find_all('img'):
                images.append({
                        'src': img.get('src'),
                        'alt': img.get('alt', ''),
                        'title': img.get('title', ''),
                    })
        else:
            for img in soup.find_all('img'):
                
                if search_text in img.get('alt', '') or search_text in img.get('title', ''):
                    images.append({
                        'src': img.get('src'),
                        'alt': img.get('alt', ''),
                        'title': img.get('title', ''),
                    })
            if images==[]:
                paragraphs = soup.find_all("p", text=lambda text: search_text in text)
                for paragraph in paragraphs:   
                    if paragraph:
                        for img in paragraph.find_previous_siblings("img"):
                            images.append({
                                'src': img.get('src'),
                                'alt': img.get('alt', ''),
                                'title': img.get('title', ''),
                            })
                        for img in paragraph.find_next_siblings("img"):
                            images.append({
                                'src': img.get('src'),
                                'alt': img.get('alt', ''),
                                'title': img.get('title', ''),
                            })
            
        # for link in soup.find_all('a', href=True):
        #     if search_text in link['href']:
        #         img_tag = link.find('img')
        #         if img_tag:
        #             images.append({
        #                 'src': img_tag.get('src', ''),
        #                 'alt': img_tag.get('alt', ''),
        #                 'title': link['href'],
        #             })
        return images
    except Exception as e:
        return []

def save_image(image_url, filename):
    try:
        
        response = requests.get(image_url)
        response.raise_for_status()
        image_path = os.path.join('images', filename)
        with open(image_path, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        pass

@app.route('/get_images', methods=['POST'])
def get_images():
    print("kk")
    data = request.get_json()
    
    sites = data.get('sites', [])
    search_text = data.get('search_text')

    if not sites or not search_text:
        return jsonify({'error': 'sites and search_text are required parameters'}), 400

    search_results = []
    i=0
    for site in sites:
        url = site.get('url')
        
        images = extract_images_from_url(url, search_text)
        for image in images:
            i+=1
            # search_result = {
            #     'id':i,
            #     'image_url': image['src'],  # Direct URL of the image source
            #     'title': image['title'],  # Title of the image, if available
            #     'description': image['alt'],  # Alt text or description of the image, if available
            #     'source_website': url,  # URL of the website where the image is found
            #     'tags':[]
            # }
            search_result = {
                'id': i,
                'url': image['src'],
                'title': image['title'],
                'description': image['alt'],
                'tags': ["Mountains", "Aesthetic", "Pretty", "Scenic", "Rugged"],  # Replace with your own tags
                'source_website': url
            }
            search_results.append(search_result)
            # save_image(image['src'], f'{image["alt"]}{i}.jpg')
    return jsonify({'search_results': search_results})
    

if __name__ == '__main__':
    app.run(debug=True)
