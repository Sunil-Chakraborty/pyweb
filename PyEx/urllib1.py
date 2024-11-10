import urllib.request

fhand = urllib.request.urlopen('https://example-files.online-convert.com/document/txt/example.txt')
for line in fhand:
    print(line.decode().strip())