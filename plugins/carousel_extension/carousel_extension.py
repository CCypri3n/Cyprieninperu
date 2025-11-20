from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import re
import xml.etree.ElementTree as etree

LANG_PREFIX_PATTERN = re.compile(r'^/(de|fr|es)/images/')

def rewrite_image_path(path):
    return path #LANG_PREFIX_PATTERN.sub('/images/', path)

class CarouselProcessor(BlockProcessor):
    RE_FENCE_START = r'^<carousel>$'
    RE_FENCE_END = r'^</carousel>$'

    # Markdown syntax example for video:
    # ![alt](thumbnail.jpg) | video:video_url.mp4 | Caption text

    def test(self, parent, block):
        first_line = block.strip().split('\n', 1)[0]
        return re.match(self.RE_FENCE_START, first_line)

    def run(self, parent, blocks):
        block = blocks.pop(0)
        lines = block.strip().split('\n')

        # Remove opening <carousel>
        lines.pop(0)

        # Container: main.carousel-container
        main_element = etree.SubElement(parent, 'main', {'class': 'carousel-container'})

        # carousel div
        carousel_div = etree.SubElement(main_element, 'div', {'class': 'carousel'})

        # Regex to match Markdown image syntax: ![alt](path)
        MD_IMAGE_RE = re.compile(r'!\[(.*?)\]\((.*?)\)')
        MD_IMAGE_VIDEO_RE = re.compile(r'!\[(.*?)\]\((.*?)\)\((.*?)\)')

        for i, line in enumerate(lines):
            if re.match(self.RE_FENCE_END, line.strip()):
                break
            if not line.strip():
                continue

            # Split by pipe for caption:
            if '|' in line:
                main_part, caption_text = line.split('|', 1)
                caption_text = caption_text.strip()
            else:
                main_part = line.strip()
                caption_text = False

            # Try to match video syntax with thumbnail and video URL
            m = MD_IMAGE_VIDEO_RE.match(main_part)
            if m:
                alt_text = m.group(1).strip()
                thumbnail_src = m.group(2).strip()
                video_src = m.group(3).strip()
                thumbnail_src = rewrite_image_path(thumbnail_src)
                video_src = rewrite_image_path(video_src)
                is_video = True
            else:
                # Fallback: normal image syntax only
                simple_img_re = re.compile(r'!\[(.*?)\]\((.*?)\)')
                m2 = simple_img_re.match(main_part)
                if m2:
                    alt_text = m2.group(1).strip()
                    thumbnail_src = m2.group(2).strip()
                    video_src = ''
                    is_video = False
                else:
                    alt_text = ''
                    thumbnail_src = rewrite_image_path(main_part)
                    video_src = ''
                    is_video = False

            # Create item div with classes
            classes = ['item']
            if i == 0:
                classes.append('active')
            if is_video:
                classes.append('video')

            item_div = etree.SubElement(carousel_div, 'div', {'class': ' '.join(classes)})

            # Add wrapper with appropriate attributes
            wrapper_attrs = {'class': 'image-wrapper'}
            if is_video:
                wrapper_attrs['data-video-url'] = video_src

            wrapper_div = etree.SubElement(item_div, 'div', wrapper_attrs)

            # Add thumbnail image
            etree.SubElement(wrapper_div, 'img', {'src': thumbnail_src, 'alt': alt_text})

            # Add play icon overlay if video
            if is_video:
                playBtn = etree.SubElement(wrapper_div, 'div', {'class': 'play-btn'})
                playBtnSvg = etree.SubElement(playBtn, 'svg', {'viewBox':'0 0 24 24'})
                etree.SubElement(playBtnSvg, 'polygon', {'points':"8,5 19,12 8,19", 'fill':"white"})

            # Add caption paragraph
            if caption_text:
                p_caption = etree.SubElement(wrapper_div, 'p', {'class': 'caption'})
                p_caption.text = caption_text 

        # Buttons as siblings inside main
        buttonElement = etree.SubElement(main_element, 'button', {'class': 'carousel-btn prev-btn'})
        svgElement = etree.SubElement(buttonElement, 'svg', {'viewBox':"0 0 24 24"})
        etree.SubElement(svgElement, 'path', {
            'd': "M15 18l-6-6 6-6",
            'stroke': 'currentColor',
            'stroke-width': '2',
            'fill': 'none',
            'stroke-linecap': 'round'
        })

        
        buttonElement = etree.SubElement(main_element, 'button', {'class': 'carousel-btn next-btn'})
        svgElement = etree.SubElement(buttonElement, 'svg', {'viewBox':"0 0 24 24"})
        etree.SubElement(svgElement, 'path', {
            'd': "M9 6l6 6-6 6",
            'stroke': 'currentColor',
            'stroke-width': '2',
            'fill': 'none',
            'stroke-linecap': 'round'
        })


        # Modal div once inside main
        modal_div = etree.SubElement(main_element, 'div', {'id': 'modal', 'class': 'modal'})

        # Close button inside modal
        close_span = etree.SubElement(modal_div, 'span', {'id': 'modalClose', 'class': 'modal-close'})
        close_span.text = '×'  # Multiplication sign (close icon)

        # Modal image inside modal div
        etree.SubElement(modal_div, 'img', {'id': 'modalImage', 'class': 'modal-content', 'src': '', 'alt': 'Full size image'})
        etree.SubElement(modal_div, 'div', {'id': 'modalVideo', 'class': 'modal-content'})

class CarouselExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(CarouselProcessor(md.parser), 'carousel', 175)

def makeExtension(**kwargs):
    return CarouselExtension(**kwargs)
