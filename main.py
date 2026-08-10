import sys
from vault import Vault

args = sys.argv[1:]
vault_path = ''
vault = None
arg_idx = 0

while arg_idx < len(args):
    if args[arg_idx] == '-v' and arg_idx + 1 < len(args):
        vault_path = args[arg_idx + 1]
        arg_idx += 1
        vault = Vault(vault_path)
        print(vault.read())
    elif args[arg_idx] == '--check':
        if vault:
            vault.check()
        else:
            print("The vault must be specified before '--check'")
    elif args[arg_idx] == '--fix':
        if vault:
            vault.fix()
        else:
            print("The vault must be specified before '--fix'")
    else:
        print('Unknown argument:', args[arg_idx])
    arg_idx += 1
