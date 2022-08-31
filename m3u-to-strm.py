from ipytv import playlist
import os
import argparse
import pdb

def save_strm(filename, url):
    with open(filename, 'w') as f:
        f.write(url)

def main():
    for entry in m3u:
        if entry.attributes:
            folder = os.path.join(args.DB, entry.attributes['group-title'])
            os.makedirs(folder, exist_ok=True)
            strm_file = os.path.join(folder, entry.attributes.get('tvg-name', entry.name) + '.strm')
            save_strm(strm_file, entry.url)
        else:
            print(entry)
            folder = os.path.join(args.DB, 'unkown')
            os.makedirs(folder, exist_ok=True)
            strm_file = os.path.join(folder, entry.name + '.strm')
            save_strm(strm_file, entry.url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IPTV playlist checker.')
    parser.add_argument('playlist', type=str, help='playlist for check')
    parser.add_argument('--DB', type=str, help="DB prefix")
    args = parser.parse_args()
    m3u = playlist.loadf(args.playlist)
    main()
