import logging

from wcwidth import wcswidth, wcwidth

logger = logging.getLogger(__name__)


def truncate_to_len(string: str, width: int) -> str:
    """Correctly truncate string for terminal considering wide characters."""
    real_len = wcswidth(string)
    if real_len <= width:
        return string

    cur_len = 0
    out_string: list[str] = []

    for char in string:
        # avoid decreasing string length with indeterminate character
        cur_len += max(wcwidth(char), 0)
        out_string += char
        if cur_len >= width:
            break
    return "".join(out_string)


def wcs_center(text: str, width: int, padding: str = " ") -> str:
    """Correctly center string for terminal considering wide characters."""
    pad_width = wcwidth(padding)
    if pad_width < 1:
        logger.warning("wcs_center called with zero width pad string: %r", padding)
        return text

    pad_cnt = (width - wcswidth(text)) // (2 * wcwidth(padding))
    if pad_cnt < 0:
        return text
    res: str = padding * pad_cnt + text + padding * pad_cnt
    return res + " " if wcswidth(res) < width else res
