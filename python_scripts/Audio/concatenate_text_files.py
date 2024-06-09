import os


def _set_output_file_name(input_files):
    """
    the hypothesis here is that the list of text files always contains as first value the exact name
    of the audio translated without added values. So this one will be used
    :param input_files:
    :return: output_file
    """
    return input_files[0][:input_files[0].find(".")] + "_all.txt"


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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Concatenate several text files into one.')
    parser.add_argument('-f', '--input_files', type=str, help='List of input text files to concatenate')
    args = parser.parse_args()
    input_files = args.input_files.split(",")
    concatenate_files(input_files)
