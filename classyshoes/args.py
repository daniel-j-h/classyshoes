from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


# User-provided command line arguments
def mkArguments(description):
    parser = ArgumentParser(description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--shopURL', default='https://api.zalando.com', help='shop API URL')
    parser.add_argument('--locale', default='de-DE', help='locale for shop to use')
    parser.add_argument('--whoami', default='ClassyShoes', help='client name to send')
    parser.add_argument('--timeout', default=0.1, help='timeout between subsequent requests')
    parser.add_argument('--verbose', action='store_true', help='be more verbose with logging')
    parser.add_argument('--model', default='model.p3', help='local Pickle3 model cache')
    parser.add_argument('--storage', default='storage.sqlite3', help='local SQLite3 storage')

    return parser.parse_args()
