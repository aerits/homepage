import re
from typing import Iterator
def post(date: str, content: str) -> str: 
    return "<p class=\"sorted-element\">" + "<b>" + date.strip() + "</b>" + ": " + content + "</p>\n<hr />\n"

def sorter(e: list[str]):
    return e[0]

# returns true if it actually got truncated
def truncater(s: str, title: str, summary_length: int) -> tuple[str, bool]:
    first_half = s[:summary_length]
    second_half = s[summary_length:]
    if len(second_half) == 0:
        return (first_half, False) # did not truncate
    
    open_tags: Iterator[str] = re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>', first_half) # type: ignore
    closed_tags: Iterator[str] = re.findall(r'</([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>', first_half) # type: ignore

    open_tags = filter(lambda x: "br" not in x and "hr" not in x, open_tags)
    at = list(open_tags)
    nt = list(closed_tags)
    
    nopen_tags: int = len(at)
    nclosed_tags: int = len(nt)
    # print(f"{at}, {nt} :: {nopen_tags}, {nclosed_tags}")

    output: str = first_half
    if nopen_tags > nclosed_tags:
        last_open_tag: re.Match[str] | None = re.search(r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>', second_half)
        last_closed_tag: re.Match[str] | None = re.search(r'</([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>', second_half)
        if last_closed_tag is None or (last_open_tag is not None and last_open_tag.end() < last_closed_tag.end()):
            print(f"missing closing tag in {title.strip()}")
        else:
            end = last_closed_tag.end()
            output += second_half[:end]

    return (output, True)

def write_template(title: str, contents: str) -> str:
    id = hash(contents)
    with open(f"./gen-templates/post{id}.t.html", 'w') as file:
        file.write(f"<h1>{title}:</h1>\n<p>{contents}</p>")
    return f"post{str(id)}.html"

def get_posts() -> str:
    posts: list[list[str]] = []
    with open("./templates/showerthoughts/posts.e.html", 'r') as file:
        for line in file:
            if line[0] == '#':
                posts.append([line[2:], ""])
            else:
                posts[-1][1] += line + " \n"
    output: str = ""
    for post_ in posts:
        # post_[0] is the date
        # post_[1] is the contents
        (contents, truncated) = truncater(post_[1], post_[0], 500)
        link: str = write_template(post_[0], post_[1])
        title = post_[0]
        if truncated: contents += f'...<p><a href="{link}">continue reading here</a></p>'  # noqa: E701
        else: title = f"{post_[0]} <a href='{link}'>permalink</a>"  # noqa: E701
        output += post(title, contents)
    return output
