def normalize_url(url):
    if not url.startswith(('https://', 'http://', 'www.')):
        return 'https://' + url
    elif url.startswith('http://'):
        return 'https://' + url[7:]
    elif url.startswith('www.'):
        return 'https://' + url[4:]
    else:
        return url

with open('list.txt', 'r') as file:
    urls = [line.strip() for line in file]

normalized_urls = [normalize_url(url) for url in urls]

with open('list.txt', 'w') as file:
    file.write('\n'.join(normalized_urls))