# Cyprien in Peru — Personal Blog

This repository contains the source files for the multilingual static site ["Cyprien in Peru"](https://cyprieninperu.netlify.app/), a personal blog documenting a year-long adventure in Peru. The site is generated using the [Pelican](https://getpelican.com/) static site generator.

## Highlights

- Full i18n support with English, French, and German translations
- SEO and social meta support: OpenGraph, Twitter Cards, JSON-LD
- Responsive design optimized for mobile devices
- Privacy-friendly analytics with GoatCounter with support for "Urchin Tracking Module" (?utm_source=mail&utm_campaign=going_abroad)
- Carousel and lazy-loading images to improve user experience and performance

## Build & preview locally

1. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install Pelican and Markdown:

    ```bash
    pip install pelican markdown pybabel
    ````

3. Build the site and write output to `output/`:

    ```bash
    pelican content -o output -s pelicanconf.py
    ```

4. Serve and preview locally (from project root):

    ```bash
    # serve the generated site on http://localhost:8000
    python3 -m http.server --directory output 8000
    ```

    or use Pelican:

    ```bash
    pelican -l
    #-r for rebuild on detected changes
    pelican -r -l
    ```

## Compile for publication

1. Optional: Use Pybabel to update translations, if applicable

    ```bash
    pybabel extract -F babel.cfg -o messages.pot .
    pybabel update -i messages.pot -d theme/locale
    pybabel compile -d theme/locale
    ```

2. Generate the static site with the wrapper that includes custom scripts.

   ```bash
   bash bin/build_and_patch.sh
   ```

3. Push the changes to the Github repo.

    ```bash
    git add .
    git commit -m "Commit Message"
    git push origin main
    ```

## TO-DO

- Rewrite old articles
