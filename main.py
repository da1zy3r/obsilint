import sys

def check():
    pass

def fix():
    pass

args = sys.argv[1:]
vault_path = ''
arg_idx = 0

while arg_idx < len(args):
    if args[arg_idx] == '-v' and arg_idx + 1 < len(args):
        vault_path = args[arg_idx + 1]
        arg_idx += 1
    elif args[arg_idx] == '--check':
        check()
    elif args[arg_idx] == '--fix':
        fix()
    else:
        print('Unknown argument:', args[arg_idx])
    arg_idx += 1
