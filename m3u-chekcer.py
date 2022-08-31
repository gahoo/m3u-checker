from ipytv import playlist
from ipytv.doctor import M3UDoctor, M3UPlaylistDoctor
from ffmpy import FFprobe, FFRuntimeError
from subprocess import PIPE
from termcolor import colored, RESET
import re
import sys
import pdb
import progressbar
import argparse
import atexit

ERASE_LINE = '\033[K'

SKIP_FFPROBE_MESSAGES = [re.compile(pattern) for pattern in (
            'Last message repeated',
            'mmco: unref short failure',
            'number of reference frames .+ exceeds max',
             )]

def is_url_valid(url):
    try:
        ffprobe = FFprobe(inputs={url: '-v warning'})
        errors = tuple(filter(
                lambda line: not (line in ('', RESET) or any(regex.search(line) for regex in SKIP_FFPROBE_MESSAGES)),
                ffprobe.run(stderr=PIPE)[1].decode('utf-8').split('\n')
        ))
    except FFRuntimeError:
        return False

    if errors:
        return False
    else:
        return True

@atexit.register
def save_on_exit():
    content = m3u.to_m3u_plus_playlist()
    args.out.write(content)

@atexit.register
def save_log_on_exit():
    content = failed.to_m3u_plus_playlist()
    args.log.write(content)

def main():
    bar = progressbar.ProgressBar(max_value=m3u.length())
    for i, entry in enumerate(m3u):
        bar.update(i)
        if not is_url_valid(entry.url):
            failed.append_channel(entry)
            m3u.remove_channel(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IPTV playlist checker.')
    parser.add_argument('playlist', type=str, help='playlist for check')
    parser.add_argument('--out', type=argparse.FileType('w'), default=sys.stdout, help="filename")
    parser.add_argument('--log', type=argparse.FileType('a'), default=sys.stderr, help="filename")
    args = parser.parse_args()
    m3u = playlist.loadf(args.playlist)
    failed = playlist.M3UPlaylist()
    main()
