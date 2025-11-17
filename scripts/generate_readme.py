import os
import subprocess

MARKER = "<!-- changes -->"


def get_allowed_commits():
    try:
        log = subprocess.check_output(
            ["git", "log", "--pretty=format:%s", "-n", "20"],
            universal_newlines=True
        )
    except Exception as e:
        return ["(cannot read commits)"]

    allowed = []
    for line in log.split("\n"):
        if "[readme]" in line.lower():
            clean = line.replace("[readme]", "").strip()
            allowed.append(f"- {clean}")

    return allowed if allowed else ["(no allowed updates)"]


def create_new_readme(commits):
    return f"""# Renvoxit

Your project description…

## Recent Changes
{MARKER}
{os.linesep.join(commits)}

"""


def update_existing_readme(content, commits):
    if MARKER not in content:
        # добавляем блок в конец, если нет маркера
        return content.strip() + f"""

## Recent Changes
{MARKER}
{os.linesep.join(commits)}
"""

    before, after = content.split(MARKER)[0], content.split(MARKER)[1]
    return before + MARKER + "\n" + "\n".join(commits) + "\n"


def main():
    commits = get_allowed_commits()

    if not os.path.exists("README.md"):
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(create_new_readme(commits))
        return

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_content = update_existing_readme(content, commits)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()

# Renvoxit
