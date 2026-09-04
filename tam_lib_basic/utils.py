import os
import shutil
import zipfile


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
