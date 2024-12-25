#!/usr/bin/env python3
import argparse

def extract_sections(input_file, output_file):
    try:
        with open(input_file, 'r') as source:
            lines = source.readlines()
            
        output = []
        remaining = []  
        i = 0
        
        while i < len(lines) and "; Include forcefield parameters" not in lines[i]:
            remaining.append(lines[i])
            i += 1
            
        if i < len(lines):
            while i < len(lines) and "[ moleculetype ]" not in lines[i]:
                output.append(lines[i])
                i += 1
            output.append('\n')
            
        while i < len(lines) and "; Include water topology" not in lines[i]:
            remaining.append(lines[i])
            i += 1
            
        if i < len(lines):
            output.extend(lines[i:])
        
        with open(output_file, 'w') as target:
            target.writelines(output)
            
        with open(input_file, 'w') as source:
            source.writelines(remaining)
            
        print(f"Successfully extracted sections to {output_file} and updated source file")
            
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}")
    except PermissionError:
        print(f"Error: Permission denied when accessing files")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Extract specific sections from a topology file')
    parser.add_argument('-i', '--input', required=True, help='Input topology file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    args = parser.parse_args()
    extract_sections(args.input, args.output)

if __name__ == "__main__":
    main()