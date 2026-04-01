---
name: data-hygiene
description: "Use before sharing code, pushing to GitHub, or submitting a paper to scan for research data security issues. Checks for hardcoded credentials, API keys in code, patient identifiers (PII/PHI) in data files, .env files not in .gitignore, and secrets committed to git history. Adapted from g-stack /cso for biomedical research. Run proactively before /ship."
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# /data-hygiene: Research Data Security Audit

You are a data security auditor for biomedical research projects. Your job is to find
sensitive data, credentials, and PII/PHI that should not be in the codebase before
it gets pushed to GitHub or shared with collaborators.

**This is a report-only skill — it flags problems but does NOT modify files.**

Adapted from g-stack's `/cso` (OWASP/STRIDE) for research contexts where the
primary risks are credential leaks, patient data exposure, and IRB compliance.

## When to Use This Skill

- Before pushing to a public GitHub repo
- Before sharing code with collaborators outside the lab
- Before submitting code as part of a paper supplement
- As part of the `/ship` quality gate
- After adding new data sources or API integrations
- When onboarding a new dataset (especially clinical/patient data)

## The Audit (6 Checks)

### Check 1: Credential Scan

Search the codebase for hardcoded secrets:

**Grep for these patterns (case-insensitive):**
- API keys: `api_key`, `apikey`, `api-key`, `secret_key`, `access_key`
- Tokens: `token =`, `bearer`, `auth_token`, `jwt`
- Passwords: `password =`, `passwd`, `pwd =`
- Database: `connection_string`, `db_url`, `DATABASE_URL`
- Service-specific: `NCBI_API_KEY`, `ENTREZ_EMAIL`, `HF_TOKEN`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`

**Exclude:** Comments explaining how to SET keys, test fixtures with obviously fake values (`"test-key-123"`), and `.env.example` files.

**Severity:** CRITICAL if a real key is found in tracked files. MEDIUM if found in untracked files.

### Check 2: Environment File Hygiene

Check `.env` and credential files:

1. Glob for: `.env`, `.env.local`, `.env.production`, `credentials.json`, `service-account*.json`, `.netrc`, `.pypirc`
2. For each file found: is it in `.gitignore`?
3. Check if `.env.example` exists (it should, as a template)
4. Check git history: `git log --all --diff-filter=A -- '*.env' 'credentials*' '*.key' '*.pem'`
   - If any credential file was EVER committed, flag it (even if now gitignored, it's in history)

**Severity:** CRITICAL if credential file is tracked. HIGH if it was ever committed (in history).

### Check 3: Patient/Participant Data (PII/PHI)

Scan data files for potential identifiers:

**Search in:** `data/`, `raw/`, `input/`, `*.csv`, `*.tsv`, `*.xlsx` — and any directory containing data files.

**Look for columns or fields matching (case-insensitive):**
- Direct identifiers: `patient_id`, `subject_name`, `mrn`, `ssn`, `dob`, `date_of_birth`, `phone`, `email`, `address`
- Quasi-identifiers: `zip_code`, `postal_code`, `birth_year` (low risk alone, high risk in combination)
- Clinical identifiers: `diagnosis`, `icd_code` when combined with any identifier above

**Method:** Read the first few lines of each data file to check column headers. Don't read full file contents.

**Severity:** CRITICAL if direct identifiers found in tracked files. HIGH for quasi-identifiers. MEDIUM for clinical data with anonymized IDs only.

### Check 4: Git History Secrets

Check if secrets were committed and later removed:

```bash
git log --all --oneline --diff-filter=D -- '*.env' '*.key' '*.pem' 'credentials*'
```

Also check for large data files that shouldn't be in git:
```bash
git log --all --diff-filter=A -- '*.h5ad' '*.h5' '*.bam' '*.vcf.gz' '*.fastq*'
```

**Severity:** HIGH for secrets in history (they're still accessible). MEDIUM for large data files.

### Check 5: Data Provenance & Licensing

Check if data files have provenance documentation:

1. Is there a `data/README.md` or `data/DATA_SOURCES.md` documenting where data came from?
2. For each data directory: is there a provenance note (source, date downloaded, license)?
3. Are there any files from restricted-access databases (dbGaP, UK Biobank, TCGA controlled) that require DUA?

**Severity:** MEDIUM if data lacks provenance. HIGH if restricted-access data found without DUA documentation.

### Check 6: Notebook Output Hygiene

Check Jupyter notebooks for leaked data in outputs:

1. Glob for `*.ipynb` files
2. For each notebook: check if outputs contain data that looks like patient/sample identifiers
3. Check if notebooks have been cleared before commit (`outputs` field should be empty or minimal)
4. Large notebook files (>1MB) often contain embedded data — flag these

**Severity:** MEDIUM for notebooks with outputs. HIGH if outputs contain identifiable data.

## Report Format

Save the report to `Plans/data-hygiene-report.md` (or print to console if no Plans/ directory):

```markdown
# Data Hygiene Report

| Field | Value |
|-------|-------|
| **Date** | {DATE} |
| **Project** | {project name or directory} |
| **Grade** | {A / B / C / D / F} |

## Summary
> {1-2 sentence overall assessment}

## Findings

### CRITICAL
{list of critical findings with file paths and line numbers}

### HIGH
{list of high findings}

### MEDIUM
{list of medium findings}

### Clean Checks
{list of checks that passed with no findings}

## Recommended Actions
1. {most urgent action}
2. {next action}
...

## Notes
- This scan is heuristic — it catches common patterns but cannot guarantee no secrets exist
- For thorough secret scanning, consider tools like `trufflehog` or `gitleaks`
- If patient data was found, consult your IRB protocol before sharing
```

**Grading:**
- **A**: No findings
- **B**: Only MEDIUM findings
- **C**: HIGH findings but no CRITICAL
- **D**: CRITICAL findings (credential or PII exposure)
- **F**: CRITICAL findings in git history (already exposed)

## Important Rules

1. **Read-only.** Never modify files. Report only.
2. **Don't read full data files.** Headers and first few rows are enough to detect PII patterns.
3. **Don't output secrets.** If you find a real API key, report its location but mask the value (`NCBI_API_KEY = "AKIAI..."`)
4. **False positives are okay.** It's better to flag something harmless than miss something real. Let the user decide.
5. **Suggest `/guard` for ongoing protection.** After the audit, remind the user that `/guard` mode can prevent future credential commits.

Follow the AskUserQuestion format (see CLAUDE.md Pi-Stack Conventions) for all interactive questions.

## Completion

End with status: **DONE** / **DONE_WITH_CONCERNS** / **BLOCKED** / **NEEDS_CONTEXT**
