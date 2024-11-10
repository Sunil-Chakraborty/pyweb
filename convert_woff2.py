import base64

with open("D:\\PyWeb\\NotoSansBengali-Regular.woff2", "rb") as font_file:
    base64_encoded_data = base64.b64encode(font_file.read()).decode('utf-8')

print(base64_encoded_data)
