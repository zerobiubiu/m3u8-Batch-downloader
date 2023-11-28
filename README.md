# m3u8-Batch-downloader

> 基于 N_m3u8DL-RE 的批量下载方案

仅在 Windows11 下使用 Python 3.10.11测试

## 引用库

- openpyxl
- subprocess
- os
- concurrent
- PySide6

## 使用方法

将需要下载的m3u8链接写在 src/downTable.xlsx 第一行为标题行无需改动，从第二行开始读取，左侧列填写链接，右侧列填写下载完毕后的文件名，下载过程在 src/bin/log 目录内查看。

在 Windows 下点击 src 下的 start.bat 启动。

一些意外终止的行为可能会导致 src/tmp 存留下载缓存，可以执行 clean.bat 删除，下载时请不要运行 clean.bat 可能会导致出错。

## 下载参数

`下载链接 --tmp-dir ./tmp --save-dir Download --save-name 文件名`

其他选项在第 32 行自行改动

## 引用项目

[nilaoda/N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)
