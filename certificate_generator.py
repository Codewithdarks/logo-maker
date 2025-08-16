from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
import os
from datetime import datetime
import requests
from io import BytesIO

class CertificateGenerator:
    def __init__(self):
        self.width, self.height = landscape(A4)
        # A4 landscape: 841.89 x 595.27 points
        
        # Register EB Garamond font
        try:
            pdfmetrics.registerFont(TTFont('EBGaramond', 'EBGaramond-Regular.ttf'))
            pdfmetrics.registerFont(TTFont('EBGaramond-Bold', 'EBGaramond-Bold.ttf'))
            self.font_regular = 'EBGaramond'
            self.font_bold = 'EBGaramond-Bold'
        except:
            self.font_regular = 'Times-Roman'
            self.font_bold = 'Times-Bold'
    
    def create_certificate(self, filename, data):
        """Create a certificate PDF with the given data matching the HTML design 100% exactly"""
        c = canvas.Canvas(filename, pagesize=landscape(A4))

        # Get logo position from data, default to 'left'
        logo_position = data.get('logo_position', 'left')

        # Outer container background - #f6f7f9 (exact match from HTML)
        c.setFillColorRGB(0.965, 0.969, 0.976)
        c.rect(0, 0, self.width, self.height, fill=True, stroke=False)

        # Certificate container - inset for border
        # Custom margins: left 50px, top 50px, right 30px, bottom 80px
        margin_left = 40
        margin_top = 40
        margin_right = 20
        margin_bottom = 60
        cert_x = margin_left
        cert_y = margin_bottom
        cert_width = self.width - margin_left - margin_right
        cert_height = self.height - margin_top - margin_bottom

        # Draw certificate with 2px light gray border and white fill
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColor(HexColor('#edeef1'))  # Light gray border
        c.setLineWidth(2)
        c.rect(cert_x, cert_y, cert_width, cert_height, fill=True, stroke=True)

        # Background watermark image (exact HTML proportions: 80% size)
        try:
            if os.path.exists('images/1717996420665_backImage.png'):
                back_img = ImageReader('images/1717996420665_backImage.png')
                back_width = cert_width * 0.8  # Exact HTML: 80%
                back_height = cert_height * 0.8  # Exact HTML: 80%
                back_x = cert_x + (cert_width - back_width) / 2
                back_y = cert_y + (cert_height - back_height) / 2
                c.saveState()
                c.setFillAlpha(0.08)  # Light watermark
                c.drawImage(back_img, back_x, back_y, width=back_width, height=back_height, preserveAspectRatio=True, mask='auto')
                c.restoreState()
        except Exception as e:
            print(f"Background image error: {e}")

        # HmContainer (95% width) with padding - fill more space
        hm_width = cert_width * 0.95
        hm_x = cert_x + (cert_width - hm_width) / 2
        hm_padding = 10  # Reduced padding

        # HmInnerContainer - the bordered area
        # CSS: padding: 2.5rem (about 36 points) - reduced for more content space
        inner_padding = 25
        inner_x = cert_x  # Start from left edge of certificate
        inner_y = cert_y  # Start from top edge of certificate
        inner_width = cert_width  # Certificate width
        inner_height = cert_height

        # All content positions below use inner_x, inner_y, inner_width, inner_height

        # Borders: 2px left, top, bottom (no right) - #edeef1 (exact HTML)
        c.setStrokeColor(HexColor('#edeef1'))
        c.setLineWidth(2)
        # Left border
        c.line(inner_x, inner_y, inner_x, inner_y + inner_height)
        # Top border  
        c.line(inner_x, inner_y + inner_height, inner_x + inner_width, inner_y + inner_height)

        # Content area inside borders - narrow left positioning
        content_x = inner_x + 20  # Reduced left margin for narrow positioning
        content_y = inner_y + inner_padding
        content_width = inner_width - (inner_padding * 2) - 100  # Leave space for right frame

        # Start positioning from top
        current_y = inner_y + inner_height - inner_padding - 10

        # Logo (32px height as per HTML CSS) - narrow left position
        # Draw logo on the left, aligned with the value (description) section
        try:
            if os.path.exists('images/1717996285387_rainlogo.png'):
                logo_img = ImageReader('images/1717996285387_rainlogo.png')
                logo_height = 100
                logo_width = 100
                # Find the y position of the value (description) section
                value_y = current_y - 30 - 25 - 5  # Subtract margins after welcome, name, and underline
                logo_x = content_x  # Align left with value
                c.drawImage(logo_img, logo_x, value_y, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Logo error: {e}")

        current_y -= 60  # Reduced space after logo

        # Certificate title - CSS: font-size: 2.6rem (39pt), color: #f05d24, line-height: 3.8rem (exact HTML)
        # HTML: margin-top: 1.2rem; margin-bottom: -10px
        current_y -= 18  # margin-top: 1.2rem
        c.setFont(self.font_bold, 33)
        c.setFillColor(HexColor('#f05d24'))
        title_text = data['course_title'].upper()
        c.drawString(content_x, current_y, title_text)
        
        current_y -= 25  # Very reduced space to bring welcome text much closer to title
        
        # Certificate clarify text - CSS: font-size: 0.9rem (13.5pt), font-weight: 600, width: 40% (exact HTML)
        c.setFont(self.font_bold, 13.5)  # Exact HTML font size
        c.setFillColor(HexColor('#000000'))
        clarify_text = data['course_sub']
        # Limit width to 40% as per HTML
        max_clarify_width = content_width * 0.4
        if c.stringWidth(clarify_text, self.font_bold, 13.5) > max_clarify_width:
            # Truncate text if too long
            while c.stringWidth(clarify_text + "...", self.font_bold, 13.5) > max_clarify_width and len(clarify_text) > 0:
                clarify_text = clarify_text[:-1]
            clarify_text += "..."
        c.drawString(content_x, current_y, clarify_text)
        
        current_y -= 30  # Increased bottom margin after welcome text
        current_y -= 25  # Reduced space to bring name closer
        
        # Name - CSS: font-size: 2rem (30pt), color: #0d2344, width: 60% (exact HTML)
        c.setFont(self.font_regular, 30)
        c.setFillColor(HexColor('#0d2344'))
        # Capitalize each word
        name_parts = data['name'].split()
        formatted_name = ' '.join([part.capitalize() for part in name_parts])
        
        # Limit width to 60% as per HTML
        max_name_width = content_width * 0.6
        if c.stringWidth(formatted_name, self.font_regular, 30) > max_name_width:
            # Truncate text if too long
            while c.stringWidth(formatted_name + "...", self.font_regular, 30) > max_name_width and len(formatted_name) > 0:
                formatted_name = formatted_name[:-1]
            formatted_name += "..."
        
        c.drawString(content_x, current_y, formatted_name)
        
        # Add space between name and underline
        current_y -= 15  # 15px space
        # Name underline - 
        name_width = c.stringWidth(formatted_name, self.font_regular, 30)
        underline_width = (name_width * 2.2) # horizental line width 
        c.setStrokeColor(HexColor('#0d2344'))
        c.setLineWidth(1)
        c.line(content_x, current_y - 6, content_x + underline_width, current_y - 6)
        
        current_y -= 50  # Margin after name
        
        # Description - CSS: font-size: 0.9rem (13.5pt), font-weight: 500, line-height: 25px (exact HTML)
        c.setFont(self.font_regular, 13.5)  # Exact HTML font size (font-weight: 500 = regular)
        c.setFillColor(HexColor('#000000'))
        
        # Word wrap description
        words = data['value'].split()
        lines = []
        current_line = []
        max_desc_width = content_width * 0.95
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, self.font_regular, 13.5) < max_desc_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw description lines with exact HTML line height
        line_height = 25  # Exact HTML: line-height: 25px
        for line in lines:
            if current_y - line_height < cert_y + inner_padding:
                break  # Prevent overflow
            c.drawString(content_x, current_y, line)
            current_y -= line_height

        # Margin after description
        if current_y - 20 < cert_y + inner_padding:
            current_y = cert_y + inner_padding + 20
        else:
            current_y -= 20

        # Date
        c.setFont(self.font_bold, 13.5)
        c.setFillColor(HexColor('#000000'))
        date_text = f"Date : {data['date']}"
        spaced_date = "".join([char + " " for char in date_text]).strip()
        if current_y - 20 < cert_y + inner_padding:
            current_y = cert_y + inner_padding + 20
        c.drawString(content_x, current_y, spaced_date)
        current_y -= 20

        # Signature section
        sig_x = content_x
        sig_y = max(current_y, cert_y + inner_padding + 60)

        if 'ceo_signature' in data and data['ceo_signature']:
            try:
                if data['ceo_signature'].startswith('http'):
                    response = requests.get(data['ceo_signature'])
                    if response.status_code == 200:
                        sig_img = ImageReader(BytesIO(response.content))
                        c.drawImage(sig_img, sig_x, sig_y - 40, width=120, height=40, preserveAspectRatio=True, mask='auto')
                else:
                    sig_img = ImageReader(data['ceo_signature'])
                    c.drawImage(sig_img, sig_x, sig_y - 40, width=120, height=40, preserveAspectRatio=True, mask='auto')
            except:
                pass

        # CEO name
        ceo_y = sig_y - 55
        c.setFont(self.font_bold, 13.5)
        c.setFillColor(HexColor('#000000'))
        ceo_name = data['ceo_name']
        spaced_ceo_name = "".join([char + " " for char in ceo_name]).strip()
        name_width = c.stringWidth(spaced_ceo_name, self.font_bold, 13.5)
        name_x = sig_x + (120 - name_width) / 2
        c.drawString(name_x, ceo_y, spaced_ceo_name)

        # CEO title
        ceo_title_y = ceo_y - 18
        c.setFont(self.font_regular, 10.5)
        ceo_title = data['ceo_title']
        title_width = c.stringWidth(ceo_title, self.font_regular, 10.5)
        title_x = sig_x + (120 - title_width) / 2
        c.drawString(title_x, ceo_title_y, ceo_title)
        # Add extra white space between CEO title and bottom of certificate
        current_y = ceo_title_y - 30

        # Draw logo in the bottom middle of the certificate page, parallel to CEO name
        try:
            if os.path.exists('images/1717996285387_rainlogo.png'):
                logo_img = ImageReader('images/1717996285387_rainlogo.png')
                logo_width = 100
                logo_height = 100
                logo_center_x = cert_x + (cert_width - logo_width) / 2
                logo_middle_y = ceo_y - (logo_height / 2)  # Centered vertically with CEO name
                c.drawImage(logo_img, logo_center_x, logo_middle_y, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Logo error: {e}")

        # Right decorative frame - restore previous position (not flush with edge)
        try:
            if os.path.exists('images/1717996469308_frame.png'):
                frame_img = ImageReader('images/1717996469308_frame.png')
                frame_height = inner_height
                frame_width = frame_height * 0.25  # Adjust aspect ratio
                frame_x = inner_x + inner_width - frame_width  # Move pattern flush to right border
                frame_y = inner_y
                c.saveState()
                clip_path = c.beginPath()
                clip_path.rect(cert_x, cert_y, cert_width, cert_height)
                c.clipPath(clip_path, stroke=0, fill=0)
                c.drawImage(frame_img, frame_x, frame_y, width=frame_width, height=frame_height, preserveAspectRatio=True, mask='auto')
                c.restoreState()
        except Exception as e:
            print(f"Frame image error: {e}")

        # Right decorative frame - positioned at right edge of inner container (exact HTML)
        # Clip the frame pattern to the certificate area using a path object
            # Right decorative frame - only the latest pattern, flush with right border
            try:
                if os.path.exists('images/1717996469308_frame.png'):
                    frame_img = ImageReader('images/1717996469308_frame.png')
                    frame_height = inner_height
                    frame_width = frame_height * 0.25  # Adjust aspect ratio
                    frame_x = inner_x + inner_width - frame_width  # Flush with right border
                    frame_y = inner_y
                    c.saveState()
                    clip_path = c.beginPath()
                    clip_path.rect(cert_x, cert_y, cert_width, cert_height)
                    c.clipPath(clip_path, stroke=0, fill=0)
                    c.drawImage(frame_img, frame_x, frame_y, width=frame_width, height=frame_height, preserveAspectRatio=True, mask='auto')
                    c.restoreState()
            except Exception as e:
                print(f"Frame image error: {e}")
        
        # Save PDF
        c.save()
        print(f"Certificate created: {filename}")