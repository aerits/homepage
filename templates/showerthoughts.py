def post(date: str, content: str) -> str: 
    return "<p class=\"sorted-element\">" + "<b>" + date + "</b>" + ": " + content + "</p>\n<hr>\n"

def sorter(e: list[str]):
    return e[0]

def get_posts() -> str:
    posts: list[list[str]] = []
    with open("./templates/showerthoughts/posts.e.html", 'r') as file:
        for line in file:
            if line[0] == '#':
                posts.append([line[2:], ""])
            else:
                posts[-1][1] += line + " "
    output: str = ""
    for post_ in posts:
        output += post(post_[0], post_[1])
    return output
