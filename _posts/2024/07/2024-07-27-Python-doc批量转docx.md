

> 此工具需要在操作系统上安装 LibreOffice，并指定它的可执行文件
> 这个工具是免费的，如果电脑上有现成的Office，可是不使用这个工具

``` python
import os
import subprocess


def convert_doc_to_docx(input_path, output_path):
    # 使用 LibreOffice 的完整路径
    libreoffice_path = r'D:\Program Files\LibreOffice\program\soffice.exe'
    print(f"转换文件: {input_path} -> {output_path}")

    # 确保 output_path 是文件夹的路径，而不是包含文件名
    result = subprocess.run(
        [libreoffice_path, '--headless', '--convert-to', 'docx', input_path, '--outdir', output_path],
        capture_output=True, text=True)

    # 打印 LibreOffice 执行结果，帮助调试
    print(result.stdout)
    print(result.stderr)


def convert_docs_in_directory(input_directory, output_directory):
    # 将相对路径转换为绝对路径
    input_directory = os.path.abspath(input_directory)
    output_directory = os.path.abspath(output_directory)

    # 打印调试信息
    print(f"输入目录: {input_directory}")
    print(f"输出目录: {output_directory}")

    if not os.path.isdir(input_directory):
        print("输入目录不存在。")
        return

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith(".doc"):
            input_path = os.path.join(input_directory, file_name)
            # 使用 output_directory 来指定输出目录，而不是文件路径
            try:
                convert_doc_to_docx(input_path, output_directory)
                # 输出文件的完整路径
                output_file_path = os.path.join(output_directory, file_name.replace(".doc", ".docx"))
                print(f"转换成功: {input_path} -> {output_file_path}")
            except Exception as e:
                print(f"转换失败 {input_path}: {e}")


input_directory_path = "./files"
output_directory_path = "./docx"
convert_docs_in_directory(input_directory_path, output_directory_path)

```
