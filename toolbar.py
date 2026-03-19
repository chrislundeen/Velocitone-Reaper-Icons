# Entry point for Velocitone-Reaper-Toolbar-Icons
import os
import json
from helpers.icon_generator import generate_icons
from helpers.file_utils import copy_pngs

def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    generate_icons(config)
    # Copy PNGs to REAPER Data directory if enabled
    if config.get('copyFiles', False):
        print('Copying .png files to REAPER Data directory')
        reaper_data_dir = os.path.expanduser(config['reaperDataDir'])
        output_dir = os.path.join(os.getcwd(), 'output')
        output_dir_png_toolbar_icons = os.path.join(output_dir, 'png', 'toolbar_icons')
        output_dir_png150 = os.path.join(output_dir_png_toolbar_icons, '150')
        output_dir_png200 = os.path.join(output_dir_png_toolbar_icons, '200')
        output_dir_png_track_icons_custom = os.path.join(output_dir, 'png', 'track_icons', 'Custom')
        reaper_dir_png_toolbar_icons = os.path.join(reaper_data_dir, 'toolbar_icons')
        reaper_dir_png150 = os.path.join(reaper_dir_png_toolbar_icons, '150')
        reaper_dir_png200 = os.path.join(reaper_dir_png_toolbar_icons, '200')
        reaper_dir_png_track_icons_custom = os.path.join(reaper_data_dir, 'track_icons', 'Custom')
        copy_pngs(output_dir_png_toolbar_icons, reaper_dir_png_toolbar_icons)
        copy_pngs(output_dir_png150, reaper_dir_png150)
        copy_pngs(output_dir_png200, reaper_dir_png200)
        copy_pngs(output_dir_png_track_icons_custom, reaper_dir_png_track_icons_custom)

if __name__ == '__main__':
    main()
