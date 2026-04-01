#!/usr/bin/env bash
# install.sh — Install Fowler Lab Claude Code configurations
#
# Copies skills, agents, and hooks into ~/.claude/.
# Skills are stored in category subdirectories in this repo but installed
# FLAT into ~/.claude/skills/ (Claude Code expects skills/{skill-name}/SKILL.md).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"

# Defaults
DRY_RUN=false
FORCE=false
SKIP_HOOKS=false
SKIP_AGENTS=false
INCLUDE_WSL=false
CATEGORIES=""

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Install Fowler Lab Claude Code configurations into ~/.claude/.

Options:
  --dry-run              Show what would be copied without copying
  --force                Overwrite existing skills/agents/hooks
  --categories "a,b,c"   Only install skills from listed categories
  --skip-hooks           Don't install hooks
  --skip-agents          Don't install agents
  --include-wsl          Include WSL-specific hooks (notify-wsl.sh)
  --help                 Show this help message

Available categories:
  orchestration, core-workflow, research, writing, notebook, data-analysis,
  database-connectors, bioinformatics, ml-ai, scientific-computing,
  lab-integrations, document-generation, domain-specific, utility, visualization

Examples:
  ./install.sh                              # Install everything
  ./install.sh --dry-run                    # Preview what would be installed
  ./install.sh --categories "core-workflow,research,bioinformatics"
  ./install.sh --force --include-wsl        # Overwrite existing + WSL hooks
EOF
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)    DRY_RUN=true; shift ;;
        --force)      FORCE=true; shift ;;
        --skip-hooks) SKIP_HOOKS=true; shift ;;
        --skip-agents) SKIP_AGENTS=true; shift ;;
        --include-wsl) INCLUDE_WSL=true; shift ;;
        --categories) CATEGORIES="$2"; shift 2 ;;
        --help|-h)    usage ;;
        *)            echo "Unknown option: $1"; usage ;;
    esac
done

# Counters
skills_installed=0
skills_skipped=0
agents_installed=0
agents_skipped=0
hooks_installed=0
hooks_skipped=0

log_install() { echo "  [INSTALL] $1"; }
log_skip()    { echo "  [SKIP]    $1 (already exists)"; }
log_dry()     { echo "  [DRY-RUN] would install $1"; }

# Create target directories
if [[ "$DRY_RUN" == false ]]; then
    mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents" "$CLAUDE_DIR/hooks"
fi

# ── Skills ──────────────────────────────────────────────────────────────

echo ""
echo "Installing skills..."

# Build list of category directories to process
if [[ -n "$CATEGORIES" ]]; then
    IFS=',' read -ra CATS <<< "$CATEGORIES"
else
    CATS=()
    for cat_dir in "$SCRIPT_DIR"/skills/*/; do
        CATS+=("$(basename "$cat_dir")")
    done
fi

for cat in "${CATS[@]}"; do
    cat=$(echo "$cat" | xargs)  # trim whitespace
    cat_path="$SCRIPT_DIR/skills/$cat"
    if [[ ! -d "$cat_path" ]]; then
        echo "  Warning: category '$cat' not found, skipping"
        continue
    fi

    echo "  ── $cat ──"
    for skill_dir in "$cat_path"/*/; do
        [[ -d "$skill_dir" ]] || continue
        skill_name="$(basename "$skill_dir")"
        target="$CLAUDE_DIR/skills/$skill_name"

        if [[ -d "$target" && "$FORCE" == false ]]; then
            if [[ "$DRY_RUN" == true ]]; then
                log_skip "$skill_name"
            else
                log_skip "$skill_name"
            fi
            ((skills_skipped++)) || true
        else
            if [[ "$DRY_RUN" == true ]]; then
                log_dry "$skill_name"
            else
                rm -rf "$target"
                cp -r "$skill_dir" "$target"
                log_install "$skill_name"
            fi
            ((skills_installed++)) || true
        fi
    done
done

# ── Agents ──────────────────────────────────────────────────────────────

if [[ "$SKIP_AGENTS" == false ]]; then
    echo ""
    echo "Installing agents..."

    for agent_file in "$SCRIPT_DIR"/agents/*.md; do
        [[ -f "$agent_file" ]] || continue
        agent_name="$(basename "$agent_file")"
        target="$CLAUDE_DIR/agents/$agent_name"

        if [[ -f "$target" && "$FORCE" == false ]]; then
            log_skip "$agent_name"
            ((agents_skipped++)) || true
        else
            if [[ "$DRY_RUN" == true ]]; then
                log_dry "$agent_name"
            else
                cp "$agent_file" "$target"
                log_install "$agent_name"
            fi
            ((agents_installed++)) || true
        fi
    done
fi

# ── Hooks ───────────────────────────────────────────────────────────────

if [[ "$SKIP_HOOKS" == false ]]; then
    echo ""
    echo "Installing hooks..."

    for hook_file in "$SCRIPT_DIR"/hooks/*; do
        [[ -f "$hook_file" ]] || continue
        hook_name="$(basename "$hook_file")"

        # Skip WSL-specific hook unless explicitly requested
        if [[ "$hook_name" == "notify-wsl.sh" && "$INCLUDE_WSL" == false ]]; then
            echo "  [SKIP]    $hook_name (WSL-only, use --include-wsl to install)"
            ((hooks_skipped++)) || true
            continue
        fi

        target="$CLAUDE_DIR/hooks/$hook_name"

        if [[ -f "$target" && "$FORCE" == false ]]; then
            log_skip "$hook_name"
            ((hooks_skipped++)) || true
        else
            if [[ "$DRY_RUN" == true ]]; then
                log_dry "$hook_name"
            else
                cp "$hook_file" "$target"
                chmod +x "$target"
                log_install "$hook_name"
            fi
            ((hooks_installed++)) || true
        fi
    done
fi

# ── Settings & CLAUDE.md ────────────────────────────────────────────────

echo ""

if [[ ! -f "$CLAUDE_DIR/settings.json" ]]; then
    if [[ -f "$SCRIPT_DIR/settings.json.example" ]]; then
        if [[ "$DRY_RUN" == true ]]; then
            echo "[DRY-RUN] would copy settings.json.example -> settings.json"
        else
            cp "$SCRIPT_DIR/settings.json.example" "$CLAUDE_DIR/settings.json"
            echo "[INSTALL] settings.json (from settings.json.example)"
        fi
    fi
else
    echo "[SKIP]    settings.json exists. Review settings.json.example for updates."
fi

if [[ ! -f "$CLAUDE_DIR/CLAUDE.md" ]]; then
    if [[ -f "$SCRIPT_DIR/CLAUDE.md.example" ]]; then
        if [[ "$DRY_RUN" == true ]]; then
            echo "[DRY-RUN] would copy CLAUDE.md.example -> CLAUDE.md"
        else
            cp "$SCRIPT_DIR/CLAUDE.md.example" "$CLAUDE_DIR/CLAUDE.md"
            echo "[INSTALL] CLAUDE.md (from CLAUDE.md.example)"
            echo "          ** Edit ~/.claude/CLAUDE.md to fill in your personal details **"
        fi
    fi
else
    echo "[SKIP]    CLAUDE.md exists. Review CLAUDE.md.example for updates."
fi

# ── Summary ─────────────────────────────────────────────────────────────

echo ""
echo "════════════════════════════════════════════"
if [[ "$DRY_RUN" == true ]]; then
    echo "  DRY RUN COMPLETE"
else
    echo "  INSTALLATION COMPLETE"
fi
echo "════════════════════════════════════════════"
echo "  Skills:  $skills_installed installed, $skills_skipped skipped"
echo "  Agents:  $agents_installed installed, $agents_skipped skipped"
echo "  Hooks:   $hooks_installed installed, $hooks_skipped skipped"
echo "════════════════════════════════════════════"

if [[ "$DRY_RUN" == false && $skills_installed -gt 0 ]]; then
    echo ""
    echo "Next steps:"
    echo "  1. Edit ~/.claude/CLAUDE.md — fill in your name, email, and GitHub handle"
    echo "  2. Review ~/.claude/settings.json — adjust permissions to your comfort level"
    echo "  3. Restart Claude Code to pick up the new skills"
fi
