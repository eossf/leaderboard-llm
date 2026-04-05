# leaderboard llm

Find the best token/s , value and cheap model

## Install

### Micromamba

```bash
micromamba activate
micromamba shell init
micromamba create -n leaderboard-llm python=3.13
```

### Node local
```bash
micromamba activate leaderboard-llm
pip install nodeenv
nodeenv env
```

### Activate for install or development

```bash
micromamba activate leaderboard-llm
# linux
. /bin/activate
# win
cpwd=$(pwd)
nodev=$(ls env/src)
echo "The path is: ${cpwd}/env/src/${nodev}"
export PATH=$PATH:"${cpwd}/env/src/${nodev}"
```

### Openspec

```bash
npm install -g @fission-ai/openspec@latest
```

## Initialisation project

It's an Openspec project

### Openspec install
```bash
openspec init
```

```bash
/opsx.explore Build an application which get data from SOURCES.md relative to LLM models performance. Persist data in light sql database, with a date DD/MM/YYYY hh:mm:ss. We add sources furthermore, the application will be able to add new source without losing information. No need UI or backend service for this version first version 0.0.1. It's only get a source, persist. When adding a new source, get it persist it. And so on we could add whatever kind of source based on URL web site for this version.

