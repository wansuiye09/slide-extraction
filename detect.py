from pytube import YouTube
import argparse
import os
import shutil
import subprocess as sp
import client
from constants import paths
from constants import defaults

ARGS = None
SPLIT_IMAGES = paths.TEMP_DIR + '/input/'

def create_dirs_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def detect(url):
    yt = YouTube(url)
    yt.set_filename('input')
    vid = yt.get('mp4', '360p')
    create_dirs_if_not_exists(paths.DATA_DIR)
    create_dirs_if_not_exists(paths.SLIDES_DIR)
    print 'Starting video download....'
    try:
        os.remove(paths.DATA_DIR + '/input.mp4')
    except:
        pass
    vid.download(paths.DATA_DIR)
    print 'Video download finished'
    try:
        shutil.rmtree(SPLIT_IMAGES)
    except OSError:
        pass
    create_dirs_if_not_exists(SPLIT_IMAGES)
    print 'Splitting video into images'
    command = ['ffmpeg', '-n', '-i', paths.DATA_DIR + '/input.mp4',
               '-vf', 'fps=1',
               SPLIT_IMAGES + '%d.jpeg']
    sp.call(command)
    print 'Images extracted from the video'
    input_images = os.listdir(SPLIT_IMAGES)

    total_images = len(input_images)
    for index, image in enumerate(input_images):
        print image
        val = client.main(SPLIT_IMAGES + image)
        if val > 0.5:
            shutil.copy2(SPLIT_IMAGES + image, paths.SLIDES_DIR)
        else:
            shutil.copyfile(SPLIT_IMAGES + image, './noslides/' + image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--url',
        type=str,
        default='',
        help='Url of the youtube video you want to extract slides from'
    )
    ARGS, unparsed = parser.parse_known_args()
    if not ARGS.url:
        raise ValueError('Pass in the url of the youtube video you want to parse slides from in the --url arg')
    detect(ARGS.url)
