"""Day 5 — report the current git branch so you never edit main by accident.(Module docstring)"""
import subprocess  # lets Python run a shell command and capture its output
 
 
def current_branch() -> str:
    """Return the name of the git branch currently checked out.(function docstring)"""
    # subprocess.run executes the command; capture_output keeps stdout for us,
    # text=True decodes bytes to str, check=True raises if git returns nonzero.
    result = subprocess.run(
        ["git", "branch", "--show-current"],   # the git command (as a list) that prints ONLY the current branch
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()  # strip the trailing newline git adds
 
 
def main() -> None:
    branch = current_branch()
    if branch == "main":
        print(f"On branch: {branch} (STOP — cut a day-NN branch first)")
    else:
        print(f"On branch: {branch} (safe to work here)")
 
 
if __name__ == "__main__":
    main()
