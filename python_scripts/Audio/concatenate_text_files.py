"""
Hypothesis:
This script is made to run with the nautilus script VideoTranscriptionOrTranslation where a temp folder is created
if there are several audio fil to transcript. Then all the transcription text files are located into this temp folder

"""

import os, subprocess


def _set_output_file_name(input_files):
    """
    the hypothesis here is that the list of text files always contains as first value the exact name
    of the audio translated with added value _01_transcription. So this one will be used
    :param input_files:
    :return: output_file
    """
    name = input_files[0][:input_files[0].find("_01_")]
    extension = "_transcription.txt"
    print(input_files[0])
    if "translation" in input_files[0]:
        extension = "_translation.txt"
    return name + extension


def concatenate_files(input_files):
    output_file = _set_output_file_name(input_files)
    print(output_file)
    with open(output_file, 'w') as outfile:
        for fname in input_files:
            if os.path.isfile(fname):
                with open(fname, 'r') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Add a newline between files
            else:
                print(f"Warning: {fname} does not exist or is not a file.")
    return output_file


def move_concatenated_file_to_root_folder_and_erase_temp_folder(output_file):
    temp_folder = output_file[::-1][output_file[::-1].find("/"):][::-1]
    root_folder = temp_folder[:-1]
    root_folder = root_folder[::-1][root_folder[::-1].find("/"):][::-1]
    print("{} -- {}".format(temp_folder, root_folder))
    move_file = [
        "mv",
        output_file,
        root_folder,
    ]
    erase_temp_folder = [
        "rm",
        "-R",
        temp_folder,
    ]
    subprocess.Popen(move_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    subprocess.Popen(erase_temp_folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Concatenate several text files into one.')
    parser.add_argument('-f', '--input_files', type=str, help='List of input text files to concatenate')
    args = parser.parse_args()
    input_files = args.input_files.split(",")
    output_file = concatenate_files(input_files)
    move_concatenated_file_to_root_folder_and_erase_temp_folder(output_file)
