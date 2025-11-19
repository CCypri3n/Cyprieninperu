from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import re

class ImageRewriteTreeprocessor(Treeprocessor):
    def run(self, root):
        lang_prefix_pattern = re.compile(r'^/(de|fr|es)/images/')

        for image in root.iter('img'):
            src = image.get('src', '')
            if lang_prefix_pattern.match(src):
                # Remove language prefix from image URL
                new_src = re.sub(r'^/(de|fr|es)/images/', '/images/', src)
                image.set('src', new_src)
        return root

class ImageRewriteExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(ImageRewriteTreeprocessor(md), 'image_rewrite', 15)

def makeExtension(**kwargs):
    return ImageRewriteExtension(**kwargs)
