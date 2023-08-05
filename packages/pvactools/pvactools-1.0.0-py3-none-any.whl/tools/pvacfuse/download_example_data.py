from lib.download_example_data import *

def define_parser():
    return DownloadExampleData.parser('pvacfuse')

def main(args_input = sys.argv[1:]):
    parser = define_parser()
    args = parser.parse_args(args_input)

    DownloadExampleData(args.destination_directory , 'pvacfuse').execute()

if __name__ == '__main__':
    main()
