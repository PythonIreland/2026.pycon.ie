#!/usr/bin/env python3
"""
CSP consistency checker.

Verifies that every external domain referenced in Hugo templates is covered
by the appropriate Content-Security-Policy directive in static/_headers.

Also checks known dynamic loaders (e.g. Typekit injecting its own CSS)
declared in csp-dynamic-loaders.yml.

Usage:
    python scripts/check-csp.py
    python scripts/check-csp.py --verbose
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

ROOT = Path(__file__).resolve().parent.parent
HEADERS_FILE = ROOT / "static" / "_headers"
LOADERS_FILE = ROOT / "csp-dynamic-loaders.yml"
TEMPLATE_GLOBS = ["layouts/**/*.html"]


def parse_csp(path):
    text = path.read_text()
    m = re.search(r"Content-Security-Policy:\s*(.+)", text)
    if not m:
        sys.exit("ERROR: No Content-Security-Policy found in static/_headers")
    directives = {}
    for part in m.group(1).split(";"):
        tokens = part.strip().split()
        if tokens:
            directives[tokens[0].lower()] = set(tokens[1:])
    return directives


def domain_allowed(domain, directive, directives):
    """Check if domain satisfies directive or falls back to default-src."""
    for src in [directive, "default-src"]:
        for rule in directives.get(src, set()):
            if rule == domain:
                return True
            # Wildcard subdomain: *.example.com
            if rule.startswith("*.") and domain.endswith(rule[1:]):
                return True
            # Scheme wildcard: "https:" allows any https:// domain
            if rule == "https:":
                return True
    return False


def classify_line(line):
    """Return list of (domain, directive) for external URLs found on a line."""
    results = []
    for url in re.findall(r'https://[^\s"\'<>]+', line):
        domain = urlparse(url).netloc
        if not domain:
            continue

        if re.search(r"<script\b", line) and "src=" in line:
            results.append((domain, "script-src"))
            continue

        if re.search(r"<link\b", line):
            rel_m = re.search(r'\brel=["\']([^"\']+)["\']', line)
            as_m = re.search(r'\bas=["\'](\w+)["\']', line)
            rel = rel_m.group(1) if rel_m else ""
            as_val = as_m.group(1) if as_m else ""

            if "stylesheet" in rel:
                results.append((domain, "style-src"))
            elif "preload" in rel:
                directive_map = {
                    "style": "style-src",
                    "font": "font-src",
                    "script": "script-src",
                    "image": "img-src",
                }
                results.append((domain, directive_map.get(as_val, "default-src")))
            elif "preconnect" in rel or "dns-prefetch" in rel:
                results.append((domain, "connect-src"))
            continue

        if re.search(r"<img\b", line) and "src=" in line:
            results.append((domain, "img-src"))

    return results


def load_dynamic_loaders():
    if not LOADERS_FILE.exists():
        return []
    if not HAS_YAML:
        print("WARNING: pyyaml not installed — dynamic loader checks skipped.")
        return []
    with LOADERS_FILE.open() as f:
        return yaml.safe_load(f) or []


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    directives = parse_csp(HEADERS_FILE)
    loaders = load_dynamic_loaders()

    errors = []
    checked = []

    # Scan template files
    for glob_pattern in TEMPLATE_GLOBS:
        for path in sorted(ROOT.glob(glob_pattern)):
            for lineno, line in enumerate(path.read_text().splitlines(), 1):
                for domain, directive in classify_line(line):
                    ok = domain_allowed(domain, directive, directives)
                    checked.append((domain, directive, path.relative_to(ROOT), lineno, ok))
                    if not ok:
                        errors.append((domain, directive, path.relative_to(ROOT), lineno))

    # Check dynamic loaders
    for loader in loaders:
        trigger = loader["trigger"]
        if domain_allowed(trigger["domain"], trigger["directive"], directives):
            for also in loader.get("also-loads", []):
                ok = domain_allowed(also["domain"], also["directive"], directives)
                label = f"[dynamic: {loader['name']}]"
                checked.append((also["domain"], also["directive"], label, 0, ok))
                if not ok:
                    errors.append((also["domain"], also["directive"], label, 0))

    # Verbose output
    if verbose:
        print(f"\nChecked {len(checked)} domain/directive pair(s):\n")
        for domain, directive, path, lineno, ok in checked:
            mark = "✅" if ok else "❌"
            loc = f"{path}:{lineno}" if lineno else str(path)
            print(f"  {mark} {domain:<42} {directive:<15} {loc}")
        print()

    # Final result
    if errors:
        print(f"❌ CSP check FAILED — {len(errors)} violation(s):\n")
        for domain, directive, path, lineno in errors:
            loc = f"{path}:{lineno}" if lineno else str(path)
            print(f"  • {domain!r} doit être dans {directive!r}")
            print(f"    source : {loc}")
            print(f"    fix    : ajouter {domain!r} à {directive} dans static/_headers\n")
        sys.exit(1)
    else:
        print(f"✅ CSP check passed — {len(checked)} domain/directive pair(s) verified.")


if __name__ == "__main__":
    main()
