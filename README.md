# m3u8-Batch-downloader
> 基于 N_m3u8DL-RE 的批量下载方案

仅在 Windows11 下使用 Python 3.10.11测试过

引用库：

- openpyxl
- subprocess
- os

将需要下载的m3u8链接写在 src/downTable.xlsx 即可，第一行为标题行无需改动，从第二行开始读取，左侧列填写链接，右侧列填写下载完毕后的文件名，下载过程中无提示，下载过程在bin目录内的log查看。

## 下载参数

`下载链接 --tmp-dir ./tmp --save-dir Download --save-name 文件名`

如需修改在main,py第35行修改

## 引用项目

[nilaoda/N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)
