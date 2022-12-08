import requests


def LykdatGlobalSearchUrl(ImgUrl):

    url = "https://cloudapi.lykdat.com/v1/global/search"
    payload = {
        "api_key": "7b5ed197ab6134bbd3f10ac57af55444b758c99211c00b2a169c3ba2c165723c",
        "image_url": ImgUrl
    }

    response = requests.post(url, data=payload)

    with open('files/'+"responseUrl.json", "w") as f:
        f.write(response.text)
        # print(response.content)


def LykdatGlobalSearchFile(ImgFile):

    url = "https://cloudapi.lykdat.com/v1/global/search"
    payload = {
        "api_key": "7b5ed197ab6134bbd3f10ac57af55444b758c99211c00b2a169c3ba2c165723c"
    }
    image_file = open(ImgFile, 'rb')

    files = [
        ('image', (ImgFile, image_file, 'image/jpeg'))
    ]

    response = requests.post(url, data=payload, files=files)
    with open('files/'+"responseFile.json", "w") as f:
        f.write(response.text)
        # print(response.content)


def main():
    LykdatGlobalSearchUrl(
        "https://cdn.shopify.com/s/files/1/0293/9277/products/image.jpg")
    LykdatGlobalSearchFile("2.jpeg")


if __name__ == '__main__':
    main()
