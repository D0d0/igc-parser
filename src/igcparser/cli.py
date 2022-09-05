from igcparser import IgcParser


def main(args):
    print(args)
    print(IgcParser.parse(args.file_path))
