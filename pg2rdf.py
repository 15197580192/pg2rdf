import csv
import os
import argparse

def csv_to_nt(csv_file, nt_file):
    triples = []
    # 打开CSV文件读取数据
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        
        # 生成NT三元组并保存到列表中
        row_number = 0
        for row in reader:
            row_number += 1
            subject = f"{os.path.basename(csv_file).split('.')[0]}_{row_number}"
            for field in fieldnames:
                predicate = field
                obj = row[field].replace(' ', '')  # 将值中的空格删除
                triples.append(f"<{subject}> <{predicate}> <{obj}> .\n")
    
    # 将三元组写入NT文件
    with open(nt_file, 'w', encoding='utf-8') as ntfile:
        ntfile.writelines(triples)
    
    return triples

def process_csv_folder(input_folder, output_folder):
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)
    
    all_nt_path = os.path.join(output_folder, "all.nt")
    # 确保all.nt文件存在，并清空它
    with open(all_nt_path, 'w', encoding='utf-8') as all_nt_file:
        all_nt_file.write('')

    # 遍历输入文件夹中的所有CSV文件
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(input_folder, file_name)
            nt_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.nt")
            triples = csv_to_nt(csv_file_path, nt_file_path)
            print(f"Processed {csv_file_path} -> {nt_file_path}")
            
            # 将每个文件的三元组追加到all.nt文件
            with open(all_nt_path, 'a', encoding='utf-8') as all_nt_file:
                all_nt_file.writelines(triples)
    
    print(f"Processed all data -> {all_nt_path}")

def main():
    parser = argparse.ArgumentParser(description='Convert CSV files in a folder to NT files.',usage='python3 %(prog)s input_folder output_folder')
    parser.add_argument('input_folder', type=str, help='Path to the input folder containing CSV files.')
    parser.add_argument('output_folder', type=str, help='Path to the output folder to save NT files.')

    args = parser.parse_args()

    process_csv_folder(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
