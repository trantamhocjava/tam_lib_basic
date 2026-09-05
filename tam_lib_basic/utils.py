import os
import shutil
import zipfile
from pathlib import Path


def zip_folder(src_path):
    """
    Nén toàn bộ file và thư mục con trong src_path
    thành file src_path/main.zip.

    File main.zip sẽ không tự nén chính nó.
    """
    src_path = os.path.abspath(src_path)
    zip_path = os.path.join(src_path, "main.zip")

    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:

        for root, dirs, files in os.walk(src_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Không đưa main.zip vào chính nó
                if os.path.abspath(file_path) == zip_path:
                    continue

                # Giữ nguyên cấu trúc thư mục bên trong src_path
                arcname = os.path.relpath(file_path, src_path)

                zipf.write(file_path, arcname)

    return zip_path


def unzip_and_delete(zip_path):
    """
    Giải nén file .zip thành một thư mục cùng tên
    trong thư mục cha DAD, sau đó xóa file .zip.

    Ví dụ:
        /data/main.zip
    ->
        /data/main/
        /data/main.zip bị xóa
    """
    zip_path = os.path.abspath(zip_path)

    if not zipfile.is_zipfile(zip_path):
        raise ValueError(f"Không phải file ZIP hợp lệ: {zip_path}")

    dad = os.path.dirname(zip_path)

    zip_name = os.path.basename(zip_path)
    folder_name = os.path.splitext(zip_name)[0]

    dst_path = os.path.join(dad, folder_name)

    os.makedirs(dst_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zipf:
        zipf.extractall(dst_path)

    os.remove(zip_path)

    return dst_path


def clear_folder(src_path):
    """
    Xóa tất cả file và thư mục con bên trong src_path.
    Không xóa chính thư mục src_path.
    """
    src_path = os.path.abspath(src_path)

    if not os.path.isdir(src_path):
        raise ValueError(f"Không phải thư mục hợp lệ: {src_path}")

    for name in os.listdir(src_path):
        path = os.path.join(src_path, name)

        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def clear_folder_except(src_path, file_names):
    """
    Xóa tất cả file và thư mục con trực tiếp trong src_path,
    ngoại trừ các file/thư mục có tên nằm trong file_names.

    Quy ước:
    - Phần tử có extension -> file
    - Phần tử không có extension -> thư mục

    Ví dụ:
        file_names = ["a.txt", "b.pdf", "data", "models"]
    """
    src_path = os.path.abspath(src_path)

    if not os.path.isdir(src_path):
        raise ValueError(f"Không phải thư mục hợp lệ: {src_path}")

    keep_names = set(file_names)

    for name in os.listdir(src_path):
        if name in keep_names:
            continue

        path = os.path.join(src_path, name)

        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def move_contents(src_path, des_path):
    """
    Di chuyển tất cả file và thư mục con trực tiếp trong src_path
    sang des_path.

    Không xóa chính thư mục src_path.
    """
    src_path = os.path.abspath(src_path)
    des_path = os.path.abspath(des_path)

    if not os.path.isdir(src_path):
        raise ValueError(f"Không phải thư mục hợp lệ: {src_path}")

    os.makedirs(des_path, exist_ok=True)

    for name in os.listdir(src_path):
        src_item = os.path.join(src_path, name)
        des_item = os.path.join(des_path, name)

        shutil.move(src_item, des_item)


def save_directory_tree(dir_path: str, txt_path: str):
    """
    Phân tích toàn bộ cấu trúc của dir_path và lưu cây thư mục vào txt_path.

    Ví dụ output:
    dir_path/
        |--sub_1/
            |--subsub_1/
            |--file.png
        |--sub_2/
    """
    root = Path(dir_path)
    output_path = Path(txt_path)

    if not root.exists():
        raise FileNotFoundError(f"Không tồn tại thư mục: {dir_path}")

    if not root.is_dir():
        raise NotADirectoryError(f"Không phải thư mục: {dir_path}")

    lines = [f"{root.name}/"]

    def build_tree(current_dir: Path, depth: int):
        items = sorted(
            current_dir.iterdir(), key=lambda x: (x.is_file(), x.name.lower())
        )

        for item in items:
            indent = "    " * depth

            if item.is_dir():
                lines.append(f"{indent}|--{item.name}/")
                build_tree(item, depth + 1)
            else:
                lines.append(f"{indent}|--{item.name}")

    build_tree(root, depth=1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def copy_items(item_list, des_path):
    """
    Với mỗi phần tử trong item_list:

    - Nếu là file:
        a/b/c/d.ext
      -> copy thành:
        des_path/d.ext

    - Nếu là thư mục:
        a/b/c/d
      -> copy toàn bộ thư mục thành:
        des_path/d

    Nếu des_path chưa tồn tại thì tự tạo.
    """
    des_path = os.path.abspath(des_path)
    os.makedirs(des_path, exist_ok=True)

    for item_path in item_list:
        item_path = os.path.abspath(item_path)

        if not os.path.exists(item_path):
            raise FileNotFoundError(f"Không tồn tại: {item_path}")

        item_name = os.path.basename(item_path)
        dst_path = os.path.join(des_path, item_name)

        if os.path.isfile(item_path):
            shutil.copy2(item_path, dst_path)

        elif os.path.isdir(item_path):
            shutil.copytree(item_path, dst_path, dirs_exist_ok=True)

        else:
            raise ValueError(f"Không phải file hoặc thư mục: {item_path}")


def text_to_item_list(text):
    """
    Chuyển text nhiều dòng thành list đường dẫn,
    đồng thời đổi dấu '\\' thành '/'.
    """
    return [
        line.strip().replace("\\", "/") for line in text.splitlines() if line.strip()
    ]


def extract_and_move_file(dir_path, file_name):
    """
    Trong dir_path:
    - Tìm file <tên>.zip
    - Giải nén thành dir_path/<tên>
    - Xóa file .zip
    - Tìm file có extension giống file_name trong thư mục đã giải nén
    - Đổi tên file đó thành file_name
    - Nếu dir_path/file_name đã tồn tại thì xóa
    - Di chuyển file ra dir_path
    - Xóa thư mục giải nén

    Parameters
    ----------
    dir_path : str | Path
        Đường dẫn thư mục.

    file_name : str
        Tên file đầu ra, ví dụ: "abc.pdf"
    """

    dir_path = Path(dir_path)

    # Extension cần tìm, ví dụ ".pdf"
    ext = Path(file_name).suffix

    # Tìm đúng 1 file .zip trong dir_path
    zip_files = list(dir_path.glob("*.zip"))

    if len(zip_files) != 1:
        raise ValueError(
            f"Yêu cầu dir_path có đúng 1 file .zip, nhưng tìm thấy {len(zip_files)} file."
        )

    zip_path = zip_files[0]

    # <tên>.zip -> <tên>
    extract_dir = dir_path / zip_path.stem

    # Nếu thư mục giải nén cũ đã tồn tại thì xóa trước
    if extract_dir.exists():
        shutil.rmtree(extract_dir)

    # Giải nén
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    # Xóa file zip
    zip_path.unlink()

    # Tìm file có extension EXT trong toàn bộ thư mục đã giải nén
    matched_files = [
        p
        for p in extract_dir.rglob("*")
        if p.is_file() and p.suffix.lower() == ext.lower()
    ]

    if len(matched_files) != 1:
        raise ValueError(
            f"Yêu cầu có đúng 1 file extension '{ext}' trong {extract_dir}, "
            f"nhưng tìm thấy {len(matched_files)} file."
        )

    source_file = matched_files[0]

    # File đích
    target_file = dir_path / file_name

    # Nếu dir_path/file_name đã tồn tại thì xóa
    if target_file.exists():
        if target_file.is_file() or target_file.is_symlink():
            target_file.unlink()
        else:
            shutil.rmtree(target_file)

    # Đổi tên FILE thành file_name ngay trong thư mục giải nén
    renamed_file = source_file.with_name(file_name)
    source_file.rename(renamed_file)

    # Di chuyển ra dir_path
    shutil.move(str(renamed_file), str(target_file))

    # Xóa thư mục giải nén
    shutil.rmtree(extract_dir)

    return str(target_file)



def clean_file_name(file_name):
    result = file_name.strip()
    return result