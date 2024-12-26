#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os

def run_mmpbsa(tpr_file, xtc_file, ndx_file, protein_group, ligand_group, interval=1):
    """
    运行s_mmpbsa分析
    参数:
        tpr_file: MD模拟的tpr文件
        xtc_file: 轨迹文件
        ndx_file: 索引文件
        protein_group: 蛋白质组的编号
        ligand_group: 配体组的编号
        interval: 分析间隔(ns)
    """
    
    
    s_mmpbsa_path = os.getenv('S_MMPBSA_PATH', '/home/suwenbin/package/s_mmpbsa/s_mmpbsa')
    
    
    if not os.path.exists(s_mmpbsa_path):
        print(f"Error: s_mmpbsa not found at {s_mmpbsa_path}")
        sys.exit(1)
    if not os.access(s_mmpbsa_path, os.X_OK):
        print(f"Error: s_mmpbsa is not executable at {s_mmpbsa_path}")
        sys.exit(1)

    
    commands = f"""
{tpr_file}
1
{xtc_file}
2
{ndx_file}
0
1
{protein_group}
2
{ligand_group}
5
{interval}
0
0

1
2
3

1
4
0
""".strip().split('\n')

    
    process = subprocess.Popen([s_mmpbsa_path], 
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             text=True)
    
   
    output, error = process.communicate('\n'.join(commands))
    
    if process.returncode != 0:
        print(f"Error running s_mmpbsa: {error}")
        sys.exit(1)
    
    print(output)

def main():
    parser = argparse.ArgumentParser(description='Run s_mmpbsa analysis automatically')
    parser.add_argument('-t', '--tpr', required=True, help='Input tpr file')
    parser.add_argument('-x', '--xtc', required=True, help='Input xtc file')
    parser.add_argument('-n', '--ndx', required=True, help='Input ndx file')
    parser.add_argument('-p', '--protein', required=True, type=int, help='Protein group number')
    parser.add_argument('-l', '--ligand', required=True, type=int, help='Ligand group number')
    parser.add_argument('-i', '--interval', type=float, default=1, help='Analysis interval in ns (default: 1)')
    
    args = parser.parse_args()
    
    run_mmpbsa(args.tpr, args.xtc, args.ndx, args.protein, args.ligand, args.interval)

if __name__ == "__main__":
    main() 