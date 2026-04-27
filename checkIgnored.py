import os
import re
import argparse


def is_there_gitignore(project_dir):
    return ".gitignore" in os.listdir(project_dir)


def get_gitignore_content(project_dir):
    rules = []
    gitignore_path = os.path.join(project_dir, ".gitignore")

    # читаем gitignore построчно
    with open(gitignore_path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            rules.append(line)

    return rules


def check_pattern(relative_path, pattern):
    # если шаблон со звездочкой, то проверяем через regex
    if pattern[0] == "*":
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = regex_pattern.replace("*", ".*")
        return re.search(regex_pattern + "$", relative_path) is not None

    # иначе это обычный путь
    return relative_path == pattern


def get_all_ignored_files(project_dir):
    if not is_there_gitignore(project_dir):
        return []

    result = []
    patterns = get_gitignore_content(project_dir)
    project_name = os.path.basename(os.path.abspath(project_dir))

    # обходим все файлы в папке проекта
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            absolute_file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(absolute_file_path, project_dir)
            relative_file_path = relative_file_path.replace("\\", "/")

            for pattern in patterns:
                if check_pattern(relative_file_path, pattern):
                    full_file_path = project_name + "/" + relative_file_path
                    result.append(
                        f"{full_file_path} ignored by expression {pattern}"
                    )
                    break

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="путь до папки"
    )
    parser.add_argument("--project_dir", required=True)
    args = parser.parse_args()
    project_dir = args.project_dir

    # проверяем, что такая папка существует
    if not os.path.isdir(project_dir):
        raise Exception(f"Неправильная директирия: {project_dir}.")

    ignored_files = get_all_ignored_files(project_dir)

    print("Ignored files:")
    for file in ignored_files:
        print(file)
