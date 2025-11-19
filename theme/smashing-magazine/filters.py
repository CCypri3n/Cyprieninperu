def image_url_no_lang(url, lang):
    # Remove leading slash and prepend SITEURL without language prefix
    base_url = SITEURL  # or set base_url manually or from settings
    return f"{base_url}/images/{url.lstrip('/')}"
