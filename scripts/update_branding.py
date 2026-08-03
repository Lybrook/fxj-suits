#!/usr/bin/env python3
"""
FXJ Suits Branding Update Script
Replaces all old NomosLink/navy color references with FXJ Suits gold palette
"""
import os
import re

BASE = "/home/ubuntu/fxj-suits"

# ── Color mapping: old → new ──────────────────────────────────────────────────
COLOR_MAP = {
    "#0B1F3A": "#403301",   # navy dark  → FXJ dark brown
    "#123C69": "#856A00",   # navy mid   → FXJ mid gold
    "#38bdf8": "#EFBF04",   # sky blue   → FXJ gold
    "#1e293b": "#403301",   # slate dark → FXJ dark
    "#334155": "#856A00",   # slate mid  → FXJ mid
    "#cbd5e1": "#C2B067",   # slate light→ FXJ muted
    "#0b1f3a": "#403301",   # lowercase variant
    "#123c69": "#856A00",
    # Tailwind class replacements (inline)
    "bg-\\[#0B1F3A\\]":   "bg-[#403301]",
    "bg-\\[#123C69\\]":   "bg-[#856A00]",
    "text-\\[#0B1F3A\\]": "text-[#403301]",
    "text-\\[#38bdf8\\]": "text-[#EFBF04]",
    "border-\\[#0B1F3A\\]": "border-[#403301]",
    "from-\\[#0B1F3A\\]": "from-[#403301]",
    "to-blue-900":        "to-[#856A00]",
    "hover:bg-blue-900":  "hover:bg-[#856A00]",
    "hover:text-blue-700":"hover:text-[#856A00]",
    "bg-blue-900":        "bg-[#856A00]",
    "text-blue-700":      "text-[#856A00]",
}

# ── Name/brand mapping ────────────────────────────────────────────────────────
NAME_MAP = {
    "NomosLink Legal Management": "FXJ Suits | Law Firm Management",
    "NomosLink":                  "FXJ Suits",
    "nomoslink":                  "fxj-suits",
    "nomoslink-auth-key":         "fxj-suits-auth-key",
    "Buwembo &amp; Co. Advocates":"FXJ Suits Law Firm",
    "Buwembo & Co. Advocates":    "FXJ Suits Law Firm",
    "Buwembo &amp; Company Advocates": "FXJ Suits Law Firm",
    "Buwembo & Company Advocates":"FXJ Suits Law Firm",
    "Buwembo & Co. Advocates":    "FXJ Suits Law Firm",
    "transaction-app":            "fxj-suits",
    "BCA Transaction & Litigation Management System": "FXJ Suits — Law Firm Management System",
    "NomosLink_Report":           "FXJSuits_Report",
    "NomosLink app":              "FXJ Suits app",
    "NomosLink account":          "FXJ Suits account",
    "NomosLink Offline":          "FXJ Suits Offline",
    "Loading NomosLink":          "Loading FXJ Suits",
    "Buwembo & Company Advocates • Invoice Management": "FXJ Suits • Invoice Management",
}

EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".css", ".html", ".json", ".md"}

def process_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return

    original = content

    # Apply color replacements (case-sensitive hex)
    for old, new in COLOR_MAP.items():
        if old.startswith("bg-\\[") or old.startswith("text-\\[") or old.startswith("border-\\[") or old.startswith("from-\\[") or old.startswith("hover:") or old.startswith("to-") or old.startswith("bg-blue"):
            # These are regex patterns
            content = re.sub(old.replace("\\[", r"\[").replace("\\]", r"\]"), new, content)
        else:
            content = content.replace(old, new)

    # Apply name replacements
    for old, new in NAME_MAP.items():
        content = content.replace(old, new)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Updated: {path.replace(BASE, '')}")

def walk_and_update():
    skip_dirs = {".git", "node_modules", "dist", "scratch", "scripts"}
    updated = 0
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in EXTENSIONS:
                fpath = os.path.join(root, fname)
                before = open(fpath, "rb").read()
                process_file(fpath)
                after = open(fpath, "rb").read()
                if before != after:
                    updated += 1
    print(f"\nTotal files updated: {updated}")

if __name__ == "__main__":
    print("FXJ Suits Branding Update — Starting...\n")
    walk_and_update()
    print("\nDone!")
