from re import search
from os.path import join

def get_size(size: int) -> str:
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024

    if size >= gb:
        return f"{round(size / gb, 2)} GB"
    elif size >= mb:
        return  f"{round(size / mb, 2)} MB"
    elif size >= kb:
        return  f"{round(size / kb, 2)} KB"
    else:
        return str(size)


def _remove_comment(css: str) -> str:
    re = r"\/\*[^*]*\*+([^\/*][^*]*\*+)*\/"

    while True:
        search_result = search(re, css)
        if search_result is None:
            break

        searched_comment = css[search_result.start():search_result.end()]
        css = css.replace(searched_comment, "")

    return css


def _remove_whitespace(css: str) -> str:
    return "".join(x for x in [x.strip() for x in css.split("\n")] if len(x) != 0)


def _remove_whitespace_static(css: str) -> str:
    css = css.replace(": ", ":")
    css = css.replace(" {", "{")
    css = css.replace(" (", "(")
    css = css.replace(") ", ")")
    css = css.replace(" !", "!")
    css = css.replace(" > ", ">")
    css = css.replace(", ", ",")
    return css


def css_clean_up(file: str, css: str) -> int:
    def _css_write() -> None:
        with open(file.replace(".css", ".min.css"), mode="w", encoding="utf-8") as css_writer:
            css_writer.write(css)

    before = len(css)

    css = _remove_comment(css=css)
    css = _remove_whitespace(css=css)
    css = _remove_whitespace_static(css=css)

    after = len(css)

    print(f"* CSS Minify Result : {get_size(size=before)} -> {get_size(size=after)} " \
        f"(-{100 - round(after / before * 100)}%) \n")

    _css_write()


if __name__ == "__main__":
    for file in [
        "./d2coding/d2coding.css",
        "./d2coding/d2coding.kr.css"
    ]:
        with open(file, mode="r", encoding="utf-8") as css_reader:
            css_clean_up(file=file, css=css_reader.read())
