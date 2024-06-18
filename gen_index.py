import os


def generate_readme(root_dir):
    # 初始化 README.md 内容
    readme_content = "# 博客目录\n\n"

    # 创建一个字典，以年份为键，存储目录路径列表
    year_dict = {}

    # 遍历根目录下的所有文件和文件夹
    for root, dirs, files in os.walk(root_dir):
        # 如果文件夹中没有文件，跳过该文件夹
        if not files:
            continue

        # 构建文件路径并确保使用正斜杠
        file_path = f'{root}/index.md'.replace(os.sep, '/')
        # 提取年份
        year = file_path.split('/')[1]
        # 获取目录名称
        dir_name = os.path.basename(root)

        # 初始化该年份的目录列表
        if year not in year_dict:
            year_dict[year] = []

        # 添加目录及其路径到对应年份的列表中
        year_dict[year].append((dir_name, file_path))

    # 按年份倒序排序并生成 README 内容
    for year in sorted(year_dict.keys(), reverse=True):
        readme_content += f"### {year}\n"
        for dir_name, file_path in year_dict[year]:
            readme_content += f"- [{dir_name}]({file_path})\n"
        readme_content += "\n"

    # 将生成的内容写入 README.md 文件
    with open(os.path.join('.', "README.md"), "w", encoding="utf-8") as readme_file:
        readme_file.write(readme_content)


# 指定你的博客根目录
blog_root_directory = "_posts/"  # 请将此路径修改为你的博客根目录路径
generate_readme(blog_root_directory)
