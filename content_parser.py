from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, KeepTogether, Image
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage, ImageOps
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
import os
SVG_ENABLED = True
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
except Exception:
    SVG_ENABLED = False

class ContentParser:
    """
    Dedicated logic layer that reads plain text/JSON and converts it into 
    rich PDF elements (Tables, ListFlowables, Paragraphs).
    """
    def __init__(self, styles):
        self.styles = styles

    def parse_recipient(self, recipient_data):
        """
        Parses recipient data into a Table for alignment.
        Expects a list of strings.
        """
        if not recipient_data or not isinstance(recipient_data, list):
            return []

        # Convert strings to Paragraphs for styling
        data = [[Paragraph(line, self.styles.get_style("Recipient"))] for line in recipient_data]
        
        # Create table
        t = Table(data, colWidths=[6 * inch])
        t.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        return [t, Spacer(1, 0.25 * inch)]

    def parse_body(self, body_data):
        """
        Parses body text. Renders as Paragraphs to maintain original visual style.
        Expects a list of strings.
        """
        if not body_data or not isinstance(body_data, list):
            return []

        story = []
        for item in body_data:
            if not isinstance(item, str):
                continue
            
            # Use Body style for everything, allowing inline XML tags like <b>
            style = self.styles.get_style("Body")
            story.append(Paragraph(item, style))

        return story

    def parse_signature(self, signature_data):
        """
        Parses signature block. Keeps lines together.
        Expects a list of strings.
        Supports [SIGNATURE:filename] marker for SVG signatures.
        """
        if not signature_data or not isinstance(signature_data, list):
            return []

        elements = []
        def _parse_unit(val, default_points=0):
            if not isinstance(val, str):
                return default_points
            v = val.strip().lower()
            try:
                if v.endswith('mm'):
                    return float(v[:-2]) * mm
                if v.endswith('in'):
                    return float(v[:-2]) * inch
                if v.endswith('px'):
                    return float(v[:-2])
                return float(v)
            except Exception:
                return default_points

        for line in signature_data:
            if line.startswith("[SIGNATURE:") and line.endswith("]"):
                content = line[11:-1]
                parts = [p.strip() for p in content.split('|')]
                filename = parts[0]
                opts = {}
                for p in parts[1:]:
                    if '=' in p:
                        k, v = p.split('=', 1)
                        opts[k.strip().lower()] = v.strip()

                assets_dir = getattr(self.styles, 'assets_dir', os.path.join(os.path.dirname(__file__), 'assets'))
                file_path = os.path.join(assets_dir, filename)

                before_space = _parse_unit(opts.get('before', '0'))
                after_space = _parse_unit(opts.get('after', '5mm'), 5 * mm)
                width_val = opts.get('w') or opts.get('width')
                height_val = opts.get('h') or opts.get('height')
                align_val = (opts.get('align') or 'left').lower()
                if align_val not in ['left', 'center', 'right']:
                    align_val = 'left'
                align_token = align_val.upper()

                if before_space > 0:
                    elements.append(Spacer(1, before_space))

                if os.path.exists(file_path):
                    try:
                        if filename.lower().endswith('.svg') and SVG_ENABLED:
                            drawing = svg2rlg(file_path)
                            target_width = _parse_unit(width_val, 1.5 * inch)
                            scale_factor = target_width / drawing.width
                            drawing.width *= scale_factor
                            drawing.height *= scale_factor
                            drawing.scale(scale_factor, scale_factor)
                            elements.append(drawing)
                        elif filename.lower().endswith('.png') or filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                            try:
                                pil = PILImage.open(file_path)
                                try:
                                    pil = pil.convert('RGBA')
                                except Exception:
                                    pass
                                
                                should_trim = (opts.get('trim') or 'false').lower() in ('true','1','yes','y')
                                
                                if should_trim:
                                    try:
                                        # Calculate Alpha BBox
                                        bbox_alpha = None
                                        if 'A' in pil.mode:
                                            alpha = pil.split()[-1]
                                            bbox_alpha = alpha.getbbox()
                                        
                                        # Calculate Grayscale BBox (Dark pixels on Light background)
                                        gray = pil.convert('L')
                                        mask = gray.point(lambda p: 255 if p < 250 else 0)
                                        bbox_gray = mask.getbbox()

                                        # Determine best bbox
                                        bbox = None
                                        if bbox_alpha and bbox_gray:
                                            # Intersection
                                            left = max(bbox_alpha[0], bbox_gray[0])
                                            top = max(bbox_alpha[1], bbox_gray[1])
                                            right = min(bbox_alpha[2], bbox_gray[2])
                                            bottom = min(bbox_alpha[3], bbox_gray[3])
                                            if left < right and top < bottom:
                                                bbox = (left, top, right, bottom)
                                            else:
                                                bbox = bbox_gray # Fallback if intersection is empty
                                        elif bbox_alpha:
                                            bbox = bbox_alpha
                                        elif bbox_gray:
                                            bbox = bbox_gray
                                        
                                        if bbox:
                                            # Check if bbox is full image (meaning no trim happened)
                                            if bbox == (0, 0, pil.width, pil.height):
                                                # If alpha was full but grayscale is smaller, use grayscale
                                                if bbox_gray and bbox_gray != bbox:
                                                    bbox = bbox_gray

                                            pil = pil.crop(bbox)
                                    except Exception:
                                        pass
                                reader = ImageReader(pil)
                                img = Image(reader)
                            except Exception:
                                img = Image(file_path)
                            target_w = _parse_unit(width_val, 1.5 * inch)
                            if height_val:
                                target_h = _parse_unit(height_val, 0)
                                if not target_h:
                                    iw, ih = (pil.size if pil is not None else (img.drawWidth, img.drawHeight))
                                    aspect = ih / float(iw)
                                    target_h = target_w * aspect
                            else:
                                if pil is not None:
                                    iw, ih = pil.size
                                else:
                                    iw, ih = img.drawWidth, img.drawHeight
                                aspect = ih / float(iw)
                                target_h = target_w * aspect
                            img.drawWidth = target_w
                            img.drawHeight = target_h
                            img.hAlign = align_token
                            elements.append(img)
                        else:
                            msg = f"[Unsupported signature format: {filename}]"
                            elements.append(Paragraph(msg, self.styles.get_style("Signature")))
                    except Exception as e:
                        elements.append(Paragraph(f"[Error loading signature: {filename}]", self.styles.get_style("Signature")))
                else:
                    elements.append(Paragraph(f"[Signature file not found: {filename}]", self.styles.get_style("Signature")))

                if after_space and after_space > 0:
                    elements.append(Spacer(1, after_space))
            else:
                elements.append(Paragraph(line, self.styles.get_style("Signature")))
        
        return [KeepTogether(elements)]
