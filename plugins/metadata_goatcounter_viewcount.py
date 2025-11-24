from pelican import signals
import json

def add_view_counts(generator):
    with open('content/extra/viewcounts.json', 'r') as f:
        counts = json.load(f)

    for article in generator.articles:
        # Match article URL path to view counts key
        lang_prefix = article.lang + '/' if article.lang not in ['', 'en'] else ''
        # article.url may or may not start with slash
        raw_path = article.url.strip('/')  
        path = f'/{lang_prefix}{raw_path}'
        article.view_count = counts.get(path, 0)

def register():
    signals.article_generator_finalized.connect(add_view_counts)
