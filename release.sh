#!/usr/bin/env bash
set -euo pipefail

# === CONFIG ===
REPO_DEV="$HOME/projetos/loja_calcados_pro"
REPO_STABLE="$HOME/projetos/loja_calcados_pro_stable"
BRANCH_DEV="develop"
BRANCH_MAIN="main"

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  echo "Uso: ./release.sh vX.Y.Z"
  exit 1
fi

echo "🔁 Iniciando release $VERSION ..."
cd "$REPO_DEV"

# 1) Checar árvore limpa
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "❌ Existem mudanças não commitadas no repo de DEV. Faça commit/stash e tente de novo."
  exit 1
fi

# 2) Atualizar referências
git fetch origin

# 3) Garantir DEV atualizado
git checkout "$BRANCH_DEV"
git pull origin "$BRANCH_DEV"

# 4) Mergear no MAIN
git checkout "$BRANCH_MAIN"
git pull origin "$BRANCH_MAIN"
git merge --no-ff "$BRANCH_DEV" -m "release: $VERSION"
git push origin "$BRANCH_MAIN"

# 5) Tag e push
git tag -a "$VERSION" -m "Release $VERSION"
git push origin "$VERSION"

# 6) Atualizar worktree estável
echo "🔧 Atualizando worktree estável..."
chmod -R u+w "$REPO_STABLE" || true
cd "$REPO_STABLE"
git fetch origin
git checkout "$BRANCH_MAIN"
git pull origin "$BRANCH_MAIN"
cd -

# 7) Travar novamente a pasta estável
chmod -R a-w "$REPO_STABLE" || true

echo "✅ Release $VERSION concluída com sucesso!"
echo "📦 main atualizada, tag enviada e worktree estável sincronizada."
