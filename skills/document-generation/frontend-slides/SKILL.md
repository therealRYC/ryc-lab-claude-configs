---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
---

# Frontend Slides Skill

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser. This skill helps non-designers discover their preferred aesthetic through visual exploration ("show, don't tell"), then generates production-quality slide decks.

## Core Philosophy

1. **Zero Dependencies** — HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — People don't know what they want until they see it. Generate visual previews, not abstract choices.
3. **Distinctive Design** — Avoid generic "AI slop" aesthetics. Every presentation should feel custom-crafted.
4. **Production Quality** — Code should be well-commented, accessible, and performant.
5. **Viewport Fitting (CRITICAL)** — Every slide MUST fit exactly within the viewport. No scrolling within slides, ever. This is non-negotiable.
6. **Self-Contained Projects** — Every presentation lives in a dated folder (`YYMMDD-title/`) with all assets, metadata, and both a local-editing and portable-sharing version of the HTML. The folder is the deliverable.

---

## CRITICAL: Viewport Fitting Requirements

**This section is mandatory for ALL presentations. Every slide must be fully visible without scrolling on any screen size.**

### The Golden Rule

```
Each slide = exactly one viewport height (100vh/100dvh)
Content overflows? → Split into multiple slides or reduce content
Never scroll within a slide.
```

### Content Density Limits

To guarantee viewport fitting, enforce these limits per slide:

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2 grid) |
| Code slide | 1 heading + 8-10 lines of code maximum |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |

**If content exceeds these limits → Split into multiple slides**

### Required CSS Architecture

Every presentation MUST include this base CSS for viewport fitting:

```css
/* ===========================================
   VIEWPORT FITTING: MANDATORY BASE STYLES
   These styles MUST be included in every presentation.
   They ensure slides fit exactly in the viewport.
   =========================================== */

/* 1. Lock html/body to viewport */
html, body {
    height: 100%;
    overflow-x: hidden;
}

html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

/* 2. Each slide = exact viewport height */
.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh; /* Dynamic viewport height for mobile browsers */
    overflow: hidden; /* CRITICAL: Prevent ANY overflow */
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

/* 3. Content container with flex for centering */
.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden; /* Double-protection against overflow */
    padding: var(--slide-padding);
}

/* 4. ALL typography uses clamp() for responsive scaling */
:root {
    /* Titles scale from mobile to desktop */
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);

    /* Body text */
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);

    /* Spacing scales with viewport */
    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);
}

/* 5. Cards/containers use viewport-relative max sizes */
.card, .container, .content-box {
    max-width: min(90vw, 1000px);
    max-height: min(80vh, 700px);
}

/* 6. Lists auto-scale with viewport */
.feature-list, .bullet-list {
    gap: clamp(0.4rem, 1vh, 1rem);
}

.feature-list li, .bullet-list li {
    font-size: var(--body-size);
    line-height: 1.4;
}

/* 7. Grids adapt to available space */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(0.5rem, 1.5vw, 1rem);
}

/* 8. Images constrained to viewport */
img, .image-container {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
}

/* ===========================================
   RESPONSIVE BREAKPOINTS
   Aggressive scaling for smaller viewports
   =========================================== */

/* Short viewports (< 700px height) */
@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
        --h2-size: clamp(1rem, 3vw, 1.75rem);
    }
}

/* Very short viewports (< 600px height) */
@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --content-gap: clamp(0.3rem, 1vw, 0.75rem);
        --title-size: clamp(1.1rem, 4vw, 2rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }

    /* Hide non-essential elements */
    .nav-dots, .keyboard-hint, .decorative {
        display: none;
    }
}

/* Extremely short (landscape phones, < 500px height) */
@media (max-height: 500px) {
    :root {
        --slide-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}

/* Narrow viewports (< 600px width) */
@media (max-width: 600px) {
    :root {
        --title-size: clamp(1.25rem, 7vw, 2.5rem);
    }

    /* Stack grids vertically */
    .grid {
        grid-template-columns: 1fr;
    }
}

/* ===========================================
   REDUCED MOTION
   Respect user preferences
   =========================================== */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }

    html {
        scroll-behavior: auto;
    }
}

/* ===========================================
   PRINT STYLES
   Enables Ctrl+P → Save as PDF for free PDF export.
   Hides navigation UI, disables snap, lays out slides as pages.
   =========================================== */
@media print {
    html {
        scroll-snap-type: none;
        scroll-behavior: auto;
    }

    .slide {
        height: auto;
        min-height: 100vh;
        overflow: visible;
        page-break-after: always;
        break-after: page;
    }

    .nav-dots, .progress-bar, .keyboard-hint,
    .custom-cursor, .cursor-trail, .decorative {
        display: none !important;
    }

    /* Show all content without animation */
    .reveal {
        opacity: 1 !important;
        transform: none !important;
        filter: none !important;
    }

    @page {
        margin: 0;
        size: landscape;
    }
}
```

### Overflow Prevention Checklist

Before generating any presentation, mentally verify:

1. ✅ Every `.slide` has `height: 100vh; height: 100dvh; overflow: hidden;`
2. ✅ All font sizes use `clamp(min, preferred, max)`
3. ✅ All spacing uses `clamp()` or viewport units
4. ✅ Content containers have `max-height` constraints
5. ✅ Images have `max-height: min(50vh, 400px)` or similar
6. ✅ Grids use `auto-fit` with `minmax()` for responsive columns
7. ✅ Breakpoints exist for heights: 700px, 600px, 500px
8. ✅ No fixed pixel heights on content elements
9. ✅ Content per slide respects density limits
10. ✅ `@media print` block included for PDF export via Ctrl+P

### When Content Doesn't Fit

If you find yourself with too much content:

**DO:**
- Split into multiple slides
- Reduce bullet points (max 5-6 per slide)
- Shorten text (aim for 1-2 lines per bullet)
- Use smaller code snippets
- Create a "continued" slide

**DON'T:**
- Reduce font size below readable limits
- Remove padding/spacing entirely
- Allow any scrolling
- Cram content to fit

### Testing Viewport Fit

After generating, recommend the user test at these sizes:
- Desktop: 1920×1080, 1440×900, 1280×720
- Tablet: 1024×768, 768×1024 (portrait)
- Mobile: 375×667, 414×896
- Landscape phone: 667×375, 896×414

---

## Phase 0: Detect Mode

First, determine what the user wants:

**Mode A: New Presentation**
- User wants to create slides from scratch
- Proceed to Phase 1 (Content Discovery)

**Mode B: PPT Conversion**
- User has a PowerPoint file (.ppt, .pptx) to convert
- Proceed to Phase 4 (PPT Extraction)

**Mode C: Existing Presentation Enhancement**
- User has an HTML presentation and wants to improve it
- Read the existing file, understand the structure, then enhance

---

## Phase 1: Content Discovery (New Presentations)

Before designing, understand the content. Ask via AskUserQuestion:

### Step 1.1: Presentation Context + Images (Single Form)

**IMPORTANT:** Ask ALL 4 questions in a single AskUserQuestion call so the user can fill everything out at once before submitting.

**Question 1: Purpose**
- Header: "Purpose"
- Question: "What is this presentation for?"
- Options:
  - "Pitch deck" — Selling an idea, product, or company to investors/clients
  - "Teaching/Tutorial" — Explaining concepts, how-to guides, educational content
  - "Conference talk" — Speaking at an event, tech talk, keynote
  - "Internal presentation" — Team updates, strategy meetings, company updates

**Question 2: Slide Count**
- Header: "Length"
- Question: "Approximately how many slides?"
- Options:
  - "Short (5-10)" — Quick pitch, lightning talk
  - "Medium (10-20)" — Standard presentation
  - "Long (20+)" — Deep dive, comprehensive talk

**Question 3: Content**
- Header: "Content"
- Question: "Do you have the content ready, or do you need help structuring it?"
- Options:
  - "I have all content ready" — Just need to design the presentation
  - "I have rough notes" — Need help organizing into slides
  - "I have a topic only" — Need help creating the full outline

**Question 4: Images**
- Header: "Images"
- Question: "Do you have images to include?"
- Options:
  - "No images" — Text-only presentation (use CSS-generated visuals instead)
  - "Yes, I'll provide paths" — I have figures from my analysis, external references, or both
  - "Yes, I'll drop them in the folders" — I'll manually place files into `figures-for-slides/` and/or `figures-external/` after the folder is created

**If user selects "Yes, I'll provide paths"**, ask a follow-up to collect the path(s). The user can provide one or two folder paths. During image evaluation (Step 1.2), each image is categorized and copied to the appropriate subfolder:
- **Analysis figures** (your own plots, notebook outputs, diagrams you generated) → `figures-for-slides/`
- **External references** (paper screenshots, concept diagrams from other sources, logos) → `figures-external/`

**If user selects "Yes, I'll drop them in"**, the skill creates both folders in Phase 1.5 and waits for the user to populate them before proceeding to evaluation.

If user has content, ask them to share it (text, bullet points, images, etc.).

### Step 1.2: Image Evaluation

**User-provided assets are important visual anchors** — but not every asset is necessarily usable. The first step is always to evaluate. After evaluation, the curated assets become additional context that shapes how the presentation is built. This is a **co-design process**: text content + curated visuals together inform the slide structure from the start, not a post-hoc "fit images in after the fact."

**If user selected "No images"** → Skip the entire image pipeline. Proceed directly to Phase 2 (Style Discovery) and Phase 3 (Generate Presentation) using text content only. The presentation will use CSS-generated visuals (gradients, shapes, patterns, typography) for visual interest — this is the original behavior and produces fully polished results without any images.

**If user has images:**

**Important:** Image evaluation happens **after** Phase 1.5 (Project Folder Setup). Images should already be in `figures-for-slides/` (analysis figures) and/or `figures-external/` (external references) — either copied there from user-provided paths or placed manually by the user.

1. **Scan both folders** — Use `ls` to list all image files (`.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`) in `figures-for-slides/` and `figures-external/`
2. **View each image** — Use the Read tool to see what each image contains (Claude is multimodal)
3. **Evaluate each image** — For each image, assess:
   - Filename and dimensions
   - What it shows (screenshot, logo, chart, diagram, photo)
   - **Usability:** Is the image clear, relevant to the presentation topic, and high enough quality? Mark as `USABLE` or `NOT USABLE` (with reason: blurry, irrelevant, broken, etc.)
   - **Content signal:** What feature or concept does this image represent? (e.g., "chat_ui.png" → "conversational interface feature")
   - Shape: square, landscape, portrait, circular
   - Dominant colors (important for style compatibility later)
4. **Present the evaluation and proposed slide outline to the user** — Show which images are usable and which are not, with reasons. Then show the proposed slide outline with image assignments.

**Co-design: curated assets inform the outline**

After evaluation, the **usable** images become context for planning the slide structure alongside text content. This is not "plan slides then add images" — it's designing the presentation around both text and visuals from the start:

- 3 usable product screenshots → plan 3 feature slides, each anchored by one screenshot
- 1 usable logo → title slide and/or closing slide
- 1 usable architecture diagram → dedicated "How It Works" slide
- 1 blurry/irrelevant image → excluded, with explanation to user

This means curated images are factored in **before** style selection (Phase 2) and **before** HTML generation (Phase 3). They are co-equal context in the design process.

5. **Confirm outline via AskUserQuestion** — Do NOT break the flow by asking the user to type free text. Use AskUserQuestion to confirm:

**Question: Outline Confirmation**
- Header: "Outline"
- Question: "Does this slide outline and image selection look right?"
- Options:
  - "Looks good, proceed" — Move on to style selection
  - "Adjust images" — I want to change which images go where
  - "Adjust outline" — I want to change the slide structure

This keeps the entire flow in the AskUserQuestion format without dropping to free-text chat.

---

## Phase 1.5: Project Folder Setup

**After Phase 1 content discovery is complete** (we now have a title/topic), create the presentation's project folder. This is the home for ALL files related to this presentation.

### Folder Naming Convention

```
YYMMDD-slugified-presentation-title/
```

**Slugification rules:**
- Lowercase the title
- Replace spaces and special characters with dashes
- Strip consecutive dashes
- Truncate to ~50 characters if very long
- Prepend today's date in YYMMDD format

**Examples:**
- "Variant Effect Map Pipeline" → `260303-variant-effect-map-pipeline/`
- "Q1 2026 Team Update" → `260303-q1-2026-team-update/`
- "My AI Startup Pitch" → `260303-my-ai-startup-pitch/`

### Folder Structure

Create this structure immediately:

```
YYMMDD-presentation-name/
├── figures-for-slides/            # Your own analysis figures (plots, notebook outputs, diagrams you made)
├── figures-external/              # External reference images (paper screenshots, concept diagrams, logos)
└── .previews/                     # Temporary: style previews (deleted in Phase 5)
```

The following files are generated later in the workflow:
```
├── presentation.html              # Linked version (local editing, lightweight)
├── presentation-portable.html     # Embedded version (self-contained, for sharing)
├── presentation-info.md           # Metadata: style, date, slide count
├── content-outline.md             # Original content + style decision trail
└── speaker-notes.md               # Only if notes exist (PPT or user-provided)
```

### Image Population

The two image folders serve different purposes based on **provenance**:

| Folder | Contains | Examples |
|--------|----------|----------|
| `figures-for-slides/` | **Your own** analysis outputs | Plots from notebooks, generated diagrams, pipeline outputs |
| `figures-external/` | **External** reference material | Paper screenshots, concept diagrams from other sources, logos, stock images |

**If user provided folder path(s) in Phase 1:**
1. **Copy** image files (`.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`) from the user's source path(s) into the appropriate subfolder
2. During evaluation (Step 1.2), categorize each image and place it in the right folder if not already there
3. All subsequent work (evaluation, processing, HTML generation) uses images from these two folders

**If user chose to drop files manually:**
1. Both folders are created empty
2. Inform the user: "Drop your analysis figures into `figures-for-slides/` and any external references into `figures-external/`, then let me know when ready."

**Processing happens in-place:** When Pillow operations are needed (resize, crop, etc.), processed images are saved alongside the originals in the **same folder** with a descriptive suffix (e.g., `logo_round.png`, `screenshot_resized.png`). Originals are never overwritten.

This makes the presentation folder fully self-contained — all inputs and outputs in one place.

### Content Outline (Start Building)

Create `content-outline.md` at this point with the content gathered so far:

```markdown
# Content Outline

## Source Content
[User's original bullet points / notes / topic as provided]

## Slide Outline
[The outline confirmed in Step 1.2, with image assignments if applicable]

## Style Decisions
(Populated after Phase 2)
```

This file gets updated again after Phase 2 with the style decision trail.

### All Subsequent Paths Are Relative to This Folder

From this point forward, all file operations (previews, HTML generation, image processing, metadata) happen **inside** the presentation folder. The user's project root stays clean.

---

## Phase 2: Style Discovery (Visual Exploration)

**CRITICAL: This is the "show, don't tell" phase.**

### DESIGN.md Check (run first)

Before style selection, check for a design system:

1. Look for `DESIGN.md` in the project root, then `~/.claude/DESIGN.md` (global default)
2. If found, read it and pre-load the aesthetic direction, color palette, and typography
3. Ask the user: "I found your design system (DESIGN.md). Want me to **use it as the starting point** (recommended), or **explore fresh styles** for this presentation?"
4. If using DESIGN.md: skip mood selection, generate previews using the established palette (Satoshi + DM Sans, Ochre & Charcoal colors, editorial layout), then let the user adjust
5. If exploring fresh: continue to standard style discovery below

This ensures presentations maintain visual identity consistency across talks without manual re-specification.

---

Most people can't articulate design preferences in words. Instead of asking "do you want minimalist or bold?", we generate mini-previews and let them react.

### How Users Choose Presets

Users can select a style in **three ways**:

**Option A: DESIGN.md Identity (when DESIGN.md exists)**
- Pre-loaded from the user's established design system
- Generates preview using the defined palette, typography, and aesthetic
- User can adjust from this baseline
- This is best for maintaining cross-presentation consistency

**Option B: Guided Discovery (Default when no DESIGN.md)**
- User answers mood questions
- Skill generates 3 preview files based on their answers
- User views previews in browser and picks their favorite
- This is best for users who don't have a specific style in mind

**Option C: Direct Selection**
- If user already knows what they want, they can request a preset by name
- Example: "Use the Bold Signal style" or "I want something like Dark Botanical"
- Skip to Phase 3 immediately

**Available Presets:**
| Preset | Vibe | Best For |
|--------|------|----------|
| Bold Signal | Confident, high-impact | Pitch decks, keynotes |
| Electric Studio | Clean, professional | Agency presentations |
| Creative Voltage | Energetic, retro-modern | Creative pitches |
| Dark Botanical | Elegant, sophisticated | Premium brands |
| Notebook Tabs | Editorial, organized | Reports, reviews |
| Pastel Geometry | Friendly, approachable | Product overviews |
| Split Pastel | Playful, modern | Creative agencies |
| Vintage Editorial | Witty, personality-driven | Personal brands |
| Neon Cyber | Futuristic, techy | Tech startups |
| Terminal Green | Developer-focused | Dev tools, APIs |
| Swiss Modern | Minimal, precise | Corporate, data |
| Paper & Ink | Literary, thoughtful | Storytelling |

### Step 2.0: Style Path Selection

First, ask how the user wants to choose their style:

**Question: Style Selection Method**
- Header: "Style"
- Question: "How would you like to choose your presentation style?"
- Options:
  - "Show me options" — Generate 3 previews based on my needs (recommended for most users)
  - "I know what I want" — Let me pick from the preset list directly

**If "Show me options"** → Continue to Step 2.1 (Mood Selection)

**If "I know what I want"** → Show preset picker:

**Question: Pick a Preset**
- Header: "Preset"
- Question: "Which style would you like to use?"
- Options:
  - "Bold Signal" — Vibrant card on dark, confident and high-impact
  - "Dark Botanical" — Elegant dark with soft abstract shapes
  - "Notebook Tabs" — Editorial paper look with colorful section tabs
  - "Pastel Geometry" — Friendly pastels with decorative pills

(If user picks one, skip to Phase 3. If they want to see more options, show additional presets or proceed to guided discovery.)

### Step 2.1: Mood Selection (Guided Discovery)

**Question 1: Feeling**
- Header: "Vibe"
- Question: "What feeling should the audience have when viewing your slides?"
- Options:
  - "Impressed/Confident" — Professional, trustworthy, this team knows what they're doing
  - "Excited/Energized" — Innovative, bold, this is the future
  - "Calm/Focused" — Clear, thoughtful, easy to follow
  - "Inspired/Moved" — Emotional, storytelling, memorable
- multiSelect: true (can choose up to 2)

### Step 2.2: Generate Style Previews

Based on their mood selection, generate **3 distinct style previews** as mini HTML files in a temporary directory. Each preview should be a single title slide showing:

- Typography (font choices, heading/body hierarchy)
- Color palette (background, accent, text colors)
- Animation style (how elements enter)
- Overall aesthetic feel

**Preview Styles to Consider (pick 3 based on mood):**

| Mood | Style Options |
|------|---------------|
| Impressed/Confident | "Bold Signal", "Electric Studio", "Dark Botanical" |
| Excited/Energized | "Creative Voltage", "Neon Cyber", "Split Pastel" |
| Calm/Focused | "Notebook Tabs", "Paper & Ink", "Swiss Modern" |
| Inspired/Moved | "Dark Botanical", "Vintage Editorial", "Pastel Geometry" |

**IMPORTANT: Never use these generic patterns:**
- Purple gradients on white backgrounds
- Inter, Roboto, or system fonts
- Standard blue primary colors
- Predictable hero layouts

**Instead, use distinctive choices:**
- Unique font pairings (Clash Display, Satoshi, Cormorant Garamond, DM Sans, etc.)
- Cohesive color themes with personality
- Atmospheric backgrounds (gradients, subtle patterns, depth)
- Signature animation moments

### Step 2.3: Present Previews

Create the previews inside the presentation folder's `.previews/` directory (created in Phase 1.5):

```
YYMMDD-presentation-name/.previews/
├── style-a.html   # First style option
├── style-b.html   # Second style option
└── style-c.html   # Third style option
```

Each preview file should be:
- Self-contained (inline CSS/JS)
- A single "title slide" showing the aesthetic
- Animated to demonstrate motion style
- ~50-100 lines, not a full presentation

**Logo in previews (if available):** If the user provided images in Step 1.2 and a logo was identified as `USABLE`, embed it (base64) into each of the 3 style previews. This creates a "wow moment" — the user sees their own brand identity styled three different ways, making the choice feel personal rather than abstract. Apply any necessary processing (e.g., circular crop) per-style so each preview shows the logo as it would actually appear in the final presentation. If no logo was provided, generate previews without one — this is fine.

Present to user:
```
I've created 3 style previews for you to compare:

**Style A: [Name]** — [1 sentence description]
**Style B: [Name]** — [1 sentence description]
**Style C: [Name]** — [1 sentence description]

Open each file to see them in action:
- YYMMDD-presentation-name/.previews/style-a.html
- YYMMDD-presentation-name/.previews/style-b.html
- YYMMDD-presentation-name/.previews/style-c.html

Take a look and tell me:
1. Which style resonates most?
2. What do you like about it?
3. Anything you'd change?
```

Then use AskUserQuestion:

**Question: Pick Your Style**
- Header: "Style"
- Question: "Which style preview do you prefer?"
- Options:
  - "Style A: [Name]" — [Brief description]
  - "Style B: [Name]" — [Brief description]
  - "Style C: [Name]" — [Brief description]
  - "Mix elements" — Combine aspects from different styles

If "Mix elements", ask for specifics.

---

## Phase 3: Generate Presentation

Now generate the full presentation based on:
- Content from Phase 1 (text only, or text + curated images)
- Style from Phase 2

If the user provided images, the slide outline already incorporates them as visual anchors from Step 1.2. If not, proceed with text-only content — CSS-generated visuals (gradients, shapes, patterns) provide visual interest.

### Image Pipeline (skip if no images)

If the user chose "No images" in Step 1.2, **skip this entire section** and go straight to generating HTML. The presentation will be text-only with CSS-generated visuals — this is a fully supported, first-class path.

If the user provided images, execute these steps **before** generating HTML.

**Key principle: Co-design, not post-hoc.** The curated images from Step 1.2 (those marked `USABLE`) are already part of the slide outline. The pipeline's job here is to process images for the chosen style and place them in the HTML.

#### Step 3.1: Image Processing (Pillow)

For each curated image, determine what processing it needs based on the chosen style (e.g., circular crop for logos, resize for large files) and what CSS framing will bridge any color gaps between the image and the style's palette. Then process accordingly.

**Rules:**
- **Never repeat** the same image on multiple slides (except logos which may bookend title + closing)
- **Always add CSS framing** (border, glow, shadow) for images whose colors clash with the style's palette

**Dependency:** Python `Pillow` library (the standard image processing library for Python).

```bash
# Install if not available (portable across macOS/Linux/Windows)
pip install Pillow
```

This is analogous to how `python-pptx` is used in Phase 4 (PPT Conversion) — a standard, well-maintained Python package that any user can install.

**Common processing operations:**

```python
from PIL import Image, ImageDraw

# ─── Circular Crop (for logos on modern/clean styles) ───
def crop_circle(input_path, output_path):
    """Crop a square image to a circle with transparent background."""
    img = Image.open(input_path).convert('RGBA')
    w, h = img.size
    # Make square if not already
    size = min(w, h)
    left = (w - size) // 2
    top = (h - size) // 2
    img = img.crop((left, top, left + size, top + size))
    # Create circular mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, size, size], fill=255)
    img.putalpha(mask)
    img.save(output_path, 'PNG')

# ─── Resize (for oversized images that inflate the HTML) ───
def resize_max(input_path, output_path, max_dim=1200):
    """Resize image so largest dimension <= max_dim. Preserves aspect ratio."""
    img = Image.open(input_path)
    img.thumbnail((max_dim, max_dim), Image.LANCZOS)
    img.save(output_path, quality=85)

# ─── Add Padding / Background (for images that need breathing room) ───
def add_padding(input_path, output_path, padding=40, bg_color=(0, 0, 0, 0)):
    """Add transparent padding around an image."""
    img = Image.open(input_path).convert('RGBA')
    w, h = img.size
    new = Image.new('RGBA', (w + 2*padding, h + 2*padding), bg_color)
    new.paste(img, (padding, padding), img)
    new.save(output_path, 'PNG')
```

**When to apply each operation:**

| Situation | Operation |
|-----------|-----------|
| Square logo on a style with rounded aesthetics | `crop_circle()` |
| Image > 1MB (slow to load) | `resize_max(max_dim=1200)` |
| Screenshot needs breathing room in layout | `add_padding()` |
| Image has wrong aspect ratio for its slide slot | Manual crop with `img.crop((left, top, right, bottom))` |

**Save processed images in-place** alongside the original in whichever folder it came from, with a descriptive suffix (e.g., `logo_round.png`, `chart_resized.png`). Never overwrite the original file.

#### Step 3.2: Place Images

**In `presentation.html` (linked version):** Use relative file paths from the HTML file. Images can come from **either** folder depending on their provenance:

```html
<!-- Analysis figure (your own plot) -->
<img src="figures-for-slides/variant_effect_map.png" alt="Variant Effect Map" class="slide-image">
<!-- External reference (paper screenshot, processed in-place) -->
<img src="figures-external/paper_fig3_resized.png" alt="Published results" class="slide-image screenshot">
<!-- Logo (external, circular-cropped in-place) -->
<img src="figures-external/logo_round.png" alt="Logo" class="slide-image logo">
```

This keeps the linked HTML lightweight and images easy to swap. The **portable version** (`presentation-portable.html`) is generated separately with base64-embedded images — see "Portable Version Generation" below.

**Image CSS classes (adapt border/glow colors to match the chosen style):**
```css
/* Base image constraint — CRITICAL for viewport fitting */
.slide-image {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
    border-radius: 8px;
}

/* Screenshots: add framing to bridge color gaps with the style */
.slide-image.screenshot {
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Logos: smaller, no frame */
.slide-image.logo {
    max-height: min(30vh, 200px);
}
```

**IMPORTANT:** Adapt the `.screenshot` border and shadow colors to match the chosen style's accent color. For example:
- Dark Botanical (gold accent): `border: 1px solid rgba(197, 160, 89, 0.2); box-shadow: 0 0 20px rgba(197, 160, 89, 0.08);`
- Creative Voltage (neon yellow): `border: 2px solid rgba(212, 255, 0, 0.25); box-shadow: 0 0 20px rgba(212, 255, 0, 0.08);`

**Placement patterns:**
- **Title slide:** Logo centered above or beside the title
- **Feature slides:** Screenshot on one side, text on the other (two-column layout)
- **Full-bleed:** Image as slide background with text overlay (use with caution)
- **Inline:** Image within content flow, centered, with caption below

**Note:** Processed images (e.g. `logo_round.png`) live alongside their originals in the same folder with a descriptive suffix. Originals are never overwritten.

### File Structure

Every presentation lives in a dated project folder (created in Phase 1.5):

```
YYMMDD-presentation-name/
├── presentation.html              # Linked version (local editing, lightweight)
├── presentation-portable.html     # Embedded version (self-contained, for sharing)
├── figures-for-slides/            # Your analysis figures (plots, notebook outputs)
│   ├── variant_effect_map.png     #   original from your notebook
│   └── coverage_plot_resized.png  #   processed in-place (suffix added)
├── figures-external/              # External references (paper figs, logos, screenshots)
│   ├── logo.png                   #   original
│   ├── logo_round.png             #   processed in-place (suffix added)
│   └── paper_fig3.png
├── presentation-info.md           # Metadata: style, date, slide count
├── content-outline.md             # Original content + style decision trail
└── speaker-notes.md               # Only if notes exist
```

**Two HTML versions:**
- `presentation.html` — References images via relative paths (`figures-for-slides/` and `figures-external/`). Lightweight, used for local editing and iteration.
- `presentation-portable.html` — All images base64-embedded inline. Truly self-contained — can be emailed, shared on Slack, opened by anyone without needing the folder.

### Portable Version Generation

**After generating `presentation.html`**, automatically create the portable version. Use this Python pipeline:

```python
import base64, re
from pathlib import Path

def generate_portable(presentation_dir: Path) -> None:
    """
    Read presentation.html, embed all images as base64 data URIs,
    write presentation-portable.html.
    """
    src = presentation_dir / "presentation.html"
    dst = presentation_dir / "presentation-portable.html"
    html = src.read_text(encoding="utf-8")

    def embed_image(match):
        src_attr = match.group(1)
        img_path = presentation_dir / src_attr
        if not img_path.exists():
            return match.group(0)  # Leave unchanged if file missing
        suffix = img_path.suffix.lower()
        mime = {
            ".png": "image/png", ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg", ".gif": "image/gif",
            ".svg": "image/svg+xml", ".webp": "image/webp",
        }.get(suffix, "application/octet-stream")
        b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
        return f'src="data:{mime};base64,{b64}"'

    # Replace all image src paths (from either figures folder) with base64 data URIs
    portable_html = re.sub(
        r'src="(figures-(?:for-slides|external)/[^"]+)"',
        embed_image, html
    )
    dst.write_text(portable_html, encoding="utf-8")
```

**When to regenerate:** Every time `presentation.html` is modified (e.g., user requests a slide edit), regenerate `presentation-portable.html` immediately and confirm: "Updated both linked and portable versions."

### HTML Architecture

Follow this structure for all presentations:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>

    <!-- Fonts (use Fontshare or Google Fonts) -->
    <link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=...">

    <style>
        /* ===========================================
           CSS CUSTOM PROPERTIES (THEME)
           Easy to modify: change these to change the whole look
           =========================================== */
        :root {
            /* Colors */
            --bg-primary: #0a0f1c;
            --bg-secondary: #111827;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --accent: #00ffcc;
            --accent-glow: rgba(0, 255, 204, 0.3);

            /* Typography - MUST use clamp() for responsive scaling */
            --font-display: 'Clash Display', sans-serif;
            --font-body: 'Satoshi', sans-serif;
            --title-size: clamp(2rem, 6vw, 5rem);
            --subtitle-size: clamp(0.875rem, 2vw, 1.25rem);
            --body-size: clamp(0.75rem, 1.2vw, 1rem);

            /* Spacing - MUST use clamp() for responsive scaling */
            --slide-padding: clamp(1.5rem, 4vw, 4rem);
            --content-gap: clamp(1rem, 2vw, 2rem);

            /* Animation */
            --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
            --duration-normal: 0.6s;
        }

        /* ===========================================
           BASE STYLES
           =========================================== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
            scroll-snap-type: y mandatory;
            height: 100%;
        }

        body {
            font-family: var(--font-body);
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
            height: 100%;
        }

        /* ===========================================
           SLIDE CONTAINER
           CRITICAL: Each slide MUST fit exactly in viewport
           - Use height: 100vh (NOT min-height)
           - Use overflow: hidden to prevent scroll
           - Content must scale with clamp() values
           =========================================== */
        .slide {
            width: 100vw;
            height: 100vh; /* EXACT viewport height - no scrolling */
            height: 100dvh; /* Dynamic viewport height for mobile */
            padding: var(--slide-padding);
            scroll-snap-align: start;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden; /* Prevent any content overflow */
        }

        /* Content wrapper that prevents overflow */
        .slide-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            max-height: 100%;
            overflow: hidden;
        }

        /* ===========================================
           RESPONSIVE BREAKPOINTS
           Adjust content for different screen sizes
           =========================================== */
        @media (max-height: 600px) {
            :root {
                --slide-padding: clamp(1rem, 3vw, 2rem);
                --content-gap: clamp(0.5rem, 1.5vw, 1rem);
            }
        }

        @media (max-width: 768px) {
            :root {
                --title-size: clamp(1.5rem, 8vw, 3rem);
            }
        }

        @media (max-height: 500px) and (orientation: landscape) {
            /* Extra compact for landscape phones */
            :root {
                --title-size: clamp(1.25rem, 5vw, 2rem);
                --slide-padding: clamp(0.75rem, 2vw, 1.5rem);
            }
        }

        /* ===========================================
           ANIMATIONS
           Trigger via .visible class (added by JS on scroll)
           =========================================== */
        .reveal {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity var(--duration-normal) var(--ease-out-expo),
                        transform var(--duration-normal) var(--ease-out-expo);
        }

        .slide.visible .reveal {
            opacity: 1;
            transform: translateY(0);
        }

        /* Stagger children */
        .reveal:nth-child(1) { transition-delay: 0.1s; }
        .reveal:nth-child(2) { transition-delay: 0.2s; }
        .reveal:nth-child(3) { transition-delay: 0.3s; }
        .reveal:nth-child(4) { transition-delay: 0.4s; }

        /* ... more styles ... */
    </style>
</head>
<body>
    <!-- Progress bar (optional) -->
    <div class="progress-bar"></div>

    <!-- Navigation dots (optional) -->
    <nav class="nav-dots">
        <!-- Generated by JS -->
    </nav>

    <!-- Slides -->
    <section class="slide title-slide">
        <h1 class="reveal">Presentation Title</h1>
        <p class="reveal">Subtitle or author</p>
    </section>

    <section class="slide">
        <h2 class="reveal">Slide Title</h2>
        <p class="reveal">Content...</p>
    </section>

    <!-- More slides... -->

    <script>
        /* ===========================================
           SLIDE PRESENTATION CONTROLLER
           Handles navigation, animations, and interactions
           =========================================== */

        class SlidePresentation {
            constructor() {
                // ... initialization
            }

            // ... methods
        }

        // Initialize
        new SlidePresentation();
    </script>
</body>
</html>
```

### Required JavaScript Features

Every presentation should include:

1. **SlidePresentation Class** — Main controller
   - Keyboard navigation (arrows, space)
   - Touch/swipe support
   - Mouse wheel navigation
   - Progress bar updates
   - Navigation dots

2. **Intersection Observer** — For scroll-triggered animations
   - Add `.visible` class when slides enter viewport
   - Trigger CSS animations efficiently

3. **Zoom-Aware Navigation (REQUIRED)** — Adapts scrolling behavior based on zoom level
   - At 1x zoom: scroll-snap is active, scrolling advances between slides normally
   - When zoomed in (>1x): scroll-snap is disabled, scrolling pans freely around the current slide
   - When zoom returns to 1x: scroll-snap re-enables automatically
   - Pinch-to-zoom and Ctrl+scroll work natively without interference
   - This MUST be included in every presentation's SlidePresentation class

   **Navigation behavior summary:**
   - Arrow keys (left/right, up/down), Space, PageUp/PageDown — move between slides
   - Scroll/two-finger swipe — at 1x zoom, CSS scroll-snap snaps between slides. Once zoomed in, scrolling pans around the slide freely
   - Pinch-to-zoom — works natively, no interference
   - Nav dots on the right — click to jump to any slide

   ```javascript
   /* ===========================================
      ZOOM-AWARE NAVIGATION
      Adapts scroll behavior based on browser zoom level.
      - At 1x zoom: scroll-snap active, scrolling advances slides
      - Zoomed in: scroll-snap disabled, scrolling pans freely
      - Uses visualViewport API (supported in all modern browsers)
        to detect zoom level reliably.
      =========================================== */

   // Inside SlidePresentation class constructor:
   this.isZoomed = false;
   this.initZoomAwareNav();

   // Methods:
   initZoomAwareNav() {
       // visualViewport.scale reflects pinch-zoom on mobile
       // and page zoom on desktop. 1.0 = no zoom.
       if (window.visualViewport) {
           // 'resize' fires on any zoom or viewport change
           window.visualViewport.addEventListener('resize', () => {
               this.updateZoomState();
           });
       }

       // Fallback: also detect Ctrl+scroll zoom on desktop.
       // Browsers update window dimensions on zoom, so we
       // poll briefly after a Ctrl+wheel event to catch it.
       window.addEventListener('wheel', (e) => {
           if (e.ctrlKey) {
               // Small delay lets the browser apply the zoom
               setTimeout(() => this.updateZoomState(), 100);
           }
       }, { passive: true });

       // Initial check in case page loads already zoomed
       this.updateZoomState();
   }

   updateZoomState() {
       // visualViewport.scale: pinch-zoom level (mobile + desktop)
       // window.outerWidth / window.innerWidth: desktop browser zoom
       // Either being >1 means the user is zoomed in.
       const pinchScale = window.visualViewport
           ? window.visualViewport.scale
           : 1;
       const browserZoom = window.outerWidth / window.innerWidth;
       const isNowZoomed = pinchScale > 1.05 || browserZoom > 1.05;

       if (isNowZoomed !== this.isZoomed) {
           this.isZoomed = isNowZoomed;
           // Toggle scroll-snap based on zoom state
           document.documentElement.style.scrollSnapType =
               isNowZoomed ? 'none' : 'y mandatory';
       }
   }
   ```

4. **Optional Enhancements** (based on style):
   - Custom cursor with trail
   - Particle system background (canvas)
   - Parallax effects
   - 3D tilt on hover
   - Magnetic buttons
   - Counter animations

### Code Quality Requirements

**Comments:**
Every section should have clear comments explaining:
- What it does
- Why it exists
- How to modify it

```javascript
/* ===========================================
   CUSTOM CURSOR
   Creates a stylized cursor that follows mouse with a trail effect.
   - Uses lerp (linear interpolation) for smooth movement
   - Grows larger when hovering over interactive elements
   =========================================== */
class CustomCursor {
    constructor() {
        // ...
    }
}
```

**Accessibility:**
- Semantic HTML (`<section>`, `<nav>`, `<main>`)
- Keyboard navigation works
- ARIA labels where needed
- Reduced motion support

```css
@media (prefers-reduced-motion: reduce) {
    .reveal {
        transition: opacity 0.3s ease;
        transform: none;
    }
}
```

**CSS Function Negation:**
- Never negate CSS functions directly — `-clamp()`, `-min()`, `-max()` are silently ignored by browsers with no console error
- Always use `calc(-1 * clamp(...))` instead. See STYLE_PRESETS.md → "CSS Gotchas" for details.

**Responsive & Viewport Fitting (CRITICAL):**

**See the "CRITICAL: Viewport Fitting Requirements" section above for complete CSS and guidelines.**

Quick reference:
- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- All typography and spacing must use `clamp()`
- Respect content density limits (max 4-6 bullets, max 6 cards, etc.)
- Include breakpoints for heights: 700px, 600px, 500px
- When content doesn't fit → split into multiple slides, never scroll
- Include `@media print` block for PDF export (see Viewport Fitting Requirements section)
- Include zoom-safe navigation JS (see Required JavaScript Features section)

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

### Step 4.1: Extract Content

Use Python with `python-pptx` to extract:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
import json
import os
import base64

def extract_pptx(file_path, output_dir):
    """
    Extract all content from a PowerPoint file.
    Returns a JSON structure with slides, text, and images.
    """
    prs = Presentation(file_path)
    slides_data = []

    # Create figures-external directory (raw extracted images go here)
    figures_ext_dir = os.path.join(output_dir, 'figures-external')
    os.makedirs(figures_ext_dir, exist_ok=True)

    for slide_num, slide in enumerate(prs.slides):
        slide_data = {
            'number': slide_num + 1,
            'title': '',
            'content': [],
            'images': [],
            'notes': ''
        }

        for shape in slide.shapes:
            # Extract title
            if shape.has_text_frame:
                if shape == slide.shapes.title:
                    slide_data['title'] = shape.text
                else:
                    slide_data['content'].append({
                        'type': 'text',
                        'content': shape.text
                    })

            # Extract images
            if shape.shape_type == 13:  # Picture
                image = shape.image
                image_bytes = image.blob
                image_ext = image.ext
                image_name = f"slide{slide_num + 1}_img{len(slide_data['images']) + 1}.{image_ext}"
                image_path = os.path.join(figures_ext_dir, image_name)

                with open(image_path, 'wb') as f:
                    f.write(image_bytes)

                slide_data['images'].append({
                    'path': f"figures-external/{image_name}",
                    'width': shape.width,
                    'height': shape.height
                })

        # Extract notes
        if slide.has_notes_slide:
            notes_frame = slide.notes_slide.notes_text_frame
            slide_data['notes'] = notes_frame.text

        slides_data.append(slide_data)

    return slides_data
```

### Step 4.2: Confirm Content Structure

Present the extracted content to the user:

```
I've extracted the following from your PowerPoint:

**Slide 1: [Title]**
- [Content summary]
- Images: [count]

**Slide 2: [Title]**
- [Content summary]
- Images: [count]

...

All images have been saved to `figures-external/`.

Does this look correct? Should I proceed with style selection?
```

### Step 4.3: Style Selection

Proceed to Phase 2 (Style Discovery) with the extracted content in mind.

### Step 4.4: Generate HTML

Convert the extracted content into the chosen style, preserving:
- All text content
- All images (processed in-place in `figures-external/`, referenced via relative paths in `presentation.html`)
- Slide order
- Any speaker notes (exported as `speaker-notes.md` in Phase 5)

**Note:** For PPT conversions, the dated project folder (Phase 1.5) is created using the PPT filename or extracted title. Images extracted by `python-pptx` go to `figures-external/` (since they come from an external source file). Processing (resize, crop) happens in-place in that folder.

---

## Phase 5: Delivery

### Final Output

When the presentation is complete, execute these steps in order:

1. **Generate portable version**
   - Run the `generate_portable()` function (see Phase 3 → Portable Version Generation)
   - Creates `presentation-portable.html` with all images base64-embedded

2. **Generate `presentation-info.md`**
   ```markdown
   # Presentation Info

   - **Title:** [presentation title]
   - **Created:** YYYY-MM-DD
   - **Style:** [preset name]
   - **Slides:** [count]
   - **Images:** [X from figures-for-slides/, Y from figures-external/, Z excluded]
   - **Files:**
     - `presentation.html` — Local editing version (linked images)
     - `presentation-portable.html` — Shareable version (embedded images, can be emailed/shared)
     - `figures-for-slides/` — Your analysis figures (plots, notebook outputs)
     - `figures-external/` — External reference images (paper screenshots, logos, etc.)
     - `content-outline.md` — Original content + style decision trail
   ```

3. **Finalize `content-outline.md`**
   - This file was started in Phase 1.5 with the source content and slide outline
   - Now append the style decision trail from Phase 2:
   ```markdown
   ## Style Decisions
   - **Mood selected:** [mood(s) from Step 2.1]
   - **Previews shown:** [Style A name], [Style B name], [Style C name]
   - **Chosen style:** [final choice]
   - **Customizations:** [any tweaks requested, or "None"]
   ```

4. **Generate `speaker-notes.md`** (if applicable)
   - Only if notes exist (from PPT conversion or user-provided)
   ```markdown
   # Speaker Notes

   ## Slide 1: [Title]
   [notes]

   ## Slide 2: [Title]
   [notes]
   ```

5. **First Impression Self-Check (before declaring done)**
   Read through the generated HTML and perform a quick gut-check:
   - "This presentation communicates **[what]** at first glance."
   - "The title slide hierarchy: my eye goes to **[1]**, **[2]**, **[3]**."
   - "AI Slop check: **[pass/flag]**" — scan for any anti-patterns from STYLE_PRESETS.md or DESIGN.md blacklists
   - "DESIGN.md compliance: **[yes/no/N/A]**" — if DESIGN.md was used, verify fonts and colors match

   Present this mini-review to the user alongside the summary. If any AI Slop patterns are detected, flag them and offer to fix before finalizing.

6. **Clean up temporary files**
   - Delete the `.previews/` directory inside the presentation folder

7. **Open the presentation**
   - Use `open YYMMDD-presentation-name/presentation.html` to launch in browser

8. **Provide summary**
```
Your presentation is ready!

Folder: YYMMDD-presentation-name/
Style: [Style Name]
Slides: [count]

**Two versions:**
- `presentation.html` — For local viewing and editing
- `presentation-portable.html` — Self-contained, share via email/Slack

**Navigation:**
- Arrow keys (left/right, up/down), Space, PageUp/PageDown — move between slides
- Scroll/two-finger swipe — snaps between slides at 1x zoom; pans freely when zoomed in
- Pinch-to-zoom / Ctrl+scroll — zoom works natively, no interference
- Nav dots on the right — click to jump to any slide
- Ctrl+P to save as PDF

**To customize:**
- Colors: Look for `:root` CSS variables at the top
- Fonts: Change the Fontshare/Google Fonts link
- Animations: Modify `.reveal` class timings

Would you like me to make any adjustments?
```

### Handling Subsequent Edits

When the user requests changes to the presentation after delivery:

1. Edit `presentation.html` (the linked version)
2. Regenerate `presentation-portable.html` using `generate_portable()`
3. Confirm: "Updated both linked and portable versions."

This ensures the portable version always stays in sync with the linked version.

---

## Style Reference: Effect → Feeling Mapping

Use this guide to match animations to intended feelings:

### Dramatic / Cinematic
- Slow fade-ins (1-1.5s)
- Large scale transitions (0.9 → 1)
- Dark backgrounds with spotlight effects
- Parallax scrolling
- Full-bleed images

### Techy / Futuristic
- Neon glow effects (box-shadow with accent color)
- Particle systems (canvas background)
- Grid patterns
- Monospace fonts for accents
- Glitch or scramble text effects
- Cyan, magenta, electric blue palette

### Playful / Friendly
- Bouncy easing (spring physics)
- Rounded corners (large radius)
- Pastel or bright colors
- Floating/bobbing animations
- Hand-drawn or illustrated elements

### Professional / Corporate
- Subtle, fast animations (200-300ms)
- Clean sans-serif fonts
- Navy, slate, or charcoal backgrounds
- Precise spacing and alignment
- Minimal decorative elements
- Data visualization focus

### Calm / Minimal
- Very slow, subtle motion
- High whitespace
- Muted color palette
- Serif typography
- Generous padding
- Content-focused, no distractions

### Editorial / Magazine
- Strong typography hierarchy
- Pull quotes and callouts
- Image-text interplay
- Grid-breaking layouts
- Serif headlines, sans-serif body
- Black and white with one accent

---

## Animation Patterns Reference

### Entrance Animations

```css
/* Fade + Slide Up (most common) */
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s var(--ease-out-expo),
                transform 0.6s var(--ease-out-expo);
}

.visible .reveal {
    opacity: 1;
    transform: translateY(0);
}

/* Scale In */
.reveal-scale {
    opacity: 0;
    transform: scale(0.9);
    transition: opacity 0.6s, transform 0.6s var(--ease-out-expo);
}

/* Slide from Left */
.reveal-left {
    opacity: 0;
    transform: translateX(-50px);
    transition: opacity 0.6s, transform 0.6s var(--ease-out-expo);
}

/* Blur In */
.reveal-blur {
    opacity: 0;
    filter: blur(10px);
    transition: opacity 0.8s, filter 0.8s var(--ease-out-expo);
}
```

### Background Effects

```css
/* Gradient Mesh */
.gradient-bg {
    background:
        radial-gradient(ellipse at 20% 80%, rgba(120, 0, 255, 0.3) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0, 255, 200, 0.2) 0%, transparent 50%),
        var(--bg-primary);
}

/* Noise Texture */
.noise-bg {
    background-image: url("data:image/svg+xml,..."); /* Inline SVG noise */
}

/* Grid Pattern */
.grid-bg {
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
}
```

### Interactive Effects

```javascript
/* 3D Tilt on Hover */
class TiltEffect {
    constructor(element) {
        this.element = element;
        this.element.style.transformStyle = 'preserve-3d';
        this.element.style.perspective = '1000px';
        this.bindEvents();
    }

    bindEvents() {
        this.element.addEventListener('mousemove', (e) => {
            const rect = this.element.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;

            this.element.style.transform = `
                rotateY(${x * 10}deg)
                rotateX(${-y * 10}deg)
            `;
        });

        this.element.addEventListener('mouseleave', () => {
            this.element.style.transform = 'rotateY(0) rotateX(0)';
        });
    }
}
```

---

## Troubleshooting

### Common Issues

**Fonts not loading:**
- Check Fontshare/Google Fonts URL
- Ensure font names match in CSS

**Animations not triggering:**
- Verify Intersection Observer is running
- Check that `.visible` class is being added

**Scroll snap not working:**
- Ensure `scroll-snap-type` on html/body
- Each slide needs `scroll-snap-align: start`

**Mobile issues:**
- Disable heavy effects at 768px breakpoint
- Test touch events
- Reduce particle count or disable canvas

**Performance issues:**
- Use `will-change` sparingly
- Prefer `transform` and `opacity` animations
- Throttle scroll/mousemove handlers

---

## Related Skills

- **learn** — Generate FORZARA.md documentation for the presentation
- **frontend-design** — For more complex interactive pages beyond slides
- **design-and-refine:design-lab** — For iterating on component designs

---

## Example Session Flow

1. User: "I want to create a pitch deck for my AI startup"
2. Skill asks about purpose, length, content, and images (single form)
3. User shares bullet points, provides paths to analysis figures and a logo
4. **Phase 1.5:** Skill creates `260303-my-ai-startup-pitch/`, copies analysis plots to `figures-for-slides/`, copies logo and screenshots to `figures-external/`
5. **Evaluate from both folders:** Skill views each image (multimodal), builds slide outline with image assignments:
   - `figures-for-slides/chat_ui.png` → USABLE → feature slide (user's own screenshot)
   - `figures-for-slides/dashboard.png` → USABLE → feature slide (user's own screenshot)
   - `figures-external/logo.png` → USABLE → title/closing slide
   - `figures-external/launch_card.png` → USABLE → feature slide
   - `figures-external/blurry_team.jpg` → NOT USABLE (too low resolution)
6. Skill writes initial `content-outline.md` with source content + slide outline
7. User confirms outline via AskUserQuestion
8. Skill generates 3 style previews in `.previews/`
9. User picks Style B (Neon Cyber)
10. **Process + Generate:** Skill runs Pillow operations in-place (e.g., `logo_round.png` next to `logo.png` in `figures-external/`), generates `presentation.html` referencing both folders
11. **Delivery:** Skill generates `presentation-portable.html` (base64 embedded), `presentation-info.md`, finalizes `content-outline.md` with style decisions, deletes `.previews/`
12. Skill opens `presentation.html` in browser
13. User requests tweaks → skill edits `presentation.html`, regenerates `presentation-portable.html`
14. Final folder delivered:
    ```
    260303-my-ai-startup-pitch/
    ├── presentation.html
    ├── presentation-portable.html
    ├── figures-for-slides/
    ├── figures-external/
    ├── presentation-info.md
    └── content-outline.md
    ```

---

## Conversion Session Flow

1. User: "Convert my slides.pptx to a web presentation"
2. Skill extracts content and images from PPT
3. **Phase 1.5:** Skill creates dated folder (e.g., `260303-quarterly-update/`), places extracted images in `figures-external/`
4. Skill confirms extracted content with user, writes `content-outline.md`
5. Skill asks about desired feeling/style, generates previews in `.previews/`
6. User picks a style
7. Skill processes images in-place in `figures-external/`, generates `presentation.html`
8. **Delivery:** Generates `presentation-portable.html`, `presentation-info.md`, `speaker-notes.md` (from PPT notes), finalizes `content-outline.md`, deletes `.previews/`
9. Final folder delivered with both HTML versions + all metadata
