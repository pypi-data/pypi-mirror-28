# coding:utf-8
from __future__ import print_function
import os
import sys
import re
import subprocess


def colorize(sheet_content):
    """ Colorizes cheatsheet content if so configured """

    # only colorize if so configured
    if not 'CHEATCOLORS' in os.environ:
        return sheet_content

    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import TerminalFormatter

    # if pygments can't load, just return the uncolorized text
    except ImportError:
        return sheet_content

    def process_block(content):
        lexer      = get_lexer_by_name('bash')
        content = filter(lambda x:x.strip() != "",content.split('\n'))
        if content[0].startswith('```'):
            sheet_content = '\n'.join(content[1:-1])
            try:
                lexer = get_lexer_by_name(first_line[3:])
            except Exception:
                pass
        else:
            sheet_content = '\n'.join(content)
        return highlight(sheet_content, lexer, TerminalFormatter())
    replace_text = 'TACEY-CHEAT-ZH'
    pattern = re.compile('```.*?```',re.S)
    no_code_content = pattern.sub(replace_text,sheet_content)
    code_blocks = pattern.findall(sheet_content)
    no_code_content = process_block(no_code_content)
    for code_block in code_blocks:
        color_code = process_block(code_block)
        no_code_content=no_code_content.replace(replace_text,color_code,1)
    return no_code_content


def die(message):
    """ Prints a message to stderr and then terminates """
    warn(message)
    exit(1)


def editor():
    """ Determines the user's preferred editor """

    # determine which editor to use
    editor = os.environ.get('CHEAT_EDITOR') \
        or os.environ.get('VISUAL')         \
        or os.environ.get('EDITOR')         \
        or False

    # assert that the editor is set
    if editor == False:
        die(
            '要创建/编辑作弊条,你必须配置CHEAT_EDITOR, VISUAL, or EDITOR 环境变量'
        )

    return editor


def open_with_editor(filepath):
    """ Open `filepath` using the EDITOR specified by the environment variables """
    editor_cmd = editor().split()
    try:
        subprocess.call(editor_cmd + [filepath])
    except OSError:
        die('无法启动' + editor())


def warn(message):
    """ Prints a message to stderr """
    print((message), file=sys.stderr)
