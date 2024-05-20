import os
import pandas as pd
import random
import requests

# get current Directory
cwd = os.getcwd()

# read data from Etsy CSV file
df = pd.read_csv('EtsyListingsDownload.csv')
df.fillna("nan", inplace=True)

count = 0

# iterate through each row in the DataFrame
for idx, row in df.iterrows():
    count=count+1

    # Resume functionality, uncomment below line to start from a specific point
    # if count < 200:
    # 	continue

    # extract item details
    desc = row['DESCRIPTION']
    price = row['PRICE']
    tags = row['TAGS']
    material = row['MATERIALS']

    print('working on ' + str(idx+1) + ' item')

    # create a directory for each item based on its title
    dirName = row['TITLE'].replace('/', '|')
    target_dir = cwd + '/data/' + dirName

    # if the directory already exists, append a random number to the directory name
    if os.path.exists(target_dir):
        target_dir = target_dir + str(random.randrange(1, 10000))

    # create the directory
    os.mkdir(target_dir)

    # write item details to separate text files within the item's directory
    if not (desc == 'nan'):
        open(target_dir + '/description.txt', 'w').write(desc)
    if not (price == 'nan'):
        open(target_dir + '/price.txt', 'w').write(str(price))
    if not (tags == 'nan'):
        open(target_dir + '/tags.txt', 'w').write(tags)
    if not (material == 'nan'):
        open(target_dir + '/materials.txt', 'w').write(material)

    # process and download images for the item
    images = row[['IMAGE1', 'IMAGE2', 'IMAGE3', 'IMAGE4', 'IMAGE5', 'IMAGE6', 'IMAGE7', 'IMAGE8', 'IMAGE9', 'IMAGE10']]

    imageCount = 0
    for url in images:

        # if the image URL is not 'nan', download and save the image
        if not (url == 'nan'):
            imageCount = imageCount + 1
            extension = url.split('.')[-1]
            r = requests.get(url, allow_redirects=True)
            open(target_dir + '/' + str(imageCount) + '.' + extension, 'wb').write(r.content)
            r.close()
