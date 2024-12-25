#!/usr/bin/env python3
import argparse
import re

def add_itp_files(itp_list, topol_file):
    try:
        with open(topol_file, 'r') as f:
            lines = f.readlines()

        atomtypes_start = -1
        atomtypes_end = -1
        water_start = -1
        
        
        in_atomtypes = False
        for i, line in enumerate(lines):
            if '[ atomtypes ]' in line:
                atomtypes_start = i
                in_atomtypes = True
                continue
            
            if in_atomtypes and line.strip() and not line.startswith(';'):
                if not any(c.isalnum() for c in line):
                    atomtypes_end = i
                    break
                last_atomtype_line = i
            
            if '; Include water topology' in line:
                water_start = i
                if atomtypes_end == -1:
                    atomtypes_end = last_atomtype_line + 1
                break
        
        if atomtypes_start == -1 or water_start == -1:
            raise ValueError("Could not find proper insertion points in topology file")

        
        new_lines = []
        for itp_file in itp_list:
            new_lines.append(f'\n; Include {itp_file} topology\n')
            new_lines.append(f'#include "{itp_file}"\n')
        new_lines.append('\n')

        
        #lines.insert(atomtypes_end + 1, ''.join(new_lines))
        lines.insert(atomtypes_end, ''.join(new_lines))
        
        with open(topol_file, 'w') as f:
            f.writelines(lines)

        print(f"Successfully added {len(itp_list)} ITP files to {topol_file}")
        print("Added files:", ", ".join(itp_list))

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Add ITP files to topology file')
    parser.add_argument('-l', '--itp_list', required=True, nargs='+', help='List of ITP files to add')
    parser.add_argument('-p', '--topol', required=True, help='Topology file to modify')
    
    args = parser.parse_args()
    add_itp_files(args.itp_list, args.topol)

if __name__ == "__main__":
    main() 