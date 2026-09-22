import sys
import os
from vault import Vault
from config import read_config, write_config
from rules import (
    ExcessiveWhitespace,
    TrailingBlankLines,
    HorizontalRule,
    BlankLinesAroundBlocks,
    TabsToSpaces
)

args = sys.argv[1:]
config = read_config()
vault_path = config['vault_path'] or ''
vault = Vault(vault_path) if vault_path else None
rules = [ExcessiveWhitespace(),
         TrailingBlankLines(),
         HorizontalRule(),
         BlankLinesAroundBlocks('code'),
         BlankLinesAroundBlocks('math'),
         TabsToSpaces()]
ignored_paths = config['ignored_paths']
arg_idx = 0

while arg_idx < len(args):
    if args[arg_idx] == '-v' and arg_idx + 1 < len(args):
        vault_path = args[arg_idx + 1]
        arg_idx += 1
        vault = Vault(vault_path)
        print(vault.read(ignored_paths))
    elif args[arg_idx] == '--save':
        if os.path.isdir(vault_path):
            config['vault_path'] = vault_path
            write_config(config)
        else:
            print("The vault must be specified before '--save'")
    elif args[arg_idx] == '--check':
        if vault:
            vault.check(rules)
        else:
            print("The vault must be specified before '--check'")
    elif args[arg_idx] == '--fix':
        if vault:
            vault.fix(rules)
        else:
            print("The vault must be specified before '--fix'")
    elif args[arg_idx] == '-i':
        if arg_idx + 1 < len(args):
            if args[arg_idx + 1] == '-d':
                if arg_idx + 2 >= len(args):
                    print("An index or path must be specified after '-d'")
                elif args[arg_idx + 2].isdigit():
                    del_path_idx = int(args[arg_idx + 2])
                    if del_path_idx in range(len(ignored_paths)):
                        del ignored_paths[del_path_idx]
                        config['ignored_paths'] = ignored_paths
                        write_config(config)
                    else:
                        print('Index is out of range')
                else:
                    if args[arg_idx + 2] in ignored_paths:
                        for i in range(len(ignored_paths)):
                            if ignored_paths[i] == args[arg_idx + 2]:
                                del ignored_paths[i]
                                break
                        config['ignored_paths'] = ignored_paths
                        write_config(config)
                    else:
                        print('Path is not in the list of ignored paths')
                arg_idx += 2
            else:
                ignored_path = args[arg_idx + 1]
                config['ignored_paths'].append(ignored_path)
                write_config(config)
                arg_idx += 1
        else:
            if len(ignored_paths) == 0:
                print('The list of ignored paths is empty')
            else:
                print('Ignored paths:')
                for ignored_path_idx, ignored_path in enumerate(ignored_paths):
                    print('{}) {}'.format(ignored_path_idx, ignored_path))
    else:
        print('Unknown argument:', args[arg_idx])
    arg_idx += 1
