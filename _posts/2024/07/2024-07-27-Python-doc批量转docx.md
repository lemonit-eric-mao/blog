---
title: "Python-doc批量转docx"
date: "2024-07-27"
categories: 
  - "python"
---



> 此工具需要在操作系统上安装 LibreOffice，并指定它的可执行文件
> 这个工具是免费的，如果电脑上有现成的Office，可是不使用这个工具

``` python
import asyncio
import os
import shutil
from asyncio import Semaphore

from logger import Logger

# 配置日志
logger = Logger()

# 限制并发数量
SEMAPHORE_LIMIT = 10
semaphore = Semaphore(SEMAPHORE_LIMIT)

input_directory_path = "./doc"
output_directory_path = "./docx"
if not os.path.isdir(output_directory_path):
    os.makedirs(output_directory_path)

# 失败文件夹路径
failed_files_directory = "./failed_files"
if not os.path.isdir(failed_files_directory):
    os.makedirs(failed_files_directory)


async def convert_doc_to_docx(input_path, output_path):
    libreoffice_path = r'D:\Program Files\LibreOffice\program\soffice.exe'
    logger.info(f"开始转换文件: {input_path} -> {output_path}")

    async with semaphore:
        try:
            process = await asyncio.create_subprocess_exec(
                libreoffice_path, '--headless', '--convert-to', 'docx', input_path, '--outdir', output_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                logger.info(f"转换成功: {input_path} -> {output_path}")
            else:
                logger.error(f"转换失败 {input_path}: {stderr.decode()}")
                # 复制失败的文件到指定文件夹
                shutil.copy(input_path, failed_files_directory)
                logger.info(f"文件已复制到失败文件夹: {input_path}")
        except Exception as e:
            logger.error(f"转换过程中出现异常 {input_path}: {e}")
            # 复制失败的文件到指定文件夹
            shutil.copy(input_path, failed_files_directory)
            logger.info(f"文件已复制到失败文件夹: {input_path}")


async def convert_docs_in_directory(input_directory, output_directory):
    input_directory = os.path.abspath(input_directory)
    output_directory = os.path.abspath(output_directory)

    logger.info(f"输入目录: {input_directory}")
    logger.info(f"输出目录: {output_directory}")

    if not os.path.isdir(input_directory):
        logger.error("输入目录不存在。")
        return

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    doc_files = [f for f in os.listdir(input_directory) if f.endswith(".doc")]

    tasks = []
    for file_name in doc_files:
        input_path = os.path.join(input_directory, file_name)
        output_path = output_directory
        tasks.append(convert_doc_to_docx(input_path, output_path))

    await asyncio.gather(*tasks)


# 运行主程序
asyncio.run(convert_docs_in_directory(input_directory_path, output_directory_path))

```
