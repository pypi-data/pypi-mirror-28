"""This module contains for functions for parsing markdown."""

import re

def markdown_to_html(markdown, paths=None):
    """Takes a string in markdown, and converts it to HTML.

    :param str markdown: The maekdown to convert.
    :param dict paths: If given, any paths will be replaced using this lookup.
    :rtype: ``str``"""

    markdown, characters = escape_characters(markdown)
    blocks = markdown_to_blocks(markdown)
    blocks = group_blocks(blocks)
    html = [block_to_html(block, paths=paths) if isinstance(block, str)
     else group_block_to_html(block) for block in blocks]
    html = "\n".join(html)
    for character in characters:
        html = html.replace("\x1A", character, 1)
    return html


def escape_characters(markdown):
    """Takes some markdown and replaces escaped characters with the substition
    character. This is returned along with a list of escaped characters.

    You cannot escape line breaks - the backslash will be removed but not the
    line break.

    :param str markdown: The string to break up.
    :rtype: ``str``, ``list``"""

    characters = []
    while "\\" in markdown:
        location = markdown.find("\\")
        if location != len(markdown) - 1:
            character = markdown[location + 1]
            if character != "\n":
                characters.append(character)
                markdown = markdown[:location] + "\x1A" + markdown[location + 2:]
            else:
                markdown = markdown[:location] + markdown[location + 1:]
        else:
            break
    return markdown, characters


def markdown_to_blocks(markdown):
    """Breaks a string into a list of blocks, using single line breaks.
    Windows line breaks (``\\r\\n``) are supported.

    :param str markdown: The string to break up.
    :rtype: ``list``"""

    blocks = markdown.replace("\r\n", "\n").split("\n")
    blocks = [block.strip().replace("\n", " ") for block in blocks]
    blocks = list(filter(bool, blocks))
    return blocks


def group_blocks(blocks):
    """Takes a list of blocks, and checks each to see if it is part of a group.
    It then clusters the consecutive ones together as a sub-list and returns
    the list back.

    :param list blocks: The list of markdown blocks to group.
    :rtype: ``list``"""

    grouped_blocks = []
    group_block = []
    while blocks:
        if is_multi_block(blocks[0]):
            group_block.append(blocks.pop(0))
        else:
            if group_block:
                grouped_blocks.append(group_block)
                group_block = []
            grouped_blocks.append(blocks.pop(0))
    if group_block:
        grouped_blocks.append(group_block)
    return grouped_blocks


def block_to_html(block, paths=None):
    """Converts a Markdown block to the relevant HTML.

    :param str block: The string to convert.
    :param dict paths: If given, these will be used to translate any paths.
    :rtype: ``str``"""

    if block[0] == "#":
        return create_heading_html(block)
    elif re.compile(r"\!\[(.*?)\](\[.*?\])?\((.*?)\)").match(block):
        return create_image_html(block, paths=paths)
    elif re.compile(r"\!\((.*?)\)").match(block):
        return create_video_html(block, paths=paths)
    elif re.compile(r"\!\{(.*?)\}").match(block):
        return create_youtube_html(block)
    else:
        return create_paragraph_html(block)


def group_block_to_html(blocks):
    """Converts a list of grouped Markdown block to the relevant HTML.

    :param list blocks: The markdown blocks.
    :rtype: ``str``"""

    return create_list_html(blocks)


def is_multi_block(block):
    """Checks whether a Markdown block is part of a group of blocks.

    :param str block: The block to check.
    :rtype: ``bool``"""

    if re.compile(r"([\d]*\.|-)(.*)").match(block):
        return True
    return False


def create_paragraph_html(block, p=True):
    """Converts a paragraph markdown block to its HTML equivalent.

    :param str block: The block to convert.
    :param bool p: If ``false``, the enclosing <p> tags will be omitted.
    :rtype: ``str``"""

    block = re.sub(
     r"\{(.*?)\}\((.*?) \"(.*?)\"\)",
     r'<a href="\2" target="_blank" title="\3">\1</a>', block
    )
    block = re.sub(
     r"\{(.*?)\}\((.*?)\)", r'<a href="\2" target="_blank">\1</a>', block
    )
    block = re.sub(
     r"\[(.*?)\]\((.*?) \"(.*?)\"\)", r'<a href="\2" title="\3">\1</a>', block
    )
    block = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', block)
    block = re.sub(r"\~\~(.*?)\~\~", r"<del>\1</del>", block)
    block = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", block)
    block = re.sub(r"\*(.*?)\*", r"<em>\1</em>", block)
    return "<p>{}</p>".format(block) if p else block


def create_heading_html(block):
    """Converts a heading markdown block to HTML. The heading level will depend
    on the number of # characters, and there is no upper limit.

    :param str block: The block to convert."""

    start = re.search(r"[^#]", block).start()
    level = block[:start].count("#")
    return "<h{}>{}</h{}>".format(level, block[start:].strip(), level)


def create_image_html(block, paths=None):
    """Converts an image markdown block to HTML. It accepts blocks with or
    without figcaption sections.

    :param str block: The block to convert.
    :param dict paths: If given, these will be used to translate any paths.
    :rtype: ``str``"""

    title, *mid, path = re.compile(
     r"\!\[(.*?)\](\[.*?\])?\((.*?)\)"
    ).findall(block)[0]
    if paths: path = paths.get(path, path)
    caption = ""
    if mid and mid[0]:
        caption = "<figcaption>{}</figcaption>".format(
         create_paragraph_html(mid[0][1:-1], p=False)
        )
    return '<figure><img src="{}" title="{}">{}</figure>'.format(
     path, title, caption
    )


def create_video_html(block, paths=None):
    """Converts a video markdown block to HTML.

    :param str block: The block to convert.
    :param dict paths: If given, these will be used to translate any paths.
    :rtype: ``str``"""

    path = re.compile(r"\!\((.*?)\)").findall(block)[0]
    if paths: path = paths.get(path, path)
    return '<video src="{}" controls></video>'.format(path)


def create_youtube_html(block):
    """Converts a youtube markdown block to HTML.

    :param str block: The block to convert."""

    v = re.compile(r"\!\{(.*?)\}").findall(block)[0]
    return ('<div class="youtube"><iframe src="//www.youtube.com/embed/{}/"' +
    ' frameborder="0" allowfullscreen></iframe></div>').format(v)


def create_list_html(blocks):
    """Converts a series of list item markdown blocks to the relevant HTML.

    :param list blocks: The list item blocks.
    :rtype: ``str``"""

    lines = []
    number = False
    for block in blocks:
        if block[0] == "-":
            lines.append(block[1:].strip())
        else:
            number = True
            lines.append(block[block.find(".") + 1:].strip())
    html = "<{}l>\n{{}}\n</{}l>".format(*["o", "o"] if number else ["u", "u"])
    return html.format("\n".join(["<li>{}</li>".format(line) for line in lines]))





'''








def create_block_html(block, paths=None):
    """Converts a Markdown block to the relevant HTML.

    :param str text: The string to break up.
    :rtype: ``list``"""

    block, characters = escape_characters(block)
    html = ""
    if block[0] == "#":
        html = create_heading_html(block)
    elif re.compile(r"\!\[(.*?)\](\[.*?\])?\((.*?)\)").match(block):
        html =  create_image_html(block, paths=paths)
    elif re.compile(r"\!\((.*?)\)").match(block):
        html =  create_video_html(block, paths=paths)
    elif re.compile(r"\!\{(.*?)\}").match(block):
        html =  create_youtube_html(block)
    else:
        html = create_paragraph_html(block)
    for char in characters:
        html = html.replace("\x1A", char, 1)
    return html


def create_multi_block_html(blocks):
    pass





def create_list_html(block):
    """Converts a list item markdown block to HTML.

    :param str block: The block to convert."""

    item = ""
    if block[0] == "-":
        item = block[1:].strip()
    else:
        item = block[block.find(".") + 1:].strip()
    return "<li>{}</li>".format(item)

def escape_characters(block):

'''
