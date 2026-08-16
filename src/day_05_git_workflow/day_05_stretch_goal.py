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


def guard() -> None:
    """Pre-work safety check: refuse to run on main or with a dirty tree.(function docstring)"""
    branch = current_branch()
    if branch == "main":
        raise SystemExit(
            "guard: you are on 'main'. Cut a day-NN branch first "
            "(e.g. `git switch -c day-05`)."
        )

    # --porcelain gives stable, script-friendly output: empty == clean tree.
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    if status.stdout.strip():
        raise SystemExit(
            f"guard: uncommitted changes present on '{branch}'. "
            "Commit or stash them before continuing."
        )


def main() -> None:
    guard()  # abort early if on main or the tree is dirty
    branch = current_branch()
    print(f"On branch: {branch} (safe to work here)")


if __name__ == "__main__":
    main()