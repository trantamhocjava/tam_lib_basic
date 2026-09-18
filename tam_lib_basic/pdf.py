from pathlib import Path

from pypdf import PdfReader, PdfWriter


def split_pdf(file_path: str, dir_path: str) -> None:
    """
    Chia một file PDF thành nhiều file PDF,
    mỗi file chứa đúng 1 trang.

    Output:
        page_1.pdf
        page_2.pdf
        ...
    """
    file_path = Path(file_path)
    dir_path = Path(dir_path)

    # Tạo thư mục output nếu chưa tồn tại
    dir_path.mkdir(parents=True, exist_ok=True)

    # Đọc file PDF
    reader = PdfReader(file_path)

    # Tách từng trang
    for page_index, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)

        output_path = dir_path / f"page_{page_index}.pdf"

        with open(output_path, "wb") as output_file:
            writer.write(output_file)


def extract_pdf_pages(
    file_path: str,
    start_page: int,
    end_page: int,
    des_path: str,
) -> None:
    """
    Lấy các trang từ start_page đến end_page trong file PDF
    và lưu vào des_path.

    Quy ước:
    - Trang đầu tiên của file PDF là trang 1.
    - start_page và end_page đều được tính inclusive.
    - Không dựa vào số trang được in bên trong nội dung PDF.

    Ví dụ:
        start_page=2, end_page=5
        -> lấy trang vật lý 2, 3, 4, 5.
    """

    file_path = Path(file_path)
    des_path = Path(des_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    if start_page < 1:
        raise ValueError("start_page phải >= 1")

    if end_page < start_page:
        raise ValueError("end_page phải >= start_page")

    reader = PdfReader(file_path)
    total_pages = len(reader.pages)

    if end_page > total_pages:
        raise ValueError(
            f"end_page={end_page} vượt quá tổng số trang của PDF "
            f"({total_pages} trang)"
        )

    writer = PdfWriter()

    # reader.pages dùng index bắt đầu từ 0,
    # trong khi start_page/end_page của hàm bắt đầu từ 1.
    for page_index in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_index])

    # Tạo thư mục cha của des_path nếu chưa tồn tại
    des_path.parent.mkdir(parents=True, exist_ok=True)

    with open(des_path, "wb") as output_file:
        writer.write(output_file)
