import os
import subprocess
import zipfile
import cairosvg
import pandas as pd
import json
import cv2


def setup_directories():
    # setup directories
    try:
        os.mkdir('res')
        print('created /res directory')
    except OSError:
        print("res/ already exists")


def get_fontawesome():

    # fetch Fontawesome
    fa_name = 'fontawesome-free-6.2.0'
    if len([file for file in os.listdir('res/') if fa_name in file]) == 0:
        subprocess.call(
            ["wget",
             "https://use.fontawesome.com/releases/v6.2.0/fontawesome-free-6.2.0-web.zip",
             "--directory-prefix=res"])
    else:
        print("fontawesome is already downloaded: {}".
              format([file for file in os.listdir('res/') if fa_name in file]))

    # unzip
    fontawesome_dir = ['res/' + file for file in os.listdir('res/') if
                       'fontawesome' in file and '.zip' in file][0]

    with zipfile.ZipFile(fontawesome_dir, "r") as zip_ref:
        zip_ref.extractall("res")

    fontawesome_dir = ['res/' + file for file in os.listdir('res/') if
                       'fontawesome' in file and 'zip' not in file][0]

    print('FontAwesome files saved in: {}'.format(fontawesome_dir))

    # read svg file -> png data
    WIDTH = 512
    HEIGHT = 512
    png_dir = 'res/fontawesome-png'

    try:
        os.mkdir(png_dir)
    except OSError:
        print("{} already exists".format(png_dir))

    files = sorted(os.listdir(os.path.join(fontawesome_dir, 'svgs', 'solid')))

    filenames = [file.split('.svg')[0] for file in files]
    textdescrip = [file.replace('-', ' ') for file in filenames]
    filenames_png = [file + '.png' for file in filenames]

    for file, filename in zip(files, filenames):
        # convert svg to png and resize
        cairosvg.svg2png(url=os.path.join(fontawesome_dir, 'svgs', 'solid',
                                          file),
                         output_width=WIDTH, 
                         output_height=HEIGHT,
                         write_to=os.path.join(png_dir, filename + '.png'))
        # convert to 3 channels and black and white
        img = cv2.imread(os.path.join(png_dir, filename + '.png'),
                         cv2.IMREAD_UNCHANGED)

        if len(img.shape) and img.shape[2] == 4:

            # change black -> white and white -> black
            img[:, :, 0] = 255-img[:, :, 3]
            img[:, :, 1] = 255-img[:, :, 3]
            img[:, :, 2] = 255-img[:, :, 3]
            # remove 4th color channel (4th is alpha channel)
            img = img[:, :, :3]

            cv2.imwrite(os.path.join(png_dir, filename + '.png'), img)
        else:
            print("Image does not have 4 channels; deleting it: {}".
                  format(os.path.join(png_dir, filename + '.png')))
            os.unlink(os.path.join(png_dir, filename + '.png'))

    # create json file with class names and descriptions
    filenames_df = pd.DataFrame({
        # 'file_name' : files,
        'file_name': filenames_png,
        'text': textdescrip})
    filenames_df.tail()

    metadata = []
    for idx, row in filenames_df.iterrows():
        metadata.append({'file_name': row['file_name'],
                         'txt': "black and white SVG icon of {}, fontawesome, nounproject".format(row['text'])})

    metadata_list_of_strs = []
    for item in metadata:
        metadata_list_of_strs.append(json.dumps(item))

    with open(os.path.join(png_dir, 'metadata.txt'), 'w') as f:
        # f.writelines(metadata_list_of_strs)
        for line in metadata_list_of_strs:
            f.write(line + '\n')

    # convert to .jsonl file
    os.rename(os.path.join(png_dir, 'metadata.txt'),
              os.path.join(png_dir, 'metadata.jsonl'))


def get_autodraw():
    autodraw_url = 'https://storage.googleapis.com/autodraw-assets/Autodraw_illustrations.zip'
    # fetch Autodraw

    if len([file for file in os.listdir('res/') if fa_name in file]) == 0:
        subprocess.call(
            ["wget",
             "https://use.fontawesome.com/releases/v6.2.0/fontawesome-free-6.2.0-web.zip",
             "--directory-prefix=res"])
    else:
        print("fontawesome is already downloaded: {}".
              format([file for file in os.listdir('res/') if fa_name in file]))

    # unzip
    fontawesome_dir = ['res/' + file for file in os.listdir('res/') if
                       'fontawesome' in file and '.zip' in file][0]

    with zipfile.ZipFile(fontawesome_dir, "r") as zip_ref:
        zip_ref.extractall("res")

    fontawesome_dir = ['res/' + file for file in os.listdir('res/') if
                       'fontawesome' in file and 'zip' not in file][0]

    print('FontAwesome files saved in: {}'.format(fontawesome_dir))





if __name__ == '__main__':
    setup_directories()
    get_fontawesome()
    get_autodraw()
