"""README 기능 테스트 표의 썸네일(docs/images/tests/tXX.png)을 원본 캡처에서 다시 만듭니다.

원본 캡처의 윗부분을 4:3 비율로 잘라 840x630으로 줄입니다. 원본이 4:3보다 납작하면(가로로 긴 캡처)
잘리지 않도록 위아래에 여백을 붙입니다.

사용법 (저장소 루트에서):
    pip install pillow
    python docs/make_thumbs.py            # 아래 표의 원본이 있는 것만 전부 다시 생성
    python docs/make_thumbs.py t02 t09    # 일부만 다시 생성
"""
import sys
from pathlib import Path

from PIL import Image

IMAGES = Path(__file__).resolve().parent / "images"
SIZE = (840, 630)  # 4:3

# 썸네일 이름 → 원본 캡처 (README 7장 기능 테스트 표와 같은 짝)
SOURCES = {
    "t01": "t01_health.png",
    "t02": "analysis.png",
    "t03": "t03_webcam.png",
    "t04": "admin_predictions.png",
    "t05": "t05_async.png",
    "t06": "history.png",
    "t07": "t07_forbidden.png",
    "t08": "dashboard.png",
    "t09": "failure.png",
    "t10": "t10_restart.png",
}


def make_thumb(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    target_ratio = SIZE[0] / SIZE[1]
    if w / h <= target_ratio:
        # 세로로 긴 캡처: 위쪽부터 4:3만큼 자름 (중요한 내용이 보통 위에 있음)
        im = im.crop((0, 0, w, round(w / target_ratio)))
    else:
        # 가로로 긴 캡처: 자르지 않고 위아래 여백을 원본 왼쪽 위 픽셀 색으로 채움
        canvas_h = round(w / target_ratio)
        canvas = Image.new("RGB", (w, canvas_h), im.getpixel((0, 0)))
        canvas.paste(im, (0, (canvas_h - h) // 2))
        im = canvas
    im.resize(SIZE, Image.LANCZOS).save(dst, optimize=True)


def main(names: list[str]) -> None:
    (IMAGES / "tests").mkdir(exist_ok=True)
    for name in names or SOURCES:
        src = IMAGES / SOURCES[name]
        if not src.exists():
            print(f"건너뜀 {name}: 원본 {src.name} 없음")
            continue
        make_thumb(src, IMAGES / "tests" / f"{name}.png")
        print(f"생성 {name}.png ← {src.name}")


if __name__ == "__main__":
    main(sys.argv[1:])
