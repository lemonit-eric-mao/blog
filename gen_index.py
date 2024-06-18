import os


def generate_readme(root_dir):
    # 初始化 README.md 内容
    readme_content = "# 博客目录\n\n"

    # 遍历根目录下的所有文件和文件夹
    for root, dirs, files in os.walk(root_dir):
        # 如果文件夹中没有文件，跳过该文件夹
        if not files:
            continue

        # 提取目录名称（例如：2017-11）
        dir_name = os.path.basename(root)
        readme_content += f"## {dir_name}\n\n"

        # 遍历目录中的所有文件
        for file in files:
            # 只处理 .md 文件
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                # 使用文件名（去掉 .md 扩展名）作为标题
                file_title = os.path.splitext(file)[0]
                readme_content += f"- [{file_title}]({file_path})\n"

        readme_content += "\n"

    # 将生成的内容写入 README.md 文件
    with open(os.path.join(root_dir, "README.md"), "w", encoding="utf-8") as readme_file:
        readme_file.write(readme_content)


# 指定你的博客根目录
blog_root_directory = "./pages"  # 请将此路径修改为你的博客根目录路径
generate_readme(blog_root_directory)
