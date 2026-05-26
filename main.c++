#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <limits>

#include "include/algorithms.h"
#include "include/utils.h"
#include "include/types.h"

// ── Forward declarations ─────────────────────────────────────
void printBanner();
void menuSearch(const std::string& text);
void menuDuplicate(const std::string& text);
void menuPlagiarism(const std::string& text);
void menuBenchmark(const std::string& text);
std::string loadText();
int  getChoice(int lo, int hi);

// ── main ─────────────────────────────────────────────────────
int main()
{
    printBanner();

    // ── Load document ──────────────────────────────────────
    std::string text = loadText();
    if (text.empty()) {
        std::cerr << "[ERROR] Empty document. Exiting.\n";
        return 1;
    }
    std::cout << "\n  Document loaded. Length: "
              << text.size() << " characters.\n";

    // ── Main menu ──────────────────────────────────────────
    bool running = true;
    while (running) {
        std::cout << "\n";
        std::cout << std::string(50, '=') << "\n";
        std::cout << "  MAIN MENU\n";
        std::cout << std::string(50, '-') << "\n";
        std::cout << "  1. Search a pattern (single keyword/phrase)\n";
        std::cout << "  2. Detect duplicate phrases\n";
        std::cout << "  3. Plagiarism percentage (multi-keyword)\n";
        std::cout << "  4. Benchmark all algorithms\n";
        std::cout << "  5. Load a different document\n";
        std::cout << "  0. Exit\n";
        std::cout << std::string(50, '=') << "\n";
        std::cout << "  Choice: ";

        int ch = getChoice(0, 5);

        switch (ch) {
        case 1: menuSearch(text);         break;
        case 2: menuDuplicate(text);      break;
        case 3: menuPlagiarism(text);     break;
        case 4: menuBenchmark(text);      break;
        case 5: text = loadText();        break;
        case 0: running = false;          break;
        }
    }

    std::cout << "\n  Thank you for using the Plagiarism Engine!\n\n";
    return 0;
}

// ── Banner ────────────────────────────────────────────────────
void printBanner()
{
    std::cout << "\n";
    std::cout << "  ╔══════════════════════════════════════════════════╗\n";
    std::cout << "  ║   PATTERN SEARCHING ENGINE FOR PLAGIARISM        ║\n";
    std::cout << "  ║   DETECTION  –  String Matching Algorithms       ║\n";
    std::cout << "  ║   Algorithms: Naive | KMP | Rabin-Karp | B-M     ║\n";
    std::cout << "  ╚══════════════════════════════════════════════════╝\n";
}

// ── Load document ────────────────────────────────────────────
std::string loadText()
{
    std::cout << "\n  Source:\n";
    std::cout << "    1. Load from file\n";
    std::cout << "    2. Enter text manually\n";
    std::cout << "    3. Use built-in sample text\n";
    std::cout << "  Choice: ";
    int ch = getChoice(1, 3);

    if (ch == 1) {
        std::cout << "  File path: ";
        std::string path;
        std::cin >> path;
        std::cin.ignore();
        return readFile(path);
    }
    if (ch == 2) {
        std::cout << "  Enter text (end with a line containing only '###'):\n";
        std::string line, all;
        std::cin.ignore();
        while (std::getline(std::cin, line) && line != "###")
            all += line + " ";
        return all;
    }
    // Built-in sample
    return
        "Plagiarism is the practice of taking someone else's work or ideas "
        "and passing them off as one's own. Plagiarism detection is an "
        "important task in academic institutions. Pattern matching algorithms "
        "are used to detect plagiarism efficiently. The Knuth-Morris-Pratt "
        "algorithm and the Boyer-Moore algorithm are both efficient pattern "
        "matching algorithms. The Rabin-Karp algorithm uses hashing for "
        "pattern matching. Naive pattern matching is the simplest algorithm. "
        "Pattern matching is a fundamental problem in computer science. "
        "Efficient pattern matching algorithms can process large documents. "
        "Academic integrity requires that students do not commit plagiarism. "
        "String matching algorithms form the backbone of plagiarism detection. "
        "The KMP algorithm builds a failure function for efficient matching. "
        "Boyer-Moore uses the bad-character heuristic to skip alignments. "
        "Rabin-Karp computes a rolling hash over a sliding window. "
        "Naive pattern matching compares every position in the text. "
        "Pattern matching and plagiarism detection are closely related topics. "
        "Students must ensure their work is original and free from plagiarism. "
        "Text analysis tools use pattern matching to detect copied content. "
        "Efficient algorithms reduce the time needed for plagiarism detection.";
}

// ── Menu 1: Single Pattern Search ────────────────────────────
void menuSearch(const std::string& text)
{
    std::cout << "\n  Enter pattern to search: ";
    std::string pattern;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::getline(std::cin, pattern);

    if (pattern.empty()) { std::cout << "  [Empty pattern – aborted]\n"; return; }

    std::cout << "  Case-sensitive? (y/n): ";
    char cs; std::cin >> cs;
    bool caseSens = (cs == 'y' || cs == 'Y');

    std::vector<SearchResult> results;

    results.push_back(naiveSearch    (text, pattern, caseSens));
    results.push_back(kmpSearch      (text, pattern, caseSens));
    results.push_back(rabinKarpSearch(text, pattern, caseSens));
    results.push_back(boyerMooreSearch(text, pattern, caseSens));

    for (const auto& r : results)
        printResult(r, pattern, text);

    printComparisonTable(results);
    exportCSV(results, pattern);
}

// ── Menu 2: Duplicate Phrase Detection ───────────────────────
void menuDuplicate(const std::string& text)
{
    std::cout << "  Window size (words per phrase, default 5): ";
    std::cin.ignore();
    std::string line;
    std::getline(std::cin, line);
    int ws = line.empty() ? 5 : std::stoi(line);

    auto dupes = findDuplicatePhrases(text, ws);

    std::cout << "\n  Duplicate " << ws << "-word phrases found: "
              << dupes.size() << "\n";
    std::cout << std::string(60, '-') << "\n";
    int shown = 0;
    for (const auto& d : dupes) {
        std::cout << "  [" << std::setw(3) << ++shown << "] " << d << "\n";
        if (shown == 50) {
            std::cout << "  ... (showing first 50)\n"; break;
        }
    }
}

// ── Menu 3: Plagiarism Percentage ────────────────────────────
void menuPlagiarism(const std::string& text)
{
    std::cout << "\n  Enter keywords/phrases (one per line).\n";
    std::cout << "  Type 'DONE' to finish:\n";

    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::vector<std::string> patterns;
    std::string line;
    while (std::getline(std::cin, line) && line != "DONE") {
        if (!line.empty()) patterns.push_back(line);
    }

    if (patterns.empty()) { std::cout << "  [No patterns – aborted]\n"; return; }

    double pct = plagiarismPercentage(text, patterns);

    std::cout << "\n";
    std::cout << std::string(50, '=') << "\n";
    std::cout << "  PLAGIARISM ANALYSIS RESULT\n";
    std::cout << std::string(50, '-') << "\n";
    std::cout << "  Patterns supplied : " << patterns.size() << "\n";
    std::cout << "  Matched word coverage: "
              << std::fixed << std::setprecision(2) << pct << " %\n";

    if      (pct >= 50) std::cout << "  Verdict: HIGH PLAGIARISM RISK\n";
    else if (pct >= 20) std::cout << "  Verdict: MODERATE RISK – review recommended\n";
    else                std::cout << "  Verdict: LOW RISK\n";
    std::cout << std::string(50, '=') << "\n";
}

// ── Menu 4: Benchmark with multiple patterns ─────────────────
void menuBenchmark(const std::string& text)
{
    // Benchmark patterns of various lengths
    std::vector<std::string> benchPatterns = {
        "the", "pattern", "plagiarism", "matching algorithms",
        "Knuth-Morris-Pratt algorithm", "pattern matching algorithms are"
    };

    std::cout << "\n  Running benchmark on " << benchPatterns.size()
              << " patterns...\n";

    for (const auto& pat : benchPatterns) {
        std::vector<SearchResult> results;
        results.push_back(naiveSearch    (text, pat, false));
        results.push_back(kmpSearch      (text, pat, false));
        results.push_back(rabinKarpSearch(text, pat, false));
        results.push_back(boyerMooreSearch(text, pat, false));
        printComparisonTable(results);
        std::cout << "  Pattern: \"" << pat << "\"\n";

        exportCSV(results, pat, "output/benchmark_" +
                  std::to_string(results[0].totalOccurrences) + ".csv");
    }
}

// ── Safe integer input ────────────────────────────────────────
int getChoice(int lo, int hi)
{
    int v;
    while (!(std::cin >> v) || v < lo || v > hi) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "  Invalid input. Enter " << lo << "-" << hi << ": ";
    }
    return v;
}
