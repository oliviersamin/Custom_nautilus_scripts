import os


def concatenate_files(input_files, output_file):
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
    parser.add_argument('input_files', metavar='N', type=str, nargs='+', help='List of input text files to concatenate')
    parser.add_argument('output_file', type=str, help='Output file name')

    args = parser.parse_args()

    concatenate_files(args.input_files, args.output_file)
