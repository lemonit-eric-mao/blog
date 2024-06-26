import os
import re


def update_markdown_images(directory):
    # 遍历指定文件夹中的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 使用正则表达式进行替换
                updated_content = re.sub(r'\[\!\[\]\(images/(.*?)\)\]\(http*.*?\)', r'![](images/\1)', content)

                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)


# 指定你的Markdown文件所在目录
markdown_directory = '_posts'
update_markdown_images(markdown_directory)


