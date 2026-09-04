import shutil
from pathlib import Path


def move_wav_to_folder(src_path, des_path):
    """
    src_path chứa:
        1.wav
        2.wav
        3.wav
        ...

    des_path chứa:
        1/
        2/
        3/
        ...

    Di chuyển:
        src_path/1.wav -> des_path/1/1.wav
        src_path/2.wav -> des_path/2/2.wav
        ...
    """

    src_path = Path(src_path)
    des_path = Path(des_path)

    for wav_path in src_path.glob("*.wav"):
        index = wav_path.stem

        target_dir = des_path / index

        if not target_dir.is_dir():
            print(f"Bỏ qua {wav_path.name}: không có thư mục {target_dir}")
            continue

        target_path = target_dir / wav_path.name

        shutil.move(str(wav_path), str(target_path))

        print(f"Đã di chuyển: {wav_path} -> {target_path}")
