import os
import shlex


def get_pager_command(filepath):
    pager = os.environ.get("RSS_PAGER", "less")
    fontsize = os.environ.get("RSS_FONT_SIZE", "")

    if "{}" in pager or "{fontsize}" in pager:
        cmd = pager.format(filepath, fontsize=fontsize)
        return cmd, True
    else:
        parts = shlex.split(pager) + [filepath]
        return parts, False
