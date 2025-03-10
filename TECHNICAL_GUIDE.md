# Technical Guide for Knowledge Graph Development

This guide provides detailed information about the technical aspects of maintaining and developing the knowledge graph for the "Banach Space Representer Theorems for Neural Networks" paper.

## Environment Setup

### Python Environment

The project uses Python 3 for its utilities. The correct path to the Python interpreter is:
```bash
/usr/local/bin/python3
```

Always use this full path when executing Python scripts to ensure proper functionality.

### MathJax Configuration

MathJax is used to render LaTeX mathematical expressions in HTML files. All HTML files should include the following script references in the `<head>` section:

**For main index.html:**
```html
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script src="js/mathjax-config.js"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
```

**For node HTML files:**
```html
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script src="../js/mathjax-config.js"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
```

**IMPORTANT:** All HTML files must use the same MathJax script source (`tex-svg.js`). Do not use `tex-mml-chtml.js` as it may cause rendering inconsistencies.

## Utility Scripts

### add_mathjax.py

This utility adds MathJax script references to all HTML files in the project.

**Usage:**
```bash
/usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/add_mathjax.py
```

**What it does:**
- Scans all HTML files in the project directory
- Checks if MathJax script references are already included
- If not, adds the script references before the closing `</head>` tag
- Displays a message for each file it modifies

**When to use:**
- After creating new HTML files
- If LaTeX expressions aren't rendering correctly in the browser
- After cloning the repository to a new environment

### scan_nodes.py

This utility identifies missing nodes, broken links, and incomplete content sections.

**Usage:**
```bash
/usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/scan_nodes.py
```

**What it does:**
- Performs a depth-first traversal of the knowledge graph starting from index.html
- Checks for required sections in each node (Motivation, Example, etc.)
- Identifies links to non-existent HTML files
- Identifies HTML files not linked from any other node ("orphaned nodes")
- Outputs a comprehensive report to the `empty_nodes` file

**When to use:**
- After adding new nodes
- Before updating the project tracker
- Periodically as a quality check

### verify_mathjax_complete.py

This utility verifies that all HTML files have the correct MathJax configuration.

**Usage:**
```bash
/usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/verify_mathjax_complete.py
```

**What it does:**
- Checks all HTML files to ensure they have the correct config path and script source
- Verifies that index.html uses `js/mathjax-config.js` and node files use `../js/mathjax-config.js`
- Confirms that all files use the same MathJax script source (`tex-svg.js`)
- Provides a detailed report of any issues

**When to use:**
- After making changes to HTML files
- When math expressions aren't rendering correctly
- Before deploying to GitHub Pages

### scan_ugly_expression.py

This utility detects ASCII-style mathematical expressions that should be replaced with proper LaTeX notation.

**Usage:**
```bash
/usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/scan_ugly_expression.py
```

**What it does:**
- Performs a depth-first traversal of all HTML files
- Identifies potentially problematic math expressions like `x^2` or `max{0,x}`
- These should be formatted as `$$x^2$$` or `$$\max\{0,x\}$$`
- Outputs a report to the `ugly_expressions` file

**When to use:**
- After creating or updating content with mathematical expressions
- Before submitting work to ensure all mathematical content uses proper LaTeX

## LaTeX in HTML

### Proper LaTeX Expression Formatting

All mathematical expressions must be properly formatted using LaTeX syntax within appropriate delimiters:

- For inline math: `$expression$`
- For block/display math: `$$expression$$`

### Conversion Examples

| ASCII Math (Incorrect) | LaTeX Notation (Correct) |
|------------------------|--------------------------|
| `f(x) = sum(a_i * x^i)` | `$$f(x) = \sum_{i=1}^n a_i x^i$$` |
| `max{0, x}` | `$$\max\{0, x\}$$` |
| `x_1 + y_2 / z` | `$$x_1 + \frac{y_2}{z}$$` |
| `|v|` | `$$\|v\|$$` |
| `a^T * b` | `$$a^T b$$` |

### CSS Classes for Mathematical Content

- `class="definition"`: Use for formal definitions
- `class="theorem"`: Use for theorem statements
- `class="math"`: Use for inline mathematical notation

Example:
```html
<div class="definition">
  <p>$$\min_{f \in \mathcal{F}_m} G(Vf) + \|R_m f\|_{M(S^{d-1} \times \mathbb{R})}$$</p>
</div>
```

## Troubleshooting

### LaTeX Not Rendering

If LaTeX expressions aren't rendering properly in the browser:

1. Run the verify_mathjax_complete.py utility to check your MathJax configuration:
   ```bash
   /usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/verify_mathjax_complete.py
   ```

2. If issues are found, ensure that:
   - All files include the correct path to mathjax-config.js (either `js/mathjax-config.js` for the main index or `../js/mathjax-config.js` for nodes)
   - All files use the same MathJax script source (`tex-svg.js`)
   - The config and script tags appear in the correct order

3. If MathJax is missing entirely, run the add_mathjax.py utility:
   ```bash
   /usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/add_mathjax.py
   ```

4. Verify that all LaTeX expressions use proper formatting:
   - Inline expressions should be wrapped in single dollar signs: `$expression$`
   - Block expressions should be wrapped in double dollar signs: `$$expression$$`

5. Clear browser cache and reload the page

### Script Execution Errors

If you encounter errors running the utility scripts:

1. Ensure you're using the correct path to the Python interpreter:
   ```bash
   /usr/local/bin/python3 /path/to/script.py
   ```

2. Check that you're in the correct directory when running the script:
   ```bash
   cd /Users/dengzishan/Documents/paper_reading/distribution_NN/
   /usr/local/bin/python3 script.py
   ```

3. Verify script permissions:
   ```bash
   chmod +x /path/to/script.py
   ```

## Best Practices

1. Always use full paths to the Python interpreter when executing scripts
2. Run the utility scripts regularly to maintain project quality
3. Update the project tracker after making significant changes
4. Ensure all mathematical content uses proper LaTeX notation
5. Maintain bidirectional linking between related concepts
6. Follow the HTML template structure when creating new nodes
7. Always use the same MathJax script source (`tex-svg.js`) across all HTML files
8. Run verify_mathjax_complete.py before committing changes to ensure consistent math rendering
