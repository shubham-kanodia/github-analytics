# GitHub Analytics

## 1. Setup environment variable(s)

```
EXPORT PAT=<your-github-pat>
```

## 2. Collect repositories (using GitHub Search)

Fetch using GitHub Search

```
python3 collect_repos.py
```

Cleanup and aggregation

```
jq -c '.[]' ./data/sources/*.json | jq -s | jq -r '.[].html_url' > ./data/repos_from_topics.txt
cat ./data/repos_from_landscape.txt ./data/best-of-crypto.txt ./data/repos_from_topics.txt | sort | uniq -u > ./data/repos.txt
awk '!/quickstart|documentation|tutorial|\/awesome/' ./data/repos.txt > tmpfile && mv tmpfile ./data/repos.txt
```

## 3. Scrape data for repositories

```
python3 main.py
```
