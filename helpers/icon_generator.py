# Icon generation logic for Velocitone-Reaper-Toolbar-Icons
import os
import cairosvg
from PIL import Image
from helpers.svg_utils import get_core, wrap_svg
from helpers.file_utils import ensure_dirs

def generate_icons(config):
    """
    Orchestrate the icon generation process: SVG composition, PNG export.
    Args:
        config: Loaded config dict.
    """
    paths = _get_paths(config)
    ensure_dirs(paths['all_output_dirs'])
    svg_header, svg_footer = _load_svg_header_footer(paths)
    backgrounds, icons = _get_backgrounds_and_icons(paths)
    _generate_svgs(paths, backgrounds, icons, svg_header, svg_footer, config)
    _convert_svgs_to_pngs(paths)

def _get_paths(config):
    """Return all relevant paths as a dict."""
    cwd = os.getcwd()
    lego_dir = config['legoDir']
    theme_name = config['themeName']
    icon_ingredients = os.path.join(cwd, 'assets')
    paths = {
        'theme_name': theme_name,
        'ingredient_wrapper_dir': os.path.join(icon_ingredients, 'svg', lego_dir, 'wrapper'),
        'ingredient_background_dir': os.path.join(icon_ingredients, 'svg', lego_dir, 'backgrounds'),
        'ingredient_tools_dir': os.path.join(icon_ingredients, 'svg', lego_dir, 'tools'),
        'output_dir': os.path.join(cwd, 'output'),
        'output_dir_svg': os.path.join(cwd, 'output', 'svg'),
        'output_dir_toolbar_svg': os.path.join(cwd, 'output', 'svg', 'toolbar'),
        'output_dir_track_svg': os.path.join(cwd, 'output', 'svg', 'track'),
        'output_dir_png': os.path.join(cwd, 'output', 'png'),
        'output_dir_png_toolbar_icons': os.path.join(cwd, 'output', 'png', 'toolbar_icons'),
        'output_dir_png150': os.path.join(cwd, 'output', 'png', 'toolbar_icons', '150'),
        'output_dir_png200': os.path.join(cwd, 'output', 'png', 'toolbar_icons', '200'),
        'output_dir_png_track_icons': os.path.join(cwd, 'output', 'png', 'track_icons'),
        'output_dir_png_track_icons_custom': os.path.join(cwd, 'output', 'png', 'track_icons', 'Custom'),
    }
    paths['all_output_dirs'] = [
        paths['output_dir'], paths['output_dir_svg'], paths['output_dir_toolbar_svg'],
        paths['output_dir_track_svg'], paths['output_dir_png'], paths['output_dir_png_toolbar_icons'],
        paths['output_dir_png150'], paths['output_dir_png200'], paths['output_dir_png_track_icons'],
        paths['output_dir_png_track_icons_custom']
    ]
    return paths

def _load_svg_header_footer(paths):
    """Load SVG header and footer from files."""
    with open(os.path.join(paths['ingredient_wrapper_dir'], 'header.svg')) as f:
        header = f.read()
    with open(os.path.join(paths['ingredient_wrapper_dir'], 'footer.svg')) as f:
        footer = f.read()
    return header, footer

def _get_backgrounds_and_icons(paths):
    """Return lists of background and icon names (no .svg extension)."""
    backgrounds = [f[:-4] for f in os.listdir(paths['ingredient_background_dir']) if f.endswith('.svg')]
    icons = [f[:-4] for f in os.listdir(paths['ingredient_tools_dir']) if f.endswith('.svg')]
    return backgrounds, icons

def _generate_svgs(paths, backgrounds, icons, svg_header, svg_footer, config):
    """Generate SVG files for all backgrounds and icons."""
    for cb in backgrounds:
        with open(os.path.join(paths['ingredient_background_dir'], cb + '.svg')) as svg_background_file:
            svg_bkgd_string = get_core(svg_background_file)
            svg_background_off = wrap_svg(90, 0, svg_bkgd_string, 'off', config)
            svg_background_over = wrap_svg(90, 100, svg_bkgd_string, 'over', config)
            svg_background_on = wrap_svg(90, 200, svg_bkgd_string, 'on', config)
            svg_background = svg_background_off + svg_background_over + svg_background_on
            svg_background_track = wrap_svg(90, 0, svg_bkgd_string, 'track', config)
        # Write toolbar and track backgrounds
        with open(os.path.join(paths['output_dir_toolbar_svg'], paths['theme_name'] + cb + '.svg'), 'w') as svg_icon_file:
            svg_icon_file.write(svg_header + svg_background + svg_footer)
        with open(os.path.join(paths['output_dir_track_svg'], paths['theme_name'] + cb + '.svg'), 'w') as svg_icon_file:
            svg_icon_file.write(svg_header + svg_background_track + svg_footer)
        for ci in icons:
            with open(os.path.join(paths['ingredient_tools_dir'], ci + '.svg')) as svg_tool_file:
                svg_tool_string = get_core(svg_tool_file)
                svg_tool = wrap_svg(60, 0, svg_tool_string, 'track', config)
                svg_tool_off = wrap_svg(60, 0, svg_tool_string, 'off', config)
                svg_tool_over = wrap_svg(60, 100, svg_tool_string, 'over', config)
                svg_tool_on = wrap_svg(60, 200, svg_tool_string, 'on', config)
                with open(os.path.join(paths['output_dir_toolbar_svg'], paths['theme_name'] + cb + '_' + ci + '.svg'), 'w') as svg_icon_file:
                    svg_icon_file.write(svg_header + svg_background + svg_tool_off + svg_tool_over + svg_tool_on + svg_footer)
                with open(os.path.join(paths['output_dir_track_svg'], paths['theme_name'] + cb + '_' + ci + '.svg'), 'w') as svg_icon_file:
                    svg_icon_file.write(svg_header + svg_background_track + svg_tool + svg_footer)

def _convert_svgs_to_pngs(paths):
    """Convert all SVGs to PNGs in the appropriate output folders."""
    for csf in os.listdir(paths['output_dir_toolbar_svg']):
        if csf.endswith('.svg'):
            fn = csf[:-4]
            cairosvg.svg2png(url=os.path.join(paths['output_dir_toolbar_svg'], fn + '.svg'), write_to=os.path.join(paths['output_dir_png200'], fn + '.png'), scale=.6)
            cairosvg.svg2png(url=os.path.join(paths['output_dir_toolbar_svg'], fn + '.svg'), write_to=os.path.join(paths['output_dir_png150'], fn + '.png'), scale=.45)
            cairosvg.svg2png(url=os.path.join(paths['output_dir_toolbar_svg'], fn + '.svg'), write_to=os.path.join(paths['output_dir_png_toolbar_icons'], fn + '.png'), scale=.3)
    for csf in os.listdir(paths['output_dir_track_svg']):
        if csf.endswith('.svg'):
            fn = csf[:-4]
            cairosvg.svg2png(url=os.path.join(paths['output_dir_track_svg'], fn + '.svg'), write_to=os.path.join(paths['output_dir_png_track_icons_custom'], fn + '.png'), scale=.64)
            im = Image.open(os.path.join(paths['output_dir_png_track_icons_custom'], fn + '.png'))
            im = im.crop((0, 0, 64, 64))
            im.save(os.path.join(paths['output_dir_png_track_icons_custom'], fn + '.png'))
