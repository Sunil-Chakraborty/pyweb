import os
from PIL import Image, ImageDraw, ImageFont

# Create image with text
def text_to_image(text, font_path='NotoSansBengali-Regular.ttf'):
    try:
        font = ImageFont.truetype(font_path, 40)
    except Exception as e:
        print(f"Error loading font: {e}")
        return

    print(os.path.exists(font_path))  # This should return True

    # Create a temporary image to get text size
    temp_img = Image.new('RGB', (1, 1))
    d = ImageDraw.Draw(temp_img)

    # Calculate the bounding box of the text
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]  # right - left
    text_height = bbox[3] - bbox[1]  # bottom - top
    
    # Create an image with adequate size
    img = Image.new('RGB', (text_width + 20, text_height + 20), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Draw the text on the image
    d.text((10, 10), text, font=font, fill=(0, 0, 0))
    img.save('text_image.png')

text_to_image("পাশ্চাত্যের সমসাময়িক বিবর্তনের কুঝ্যাটিকা  কেমন মাঠে দেখা হলো বল । কিরে চিনতে পারলি। বল কোথায় যেন দেখেছি।  কেমন যেন চেনা চেনা লাগছে। হ্যা  রে। নকশা মারিস না , চিনলে কিরে  বলে ধাক্কা মার্তি। কতদিন বাদে দেখা , আমার কি দোষ। ")  # Bengali text
