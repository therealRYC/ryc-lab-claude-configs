#!/usr/bin/env bash
# generate-catalog.sh — Generate CATALOG.md from skill frontmatter
#
# Reads skills/{category}/{skill}/SKILL.md, extracts name + description
# from YAML frontmatter, and outputs a browsable catalog grouped by category.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT="$SCRIPT_DIR/CATALOG.md"

# Category display names (order matters for output)
declare -a CATEGORY_ORDER=(
    "orchestration"
    "core-workflow"
    "research"
    "writing"
    "notebook"
    "data-analysis"
    "database-connectors"
    "bioinformatics"
    "ml-ai"
    "scientific-computing"
    "lab-integrations"
    "document-generation"
    "domain-specific"
    "utility"
    "visualization"
)

declare -A CATEGORY_NAMES=(
    ["orchestration"]="Orchestration"
    ["core-workflow"]="Core Workflow (Pi-Stack Pipeline)"
    ["research"]="Research & Learning"
    ["writing"]="Scientific Writing"
    ["notebook"]="Lab Notebook & Documentation"
    ["data-analysis"]="Data Analysis"
    ["database-connectors"]="Database Connectors"
    ["bioinformatics"]="Bioinformatics Libraries"
    ["ml-ai"]="Machine Learning & AI"
    ["scientific-computing"]="Scientific Computing"
    ["lab-integrations"]="Lab Platform Integrations"
    ["document-generation"]="Document Generation"
    ["domain-specific"]="Domain-Specific Tools"
    ["utility"]="Utility & Meta"
    ["visualization"]="Visualization"
)

total_skills=0

{
    echo "# Skill Catalog"
    echo ""
    echo "Auto-generated index of all Claude Code skills in this repository."
    echo "Run \`./generate-catalog.sh\` to regenerate after adding or modifying skills."
    echo ""

    for cat in "${CATEGORY_ORDER[@]}"; do
        cat_path="$SCRIPT_DIR/skills/$cat"
        [[ -d "$cat_path" ]] || continue

        display_name="${CATEGORY_NAMES[$cat]:-$cat}"

        # Count skills in this category
        count=0
        for skill_dir in "$cat_path"/*/; do
            [[ -d "$skill_dir" ]] && ((count++)) || true
        done

        echo "## $display_name ($count)"
        echo ""

        for skill_dir in "$cat_path"/*/; do
            [[ -d "$skill_dir" ]] || continue
            skill_name="$(basename "$skill_dir")"
            skill_md="$skill_dir/SKILL.md"

            if [[ -f "$skill_md" ]]; then
                # Extract description from frontmatter
                desc=$(awk '
                    /^---$/ { in_fm++; next }
                    in_fm == 1 && /^description:/ {
                        sub(/^description: */, "")
                        gsub(/^"/, ""); gsub(/"$/, "")
                        print
                        exit
                    }
                ' "$skill_md")

                if [[ -n "$desc" ]]; then
                    # Truncate long descriptions
                    if [[ ${#desc} -gt 120 ]]; then
                        desc="${desc:0:117}..."
                    fi
                    echo "- **$skill_name** — $desc"
                else
                    echo "- **$skill_name**"
                fi
            else
                echo "- **$skill_name** *(no SKILL.md)*"
            fi

            ((total_skills++)) || true
        done

        echo ""
    done

    echo "---"
    echo ""
    echo "*Total: $total_skills skills across ${#CATEGORY_ORDER[@]} categories*"

} > "$OUTPUT"

echo "Generated $OUTPUT ($total_skills skills)"
