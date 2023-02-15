from sys import argv
import re


def sbv2lrc(sbv):
    '''
    param. sbv
    return. lrc
    '''
    # let it be lrc style: HH:MM:SS.xxx, HH:MM:SS.xxx -> [MM:SS.xxx]
    lrc = re.sub(r'(\d+):(\d+):(\d+)\.(\d+),(\d+):(\d+):(\d+)\.(\d+)\n(.+)\n',
                            r'[\2:\3.\4]\9\n', sbv)
    
    # process the multi-line problem
    lines = lrc.split('\n')
    for i in range(len(lines)):
        if lines[i] == '':
            continue
        if lines[i][0] != '[':
            lines[i-1] += (' ' + lines[i])
    lrc = str()
    for line in lines:
        if line == '' or '[0' not in line:
            continue
        lrc += (line+'\n')

    return lrc

def srt2lrc():
    lrc = ''
    return lrc
def vtt2lrc():
    lrc = ''
    return lrc

def main():
    if len(argv) != 2:
        print('input file plz.')

    input_path = argv[1]
    mode = ''
    for _mode in ['sbv','srt','vtt']:
        if _mode in input_path:
            mode = _mode

    converter = {
        'sbv':sbv2lrc,
        'srt':srt2lrc,
        'vtt':vtt2lrc
    }

    with open(input_path,'r',encoding='utf-8') as f:
        lines = f.readlines()
    
    lrc = converter[mode](input_path)
    output_path = input_path[:-3] + 'lrc'
    with open(output_path,'w',encoding='utf-8') as f:
        f.writelines(lrc)

# if __name__ == '__main__':
#     main()