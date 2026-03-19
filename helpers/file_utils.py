# File and directory helpers for Velocitone-Reaper-Toolbar-Icons
import os
import shutil

def ensure_dirs(dirs):
    """
    Ensure all directories in the list exist.
    Args:
        dirs: List of directory paths.
    """
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def copy_pngs(src_dir, dst_dir):
    """
    Copy all PNG files from src_dir to dst_dir.
    Args:
        src_dir: Source directory.
        dst_dir: Destination directory.
    """
    for filename in os.listdir(src_dir):
        if filename.endswith('.png'):
            shutil.copy(os.path.join(src_dir, filename), dst_dir)
