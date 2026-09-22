#!/usr/bin/env python3
"""把 tools/help-card.html 渲染成 assets/help.png。

依赖：本机的 Edge 或 Chrome（无头模式）+ Pillow。
用法：python tools/build-help.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "help-card.html")
OUT = os.path.join(ROOT, "assets", "help.png")

PAGE_WIDTH = 880          # 与 help-card.html 里 body 的宽度一致
SCALE = 2                 # 2 倍图，发到群里放大也清晰
RENDER_HEIGHT = 2600      # 先渲染得足够高，之后按内容裁掉多余部分
MARGIN = 36               # help-card.html 里 .card 的外边距，裁切时保留
LUMA_THRESHOLD = 60       # 比这更亮就算“有内容”，用来找内容底部

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/microsoft-edge",
    "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_browser():
    for path in BROWSERS:
        if os.path.exists(path):
            return path
    for name in ("msedge", "google-chrome", "chromium", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("找不到 Edge / Chrome，请在脚本里补上浏览器路径。")


def render(browser, dest):
    profile = tempfile.mkdtemp(prefix="fftip-help-")
    url = "file:///" + SRC.replace("\\", "/")
    cmd = [
        browser,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-dev-shm-usage",
        "--no-first-run",
        "--hide-scrollbars",
        "--force-device-scale-factor=%d" % SCALE,
        "--user-data-dir=%s" % profile,
        "--window-size=%d,%d" % (PAGE_WIDTH, RENDER_HEIGHT),
        "--virtual-time-budget=2500",
        "--screenshot=%s" % dest,
        url,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    shutil.rmtree(profile, ignore_errors=True)


def crop(img):
    """按内容底部裁掉多余空白，上下保留同样的外边距。"""
    mask = img.convert("L").point(lambda v: 255 if v > LUMA_THRESHOLD else 0)
    box = mask.getbbox()
    if not box:
        return img, None
    bottom = min(box[3] + MARGIN * SCALE, img.height)
    return img.crop((0, 0, img.width, bottom)), box


def main():
    if not os.path.exists(SRC):
        sys.exit("找不到 %s" % SRC)

    tmp_png = os.path.join(tempfile.mkdtemp(prefix="fftip-shot-"), "help.png")
    render(find_browser(), tmp_png)

    img = Image.open(tmp_png).convert("RGB")
    raw_size = img.size
    img, box = crop(img)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    # 画面是纯色块 + 细字，256 色调色板几乎看不出来差别，体积却小一半
    img.quantize(colors=256, method=Image.MEDIANCUT).save(OUT, "PNG", optimize=True)

    print("渲染尺寸 %dx%d -> 输出 %dx%d" % (raw_size[0], raw_size[1], img.width, img.height))
    print("内容范围 %s，输出 %s（%.0f KB）" % (box, OUT, os.path.getsize(OUT) / 1024))
    if box and box[3] >= raw_size[1] - 5:
        print("提示：内容可能被渲染高度截断，请调大 RENDER_HEIGHT。")


if __name__ == "__main__":
    main()
