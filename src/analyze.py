import numpy as np
import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def write_report(filename, oldest, largest, mine, others):
    """
    with open(filename, "w") as f:
        f.write("FILE REPORT\n")
        f.write("=" * 60 + "\n\n")

        f.write("10 OLDEST FILES\n")
        f.write("-" * 60 + "\n")
        f.write(oldest.to_string(index=False))
        f.write("\n\n")

        f.write("10 LARGEST FILES\n")
        f.write("-" * 60 + "\n")
        f.write(largest.to_string(index=False))
        f.write("\n\n")

        f.write("MY FILES (no group write)\n")
        f.write("-" * 60 + "\n")
        f.write(mine.to_string(index=False))
        f.write("\n\n")

        f.write("OTHER USERS' FILES (no group write)\n")
        f.write("-" * 60 + "\n")
        f.write(others.to_string(index=False))
        f.write("\n")
    """
    print("\n\n")
    print(bcolors.HEADER + "======================FILE REPORT======================\n" + bcolors.ENDC)
    print(bcolors.OKBLUE + "-------------------10 OLDEST DIRECTORIES---------------------\n" + bcolors.ENDC)
    oldest["size"] = oldest["size"].apply(humanbytes)
    print(oldest)
    print("\n\n")
    print(bcolors.OKBLUE + "------------------10 LARGEST DIRECTORIES---------------------\n" + bcolors.ENDC)
    largest["size"] = largest["size"].apply(humanbytes)
    print(largest)
    print("\n\n")
    print(bcolors.OKBLUE + "--------------MY DIRECTORIES (no group write)----------------\n" + bcolors.ENDC)
    mine["size"] = mine["size"].apply(humanbytes)
    print(mine)
    print("\n\n")
    print(bcolors.OKBLUE + "--------OTHER USERS' DIRECTORIES (no group write)------------\n" + bcolors.ENDC)
    others["size"] = others["size"].apply(humanbytes)
    print(others)
    print(bcolors.HEADER + "=======================================================\n" + bcolors.ENDC)
    print("\n\n")

def humanbytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)

def main():
    colnames = ["permissions", "owner", "last-access", "size", "path"]
    df = pd.read_csv("slurm_output/find_output.csv", names=colnames, header=None)
    
    oldest = df.sort_values(by='last-access',ascending=True).head(10)
    largest = df.sort_values(by='size',ascending=False).head(10)

    df_n_gw = df[df["permissions"].str[5] != "w"] # Find paths with no group write permissions

    user = os.environ['USER']

    mine = df_n_gw[df_n_gw["owner"] == user].head(20) # They belong to me and have no group write
    others = df_n_gw[df_n_gw["owner"] != user].head(20) # They belong to someone else and have to group write
    
    output_dir = os.environ['HOME']
    output_path = os.path.join(output_dir, "gpfs_data_summary.txt")

    write_report(output_path, oldest, largest, mine, others)

if __name__ == '__main__':
    main()

