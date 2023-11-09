import openpyxl
import os
import subprocess


# 获取当前脚本所在的目录
script_directory = os.path.dirname(os.path.abspath(__file__))

# Excel的位置
excelPath = script_directory + "/downTable.xlsx"

# 打开一个Excel文件
workbook = openpyxl.load_workbook(excelPath)

# 选择工作表
sheet = workbook.active

# 设置核心执行程序的位置
cli_program = script_directory + "\\bin\\N_m3u8DL-RE.exe "

# 使用iter_rows()方法遍历工作表的行
for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
    if row_index == 1:
        continue  # 跳过标题行
    command = [
        cli_program,
        str(row[0]),
        "--tmp-dir",
        "./tmp",
        "--save-dir",
        "Download",
        "--save-name",
        str(row[1]),
    ]
    subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

# 关闭工作簿
workbook.close()
