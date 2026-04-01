<!-- Created: 2026-02-23 -->
<!-- Last updated: 2026-02-23 — Initial creation -->

---
name: analyze-literature
description: Analyze scientific papers, preprints, or research topics. Use when reviewing papers, extracting methodology, comparing studies, or summarizing findings.
user-invocable: true
allowed-tools: Read, WebFetch, WebSearch, Grep, Glob
argument-hint: "[paper-DOI, topic, or file-path]"
---

# Literature Analysis

Analyze the provided paper, preprint, or research topic.

## If given a DOI or paper title:
Search PubMed and bioRxiv MCP servers for the paper. Retrieve the abstract and full text if available.

## If given a file path:
Read the file and analyze its contents.

## Analysis Structure:
1. **Summary** (2-3 sentences): What is this paper about?
2. **Methodology**: Study design, sample size, key techniques, statistical methods
3. **Key Findings**: Main results with specific numbers, effect sizes, p-values
4. **Strengths**: What this study does well
5. **Limitations**: Potential weaknesses, confounders, missing controls
6. **Relevance**: How this connects to variant effect maps, deep mutational scanning, or protein function research
7. **Key References**: Notable citations worth following up on

Focus on: $ARGUMENTS
