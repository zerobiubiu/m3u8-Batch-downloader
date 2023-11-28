import os
import subprocess
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk

import openpyxl

# 获取当前脚本所在的目录
script_directory = os.path.dirname(os.path.abspath(__file__))

# Excel的位置
excelPath = script_directory + "/downTable.xlsx"

# 设置核心执行程序的位置
cli_program = script_directory + "\\bin\\N_m3u8DL-RE.exe "


# 读取下载列表,列表元素为一个元组{'url'：xxx, 'name': xxx, 'command': xxx}
def readDownloadList(path, program):
    empty_file_name = "未命名-"
    # 打开一个Excel文件
    workbook = openpyxl.load_workbook(path)
    # 选择工作表
    sheet = workbook.active
    # 定义一个列表用于存放读取结果
    downloader_list = []
    for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
        # 跳过标题行和空行
        if row_index == 1 or row[0] is None:
            continue
        url = str(row[0])
        # 处理没有命名下载文件名称的场景
        name = empty_file_name + url if row[1] is None else str(row[1])
        command = [
            program,
            url,
            "--tmp-dir",
            "./tmp",
            "--save-dir",
            "Download",
            "--save-name",
            name,
        ]
        downloader_list.append({"url": url, "name": name, "command": command})
    # 读取完成后关闭工作簿
    workbook.close()
    return downloader_list


# 自定义并行任务个数，默认为3
def defTaskCount():
    window = tk.Tk()
    # 窗口居中
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    box_width = 200
    box_height = 40
    offset_left = (screen_width - box_width) / 2
    offset_top = (screen_height - box_height) / 2
    window.title("提示")
    window.geometry("%dx%d+%d+%d" % (200, 40, offset_left, offset_top))

    # 放置文本提示
    tk.Label(window, text="并行任务数量").place(x=4, y=6)
    # 默认三个任务同时跑
    res = 3

    # 不知道为啥要加event参数, 不加跑不通
    def change(event):
        nonlocal res
        res = cbox.get()

    # 放置下拉框
    cbox = ttk.Combobox(window, width=4)
    cbox.bind('<<ComboboxSelected>>', change)
    cbox.place(x=90, y=6)
    # 自定义下载任务数量
    cbox['value'] = (1, 2, 3, 4, 5)
    cbox.current(2)

    # 放置按钮
    tk.Button(window, text='确认', pady=0, relief=tk.GROOVE, command=window.destroy).place(x=150, y=4)
    window.mainloop()
    return res


# 将下载任务提交到线程池
def exeDownload(a_list, count):
    pool = ThreadPoolExecutor(max_workers=count, thread_name_prefix="worker_")
    for index, item in enumerate(a_list):
        pool.submit(download, item)


# 执行下载操作
def download(item_list):
    try:
        process = subprocess.Popen(item_list["command"], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        print(item_list["name"] + " 开始下载!")
        while process.poll() is None:
            pass
        print(item_list["name"] + " 下载完成！")
        process.kill()
    except Exception:
        print(item_list["name"] + " 下载失败！")


# step1: 获取下载列表
# step2: 确定并行下载任务数量
# step3: 提交下载任务
d_list = readDownloadList(excelPath, cli_program)
task_count = int(defTaskCount())
exeDownload(d_list, task_count)
