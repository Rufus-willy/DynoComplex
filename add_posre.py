#!/usr/bin/env python3
import argparse

def add_posre_files(posre_list, topol_file):
    try:
        with open(topol_file, 'r') as f:
            lines = f.readlines()

        
        for posre_file in posre_list:
            
           
            mol_name = posre_file.split('_')[1].split('.')[0]
            itp_file = f"{mol_name}.itp"
            
            
            for i, line in enumerate(lines):
                if f'#include "{itp_file}"' in line:
                   
                    posre_text = f"\n; Position restraint for {mol_name}\n"
                    posre_text += f"#ifdef POSRES_{mol_name.upper()}\n"
                    posre_text += f"#include \"{posre_file}\"\n"
                    posre_text += "#endif\n"
                    
                    
                    lines.insert(i + 1, posre_text)
                    break
            else:
                print(f"Warning: Could not find include line for {itp_file}")

        
        with open(topol_file, 'w') as f:
            f.writelines(lines)

        print(f"Successfully added {len(posre_list)} position restraint files to {topol_file}")
        print("Added files:", ", ".join(posre_list))

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Add position restraint files to topology file')
    parser.add_argument('-l', '--posre_list', required=True, nargs='+', help='List of position restraint files to add')
    parser.add_argument('-p', '--topol', required=True, help='Topology file to modify')
    
    args = parser.parse_args()
    add_posre_files(args.posre_list, args.topol)

if __name__ == "__main__":
    main() 