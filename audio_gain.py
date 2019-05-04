import os
import subprocess
import multiprocessing
import pathlib
import time

def get_list_of_videos():
    dirpath = os.getcwd()
    list_of_files = os.listdir(dirpath)
    list_of_paths = [os.path.join(dirpath, filename) for filename in list_of_files]
    suffix_list = ['.MOV', '.mp4', '.mov', '.flv', '.avi', '.m4v']
    return [video_path for video_path in list_of_paths if get_file_suffix(video_path) in suffix_list]

def get_file_suffix(path):
    return pathlib.Path(path).suffix

def process_videos(dirpath, list_of_videos, gain):
    output_path = os.path.join(dirpath, "processed")
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for index, video_file in enumerate(list_of_videos):
        process_video(output_path, video_file, gain, index, len(list_of_videos))

    print('-----------------------------------------------')
    print('Done!')

def process_video(outpath, video_file, gain, index, length):
    print('-----------------------------------------------')
    print('Processing ' + video_file +': ' + str(index + 1) + ' of ' + str(length))
    
    outfile = os.path.join(outpath, os.path.basename(video_file))
    cmd = ['ffmpeg', '-i', video_file, '-vcodec', 'copy', '-af', 'volume=' + str(gain) + 'dB',
           '-y', outfile] #-y to overwrite file
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    if proc.poll() is None:
        print_output(proc, index, length)
        

def get_output(proc):
    o, e = proc.communicate()
    output = o.decode('utf-8')
    error = e.decode('utf-8')
    return [output, error]

def print_output(proc, index, length):
    std = get_output(proc)
    if std[0]:
        output = std[0]
        print('-----------------------------------------------')
        print('Output: ' + output)
    if std[1]:
        error = std[1]
        print('-----------------------------------------------')
        print('Error: ' + error)
    print('-----------------------------------------------')
    print('Done ' + str(index + 1) + ' of ' + str(length))

gain = '-'
while (not gain.isdigit() and gain != ''):
    gain = input('Set Gain (default 25) ')
gain = gain or 25
list_of_videos = get_list_of_videos()
process_videos(os.getcwd(), list_of_videos, gain)

