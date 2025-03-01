# Banach Space Representer Theorems for Neural Networks

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://nonosecreta.github.io/distribution_NN/)

View the live knowledge graph: [https://nonosecreta.github.io/distribution_NN/](https://nonosecreta.github.io/distribution_NN/)

## Project Overview

This project creates an interactive knowledge graph for the paper "Banach Space Representer Theorems for Neural Networks and Ridge Splines" by Parhi and Nowak. The knowledge graph organizes key concepts and their relationships into interconnected HTML nodes, making the paper's technical content more accessible and navigable.

## Project Structure

- `index.html`: The root node providing an overview of the paper
- `/nodes/`: Directory containing individual concept nodes
- `/css/`: Directory containing styling information
- `scan_nodes.py`: Utility for identifying missing nodes or sections
- `scan_ugly_expression.py`: Utility for identifying ASCII math expressions
- `add_mathjax.py`: Utility for adding MathJax support to HTML files
- `project_tracker.md`: Tracks completion status of all nodes
- `empty_nodes`: Auto-generated report of missing nodes/sections
- `ugly_expressions`: Auto-generated report of ASCII math expressions

## Development Instructions

### Creating New Nodes

1. Follow the HTML template structure present in existing nodes
2. Each node must include these components:
   - Title matching the filename
   - One-sentence summary in the "concept-summary" div
   - Motivation section explaining importance/relevance
   - Key principles/proof overview section
   - Example section demonstrating practical application
   - Links to related concepts
   - Back link to main index

### Mathematical Notation

**Important**: Use formal LaTeX notation for mathematical expressions. Implement this using MathJax-style notation:

```html
<div class="definition">
  <p>$$\min_{f \in \mathcal{F}_m} G(Vf) + \|R_m f\|_{M(S^{d-1} \times \mathbb{R})}$$</p>
</div>
```

Avoid ASCII approximations like "f(x) = sum(v_k*max{0,w_k^T*x})" for mathematical expressions.

### MathJax Support

The project uses MathJax to render LaTeX expressions in the browser. All HTML files should include the MathJax script references in the `<head>` section. You can use the `add_mathjax.py` utility to automatically add MathJax support to all HTML files:

```bash
/usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/add_mathjax.py
```

If LaTeX expressions aren't rendering properly in the browser, ensure MathJax is properly included.

### Priority Development Order

1. Complete nodes directly linked from existing pages first
2. Focus on core mathematical concepts that appear frequently
3. Complete subconcepts after their parent concepts
4. Reference the `empty_nodes` file for the most current list of missing nodes

### Quality Assurance

1. Run the scan_nodes.py utility after adding new nodes:
   ```bash
   /usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/scan_nodes.py
   ```

2. Check `empty_nodes` file for any issues

3. Run the scan_ugly_expression.py utility to identify improper mathematical notation:
   ```bash
   /usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/scan_ugly_expression.py
   ```

4. Check `ugly_expressions` file for ASCII math expressions to convert to LaTeX
5. Update `project_tracker.md` with the current status of each node
6. Ensure bidirectional linking between related nodes

## Development Workflow

### Standard Development Process

1. Choose a missing node from `empty_nodes` or `project_tracker.md`
2. Create the node following the template structure
3. Include formal LaTeX mathematical notation
4. Update any nodes that should link to this new node
5. Run `scan_nodes.py` to verify completeness
6. Run `add_mathjax.py` to ensure MathJax support
7. Update `project_tracker.md` with current status

### Systematic Approach for Fixing Empty Nodes

1. **Assessment Phase**
   - Run `scan_nodes.py` to generate the `empty_nodes` report
   - Run `scan_ugly_expression.py` to check for ASCII math notation
   - Review `project_tracker.md` for current status
   - Prioritize nodes directly referenced from existing content

2. **Implementation Phase**
   - Create missing node files using the standard template
   - Ensure proper mathematical notation with LaTeX
   - Implement bidirectional linking with related concepts
   - When appropriate, create symbolic links for nodes referenced under alternative names

3. **Verification Phase**
   - Run `scan_nodes.py` again to verify fixes
   - Run `scan_ugly_expression.py` to check any remaining ASCII math issues
   - Make targeted edits to address any remaining issues
   - Update `project_tracker.md` with newly completed nodes

This systematic approach ensures consistent quality and comprehensive coverage of all concepts in the knowledge graph.

## Technical Guidance

### Mathematical Notation

All mathematical expressions must use proper LaTeX notation within `$$` delimiters, not ASCII approximations:

✓ Correct: `$$f(x) = \sum_{k=1}^K v_k\max\{0, w_k^Tx - b_k\} + u^Tx + s$$`

✗ Incorrect: `f(x) = sum(v_k*max{0,w_k^T*x - b_k}) + u^T*x + s`

Use the `scan_ugly_expression.py` utility to identify ASCII math expressions that need conversion to LaTeX.

### CSS Classes

- For proper display of mathematical expressions, keep the class names consistent:
  - Use `class="definition"` for formal definitions
  - Use `class="theorem"` for theorem statements
  - Use `class="math"` for inline mathematical notation
- CSS is already configured to style these elements appropriately
- When adding new nodes, ensure they are referenced in at least one existing node

## Utility Scripts

### scan_nodes.py
Identifies missing nodes, broken links, and incomplete content sections (Motivation, Example, etc.). Use after adding new nodes or before updating the project tracker.

**Important**: Always use the full path to the Python interpreter:
```bash
/usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/scan_nodes.py
```

### scan_ugly_expression.py
Detects ASCII-style mathematical expressions that should be replaced with proper LaTeX notation. This script performs a depth-first traversal of all HTML files, identifying potentially problematic math expressions like `x^2` or `max{0,x}` that should be formatted as `$$x^2$$` or `$$\max\{0,x\}$$`.

**Important**: Always use the full path to the Python interpreter:
```bash
/usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/scan_ugly_expression.py
```

### add_mathjax.py
Adds MathJax script references to all HTML files in the project to enable proper rendering of LaTeX expressions in the browser.

**Important**: Always use the full path to the Python interpreter:
```bash
/usr/local/bin/python3 /Users/dengzishan/Documents/paper_reading/distribution_NN/add_mathjax.py
```

## Current Status

Refer to `project_tracker.md` for the current completion status of all nodes. The knowledge graph currently includes the core concepts of the paper, with several supporting mathematical concepts still to be developed.

**YOU SOULD ALWAYS WRITE '<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script src="../js/mathjax-config.js"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>' at the head of html file to ensure the latex expression being displayed correctly!!!*
