import sys
import platform
import subprocess
 
def toolchain_check() -> str:
    """Confirm the interpreter uv handed us is the one we expect,
    and that uv itself is reachable from inside Python."""
    
    version = platform.python_version()          # e.g. '3.12.4'
    major_minor = ".".join(version.split(".")[:2])  # trims patch: '3.12'
    expected = "3.12"
    status = "ready" if major_minor == expected else "MISMATCH"
    python_line = f"Python {version} via uv — {status}"

    uv_result = subprocess.run(
        ["uv", "--version"],
        capture_output=True,
        text=True,
    )
    uv_version = uv_result.stdout.strip()
    uv_line = f"uv toolchain — {uv_version}" if uv_version else "uv toolchain — NOT FOUND"

    return f"{python_line}\n{uv_line}"
 
if __name__ == "__main__":
    print(toolchain_check())
