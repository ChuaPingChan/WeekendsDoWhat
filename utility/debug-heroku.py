import os

print(f"Environment variables on Heroku:")
for k, v in os.environ.items():
    print(f"\t{k}: {v}")
