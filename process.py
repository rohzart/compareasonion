import imgkit
import json
from urllib.parse import urlparse
import os

with open('compareasonion.config.json', 'r') as cf:
    config = json.load(cf)

options = config["imgkit"]["options"]
# additional options: 'width': 400, 'disable-smart-width': ''

alloweddomains = config["alloweddomains"]

imgkitconfig = imgkit.config(
    wkhtmltoimage=config["imgkit"]["wkhtmltoimagepath"])

with open(config["inputfilepath"], 'r') as fp:
    records = json.load(fp)

records_json = {}
for page_name in records:
    print(f'Processing: {page_name}')
    counter = 0
    urls_json = []
    for url in records[page_name]:
        domain = ''
        image_path = ''
        error = ''
        if url == '':
            error = 'error: no page url provided'
        try:
            result = urlparse(url)
        except Exception as e:
            print(e)
            error = f'error: urlparse > {url}'
        domain = result.netloc
        if not domain in alloweddomains:
            error = f'error: invalid domain: {domain}'
        if error == '':
            if all([result.scheme, result.netloc, result.path]):
                counter = counter + 1
                page_name = page_name.replace(' ', '_')
                image_path = f'{config["outputdir"]}/{page_name}_{str(counter)}.png'
                if os.path.exists(image_path):
                    print('image exists')
                else:
                    try:
                        print(url)
                        imgkit.from_url(url, image_path, options=options, config=imgkitconfig)
                    except Exception as e:
                        # if os.path.exists(image_path):
                        #     os.remove(image_path)
                        #     print('error occurred, image removed')
                        error = f'error: imgkit processing {url} > {e}'
            else:
                error = f'error: invalid url: {url}'

        urls_json.append(
            {"url": url, "image_path": image_path, "error": error})
    records_json[page_name] = urls_json

with open(config["outputjsonpath"], 'w') as outfile:
    json.dump(records_json, outfile)

cf.close()
fp.close()
outfile.close()

print('---OVER---')
