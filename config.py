import subprocess

process = subprocess.Popen(
    ["git", "rev-parse", "--short", "HEAD"], shell=False, stdout=subprocess.PIPE
)
HASH = process.communicate()[0].strip().decode()
