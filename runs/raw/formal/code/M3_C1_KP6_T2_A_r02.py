import subprocess
result = subprocess.run(['ls', '-la', '/mnt/data/'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
