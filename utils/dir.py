import os
import platform
import subprocess
from pathlib import Path

def open_dir():

    target_dir = "./video"

    # 确定目标目录路径
    path = Path(target_dir) if target_dir else Path.cwd()
    path = path.expanduser().resolve()  # 处理 ~ 并转为绝对路径

    if not path.exists():
        raise FileNotFoundError(f"目录不存在: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"路径不是目录: {path}")

    # 根据操作系统执行打开命令
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(str(path))
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(path)], check=True)
        elif system == "Linux":
            subprocess.run(["xdg-open", str(path)], check=True)
        else:
            raise OSError(f"不支持的操作系统: {system}")
    except Exception as e:
        raise RuntimeError(f"打开目录失败: {e}") from e