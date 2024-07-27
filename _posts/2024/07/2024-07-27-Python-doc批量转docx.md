---
title: "Python-doc批量转docx"
date: "2024-07-27"
categories: 
  - "python"
---



> 此工具需要在操作系统上安装 LibreOffice，并指定它的可执行文件。
> 
> 这个工具是免费的，如果电脑上有现成的Office，可以不使用这个工具。
> 
> 已经尝试使用批量转换了，但LibreOffice不支持并发。

``` python
import os
import shutil
import subprocess

from logger import Logger

# 配置日志
logger = Logger()


def convert_doc_to_docx(input_path, output_path, failed_path):
    """
    将单个 DOC 文件转换为 DOCX
    """
    libreoffice_path = r'D:\Program Files\LibreOffice\program\soffice.exe'

    try:
        process = subprocess.run(
            [libreoffice_path, '--headless', '--convert-to', 'docx', input_path, '--outdir', output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # 使用文本模式来方便调试
            check=True  # 当命令返回非零状态码时抛出异常
        )

        if process.returncode == 0:
            logger.info(f"转换成功: {input_path} -> {output_path}")
        else:
            logger.error(f"转换失败: {input_path} -> {failed_path}")
            handle_failed_conversion(input_path, failed_path)
    except subprocess.CalledProcessError as e:
        logger.error(f"转换过程中出现异常: {input_path} -> {failed_path} \n {e}")
        handle_failed_conversion(input_path, failed_path)


def handle_failed_conversion(input_path, failed_path):
    """
    处理转换失败的文件，将其复制到失败文件夹
    """
    shutil.copy(input_path, failed_path)


def convert_docs_in_directory(input_directory, output_directory, failed_directory):
    """
    批量转换目录中的 DOC 文件
    """

    for file_name in os.listdir(input_directory):
        if file_name.endswith(".doc"):
            input_path = os.path.join(input_directory, file_name)
            convert_doc_to_docx(input_path, output_directory, failed_directory)


# 运行主程序
if __name__ == "__main__":

    # 文件夹路径
    INPUT_DIRECTORY = os.path.abspath("./doc")
    OUTPUT_DIRECTORY = os.path.abspath("./docx")
    FAILED_DIRECTORY = os.path.abspath("./failed_files")
    logger.debug(f"输入目录: {INPUT_DIRECTORY}")
    logger.debug(f"输出目录: {OUTPUT_DIRECTORY}")
    logger.debug(f"失败目录: {FAILED_DIRECTORY}")

    # 确保目录存在
    for directory in [INPUT_DIRECTORY, OUTPUT_DIRECTORY, FAILED_DIRECTORY]:
        if not os.path.isdir(directory):
            os.makedirs(directory)

    convert_docs_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY, FAILED_DIRECTORY)

```
