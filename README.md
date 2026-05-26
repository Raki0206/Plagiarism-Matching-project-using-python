# Pattern Searching Engine for Academic Plagiarism Detection
## Using String Matching Algorithms — C++ Mini Project

---

## Project Overview

A menu-driven C++ console application that detects plagiarism in academic
documents by implementing four classic string-matching algorithms:

| # | Algorithm   | Time Complexity     | Space |
|---|-------------|---------------------|-------|
| 1 | Naive       | O(n × m)            | O(1)  |
| 2 | KMP         | O(n + m)            | O(m)  |
| 3 | Rabin-Karp  | O(n+m) avg          | O(1)  |
| 4 | Boyer-Moore | O(n/m) best         | O(σ)  |

---

## Folder Structure

```
plagiarism_engine/
├── main.cpp                   ← Entry point, menu-driven UI
├── include/
│   ├── types.h                ← SearchResult, ComparisonRow structs
│   ├── algorithms.h           ← Algorithm declarations
│   └── utils.h                ← Helper function declarations
├── src/
│   ├── naive.cpp              ← Brute-force matcher
│   ├── kmp.cpp                ← Knuth-Morris-Pratt
│   ├── rabin_karp.cpp         ← Rolling-hash matcher
│   ├── boyer_moore.cpp        ← Bad-character heuristic
│   └── utils.cpp              ← File I/O, display, CSV, plagiarism %
├── data/
│   └── sample.txt             ← Test document
├── output/                    ← CSV results + PNG charts (auto-created)
├── visualize.py               ← Matplotlib charts (Python)
└── README.md
```

---

## Compile & Run (Windows — g++ / MSYS2 / VS Code Terminal)

```bash
# Compile
g++ main.cpp src/naive.cpp src/kmp.cpp src/rabin_karp.cpp \
    src/boyer_moore.cpp src/utils.cpp \
    -I include -std=c++17 -O2 -o plagiarism

# Run
./plagiarism          # MSYS2 / Git Bash
plagiarism.exe        # Windows CMD
```

### VS Code — tasks.json (Build Task)

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Build Plagiarism Engine",
      "type": "shell",
      "command": "g++",
      "args": [
        "main.cpp",
        "src/naive.cpp", "src/kmp.cpp",
        "src/rabin_karp.cpp", "src/boyer_moore.cpp",
        "src/utils.cpp",
        "-I", "include",
        "-std=c++17", "-O2",
        "-o", "plagiarism"
      ],
      "group": { "kind": "build", "isDefault": true }
    }
  ]
}
```

---

## Visualisation (Python)

```bash
pip install matplotlib numpy
python visualize.py
```

Generates 6 PNG charts in `output/`:
1. `fig1_execution_time_grouped.png`  — Grouped bar: time per pattern
2. `fig2_comparisons_grouped.png`     — Grouped bar: comparisons per pattern
3. `fig3_time_vs_pattern_length.png`  — Line chart: time vs pattern length
4. `fig4_radar.png`                   — Radar: overall algorithm quality
5. `fig5_avg_comparisons.png`         — Horizontal bar: average comparisons
6. `fig6_theoretical_complexity.png`  — Theoretical O-notation growth curves

---

## Menu Options

```
1. Search a pattern     – run all 4 algorithms, export CSV
2. Detect duplicates    – find repeated n-word phrases
3. Plagiarism %         – token-overlap score for keyword list
4. Benchmark            – run all 4 algorithms on 6 preset patterns
5. Load a document      – from file / stdin / built-in sample
0. Exit
```

---

## Sample Run

```
Pattern: "pattern matching"
─────────────────────────────────────────────────────────
Algorithm     Occurrences  Comparisons  Time(µs)  Complexity
─────────────────────────────────────────────────────────
Naive              9          1403        4.30    O(n*m)
KMP                9          1256        4.60    O(n+m)
Rabin-Karp         9          1398        7.22    O(n+m) avg
Boyer-Moore        9           312        2.30    O(n/m) best
```

---

## Algorithm Explanations

### 1 — Naive (Brute-Force)
Slides the pattern over every position and compares character-by-character.
No preprocessing. Simple but O(n×m) worst case.

### 2 — Knuth-Morris-Pratt (KMP)
Builds a *Longest Proper Prefix–Suffix* (LPS) array during preprocessing.
Uses it to skip re-comparisons after a mismatch. Guaranteed O(n+m).

### 3 — Rabin-Karp
Maintains a *rolling polynomial hash* of the current text window.
Compares hashes first (O(1)); confirms character-by-character only on a hit.
Degrades to O(n×m) if many hash collisions occur.

### 4 — Boyer-Moore (Bad-Character)
Compares right-to-left within the pattern. On a mismatch, shifts the pattern
by `j − last[text[i+j]]` positions, potentially skipping many characters.
Sub-linear best case: O(n/m).

---

## Complexity Summary

| Algorithm   | Pre-process | Search       | Space |
|-------------|-------------|--------------|-------|
| Naive       | —           | O(n×m)       | O(1)  |
| KMP         | O(m)        | O(n)         | O(m)  |
| Rabin-Karp  | O(m)        | O(n) avg     | O(1)  |
| Boyer-Moore | O(m + σ)    | O(n/m) best  | O(σ)  |

---

## Plagiarism % Calculation

1. Tokenise the document into words.
2. For each supplied keyword/phrase, mark all matching token indices.
3. `plagiarism_% = (matched_tokens / total_tokens) × 100`

Verdict thresholds:
- ≥ 50% → HIGH RISK
- 20–49% → MODERATE
- < 20% → LOW RISK

---

## STL Features Used

- `std::string`, `std::vector`, `std::map`, `std::set`
- `std::ifstream` / `std::ofstream` — file I/O
- `std::chrono::high_resolution_clock` — execution timing
- `std::istringstream` — tokenisation
- `std::setw`, `std::fixed`, `std::setprecision` — formatted output

---

## Author

Mini Project — M.Tech / B.E. (Computer Science & Engineering)
Topic: Design and Development of an Efficient Pattern Searching Engine
       for Academic Plagiarism Detection Using String Matching Algorithms
