import urllib.request
import json
import os
import re

USERNAME = "allangaiteir00"
API_URL = f"https://api.github.com/users/{USERNAME}/repos?type=public&sort=pushed&per_page=100"

req = urllib.request.Request(API_URL)
token = os.getenv("GITHUB_TOKEN")
if token:
    req.add_header("Authorization", f"Bearer {token}")

try:
    with urllib.request.urlopen(req) as response:
        repos = json.loads(response.read().decode())
except Exception as e:
    print(f"Erro ao buscar repositórios: {e}")
    exit(1)

# Filtra repositórios que não são forks e que não seja o próprio repositório de perfil
filtered_repos = [r for r in repos if not r.get('fork') and r.get('name') != USERNAME]

# Pega os 4 repositórios atualizados mais recentemente
top_repos = filtered_repos[:4]

html_content = '<div align="center">\n'
for repo in top_repos:
    html_content += f'  <a href="{repo["html_url"]}">\n'
    html_content += f'    <img src="https://github-readme-stats-eight-theta.vercel.app/api/pin/?username={USERNAME}&repo={repo["name"]}&theme=github_dark" />\n'
    html_content += f'  </a>\n'
html_content += '</div>'

with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

# Substitui o conteúdo entre as tags START_REPOS e END_REPOS
new_readme = re.sub(
    r'(<!-- START_REPOS -->).*?(<!-- END_REPOS -->)',
    rf'\1\n{html_content}\n\2',
    readme_content,
    flags=re.DOTALL
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("✅ README.md atualizado com sucesso com os repositórios dinâmicos!")
