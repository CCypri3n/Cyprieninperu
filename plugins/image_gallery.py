from pelican import signals
import os
import json
from bs4 import BeautifulSoup

def update_gallery_json(generator):
    content_path = generator.settings.get('PATH')
    extra_dir = os.path.join(content_path, 'extra')
    os.makedirs(extra_dir, exist_ok=True)
    gallery_file_path = os.path.join(extra_dir, 'gallery.json')

    if os.path.exists(gallery_file_path):
        with open(gallery_file_path, 'r') as f:
            gallery = json.load(f)
    else:
        gallery = []

    # Collect existing URLs to prevent duplicates
    existing_urls = {entry.get('url') for entry in gallery if 'url' in entry}
    # For videos: track both video and thumbnail URLs separately
    existing_video_urls = {entry.get('video_url') for entry in gallery if entry.get('type') == 'video'}

    new_items = []

    for article in generator.articles:
        soup = BeautifulSoup(article._content, 'html.parser')

        # First find all video items
        video_thumbnail_urls = set()
        video_wrappers = soup.find_all('div', class_=lambda x: x and 'item' in x.split() and 'video' in x.split())
        for video_div in video_wrappers:
            image_wrapper = video_div.find('div', class_='image-wrapper')
            if not image_wrapper:
                continue
            video_url = image_wrapper.get('data-video-url')
            thumbnail_img = image_wrapper.find('img')
            thumbnail_url = thumbnail_img.get('src') if thumbnail_img else None

            if video_url and thumbnail_url:
                # Add video entry if new
                if video_url not in existing_video_urls:
                    existing_video_urls.add(video_url)
                    new_items.append({
                        'type': 'video',
                        'video_url': video_url,
                        'thumbnail_url': thumbnail_url
                    })
                # Track thumbnail to exclude from normal images
                video_thumbnail_urls.add(thumbnail_url)

        # Then find normal images excluding video thumbnails
        imgs = soup.find_all('img')
        for img in imgs:
            url = img.get('src')
            if url and url not in existing_urls and url not in video_thumbnail_urls:
                existing_urls.add(url)
                new_items.append({'url': url})

    if new_items:
        gallery.extend(new_items)
        with open(gallery_file_path, 'w') as f:
            json.dump(gallery, f, indent=2)
        print(f"Added {len(new_items)} new items (images/videos) to gallery.json")

def register():
    signals.article_generator_finalized.connect(update_gallery_json)
    