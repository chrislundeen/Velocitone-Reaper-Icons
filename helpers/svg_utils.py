# SVG helper functions for Velocitone-Reaper-Toolbar-Icons

def get_core(svg_file):
    """
    Extracts the core SVG content, removing XML/doctype/header/footer.
    Args:
        svg_file: Open file object for SVG.
    Returns:
        str: SVG content without header/footer.
    """
    lines = svg_file.readlines()
    # Remove last line (footer) and first three lines (xml, doctype, svg open)
    if len(lines) > 4:
        lines = lines[3:-1]
    return ''.join(lines)

def apply_svg_colors(svg_string, color, config):
    """
    Replace placeholder colors in SVG string with theme colors.
    Args:
        svg_string: SVG string with placeholders.
        color: One of 'off', 'over', 'on', 'track'.
        config: Loaded config dict.
    Returns:
        str: SVG string with colors replaced.
    """
    if color is None:
        return svg_string
    svg_string = svg_string.replace(
        'rgb(111,111,111)', config['colors'][config['themecolor']['background']['stroke'][color]])
    svg_string = svg_string.replace(
        'rgb(11,11,11)', config['colors'][config['themecolor']['background']['fill'][color]])
    svg_string = svg_string.replace(
        'rgb(222,222,222)', config['colors'][config['themecolor']['icon']['fill'][color]])
    return svg_string

def wrap_svg(scale, position, svg_content, color, config):
    """
    Wrap SVG content in a <g> tag with transform and apply color replacements.
    Args:
        scale: Scale factor (int or float).
        position: X offset for placement.
        svg_content: SVG string.
        color: Color state ('off', 'over', 'on', 'track').
        config: Loaded config dict.
    Returns:
        str: Wrapped and colorized SVG string.
    """
    xoffset = str(position + ((100 - scale) / 2))
    yoffset = str((100 - scale) / 2)
    svg_header = f'\n<g transform="matrix(.{scale},0,0,.{scale},{xoffset},{yoffset})">\n'
    svg_footer = '\n</g>\n'
    svg_string = svg_header + svg_content + svg_footer
    return apply_svg_colors(svg_string, color, config)
