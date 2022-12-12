import os
import sys
import subprocess
import tkinter
from tkinter import filedialog
import cv2
import math
from datetime import datetime
from progress.bar import ShadyBar


start_time = datetime.now()
path_to_file = ""

width = 150
height = 0
compress = True


def main() -> None:
    frames = get_vid()

    # code for progress bar
    bar = ShadyBar("Calculating Frames", max=len(frames))

    output_list = []
    for frame in frames:
        frame = turn_image_grey(frame)
        if compress:
            output_list.append(calculate_with_compression(frame, bar))
        else:
            output_list.append(calculate(frame, bar))
    safe_to_html(output_list)
    exit()


def get_vid() -> list:
    video_frames = []
    global path_to_file
    # remove tk root window
    tkinter.Tk().withdraw()
    # open file selection window
    path_to_file = filedialog.askopenfilename(filetypes=[("Image of Video files", ".png .jpg .jpeg .mp4 .wav .mkv")],
                                              title="Select a photo or video.")
    # exit program if no file is selected
    if not path_to_file:
        exit("No file selected.")

    # check if file is image
    if path_to_file.endswith(".png") or path_to_file.endswith(".jpg") or path_to_file.endswith(".jpeg"):
        img = cv2.imread(path_to_file)
        img_height, img_width, _ = img.shape
        video_frames.append([img, img_width, img_height])
        return video_frames

    video_capture = cv2.VideoCapture(path_to_file)

    success, image = video_capture.read()
    count = 0
    while success:
        img_height, img_width, _ = image.shape
        video_frames.append([image, img_width, img_height])
        success, image = video_capture.read()
        count += 1
    return video_frames


def turn_image_grey(file: list) -> list:
    file[0] = cv2.cvtColor(file[0], cv2.COLOR_RGB2GRAY)
    return file


def calculate(file: list, bar: ShadyBar) -> str:
    tile_size = math.floor(file[1] / width)

    output = ""

    global height
    height = math.floor(file[2] / tile_size)

    for y in range(height):
        line = ""
        for x in range(width):
            tile_pos = [x * tile_size, y * tile_size]
            line += calculate_tile(file, tile_pos, tile_size)
        output += line + "<br>"

    bar.next()
    return "<p>" + output + "</p>"


def calculate_with_compression(file: list, bar: ShadyBar) -> str:
    tile_size = math.floor(file[1] / width)

    output = ""

    global height
    height = math.floor(file[2] / tile_size)

    comp_char = ""
    comp_char_number = 0
    for y in range(height):
        for x in range(width):
            tile_pos = [x * tile_size, y * tile_size]
            this_char = calculate_tile(file, tile_pos, tile_size)

            # if compression char number is less than one, set it and the char and continue
            if comp_char_number < 1:
                comp_char = this_char
                comp_char_number = 1
                continue

            if this_char == comp_char:
                comp_char_number += 1
            else:
                # write last char
                output += comp_char + str(comp_char_number) + "*"
                # save new char
                comp_char = this_char
                comp_char_number = 1

        # add last char
        if y == height - 1:
            output += comp_char + str(comp_char_number) + "*"
            continue

    bar.next()
    return output


def calculate_tile(file: list, tile_pos: list, tile_size: int) -> str:
    chars = ["W", "W", "W", "@", "#", "N", "$", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0", "?", "!", "a", "b",
             "c", ";", ":", "+", "=", "_", "-", ",", ".", ".", "."]
    scale = [0, 255]
    step = (scale[1] - scale[0]) / len(chars)

    cropped_img = file[0][tile_pos[1]:tile_pos[1] + tile_size, tile_pos[0]:tile_pos[0] + tile_size]
    brightness = sum(map(sum, cropped_img)) / (tile_size * tile_size)

    for i, x in enumerate(chars):
        if brightness < step * (i + 1):
            return chars[i]

    return chars[0]


def safe_to_html(output: list) -> None:
    save_path = os.path.dirname(os.path.realpath(__file__)) + "/file-to-text/"

    # check if path exists, if not: create it
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # create new html file and write html code into it
    new_file = open(os.path.join(save_path, make_filename()), "w", encoding="utf-8")
    new_file.write(create_html_string_from_template(output))
    new_file.close()
    # show final file
    open_file(save_path)


def open_file(filename):
    # from https://stackoverflow.com/questions/17317219/is-there-an-platform-independent-equivalent-of-os-startfile
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def create_html_string_from_template(frames: list) -> str:
    frames_js = ""
    for frame in frames:
        frames_js += "'" + frame + "', "

    # open template file
    template_file = open("html_template.html", "r")
    # load template content
    template = template_file.read()
    # close template file
    template_file.close()
    # insert frames
    out = template.replace("VAR_frames_js_VAR", frames_js)
    # insert number of frames
    out = out.replace("VAR_frames_len_VAR", str(len(frames) - 1))
    # insert width
    out = out.replace("VAR_frames_width_VAR", str(width))
    # insert height
    out = out.replace("VAR_frames_height_VAR", str(height))
    # insert if file was compressed
    out = out.replace("VAR_compressed_VAR", str(compress).lower())

    return out


def get_filename() -> str:
    name = str(os.path.basename(path_to_file)).split(".")[0]
    name = name.replace(" ", "-")
    name = name.replace("_", "-")
    return name


def get_runtime() -> str:
    runtime = str(datetime.now() - start_time)
    runtime = runtime.split(".")[0]
    runtime = runtime[2:]
    runtime = runtime.replace(":", "-")
    return runtime


def make_filename() -> str:
    return get_filename() + "-(x" + str(width) + ")--runtime-" + get_runtime() + "s.html"


def get_user_input() -> None:
    print("\nConfigure width and frame rate of output file or skip.")
    usr_x_res = input("Change default width of 150 characters? -> ")

    global width
    if usr_x_res.isnumeric() and 9 < int(usr_x_res):
        width = int(usr_x_res)

    print("\nIf the file contains few bigger, same colored spots, disable compression.")
    disable_compression = input("Disable compression? (Y/N)").lower()

    global compress
    if disable_compression == "y":
        compress = False

    main()


if __name__ == '__main__':
    get_user_input()
