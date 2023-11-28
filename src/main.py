import os
import openpyxl
import subprocess
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtWidgets import QApplication, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget, QTextEdit

# 获取当前脚本所在的目录
script_directory = os.path.dirname(os.path.abspath(__file__))

# Excel的位置
excelPath = os.path.join(script_directory, "downTable.xlsx")

# 设置核心执行程序的位置
cli_program = os.path.join(script_directory, "bin", "N_m3u8DL-RE.exe ")

# 读取下载列表,列表元素为一个元组{'url'：xxx, 'name': xxx, 'command': xxx}
def read_download_list(path, program):
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
def def_task_count():
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("提示")

    # 创建布局
    layout = QVBoxLayout(window)

    # 放置文本提示
    label = QLabel("并行任务数量")
    layout.addWidget(label)

    # 默认三个任务同时跑
    res = 3

    # 不知道为啥要加event参数, 不加跑不通
    def change(value):
        nonlocal res
        res = combo_box.currentText()

    # 放置下拉框
    combo_box = QComboBox()
    combo_box.currentIndexChanged.connect(change)
    combo_box.addItems([str(i) for i in range(1, 33)])
    combo_box.setCurrentIndex(2)  # 设置默认选择为3
    layout.addWidget(combo_box)

    # 放置按钮
    button = QPushButton('确认')
    button.clicked.connect(window.close)
    layout.addWidget(button)

    # 显示窗口
    window.show()
    app.exec_()

    return int(res)

# 将下载任务提交到线程池
def exe_download(a_list, count):
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

# 获取下载列表
download_list = read_download_list(excelPath, cli_program)

# 获取并行任务数量
task_count = def_task_count()

# 提交下载任务到线程池
exe_download(download_list, task_count)
