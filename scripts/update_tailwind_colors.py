#!/usr/bin/env python3
"""
FXJ Suits — Tailwind Class Color Replacement
Replaces all residual slate/blue/navy Tailwind classes with FXJ gold palette equivalents
"""
import os
import re

BASE = "/home/ubuntu/fxj-suits/src"

# Tailwind class replacements: old pattern → new class
# Order matters — more specific first
REPLACEMENTS = [
    # ── Backgrounds ──────────────────────────────────────────────
    (r'bg-slate-900(/\d+)?',     lambda m: f'bg-[#403301]{m.group(1) or ""}'),
    (r'bg-slate-800(/\d+)?',     lambda m: f'bg-[#403301]{m.group(1) or ""}'),
    (r'bg-slate-700(/\d+)?',     lambda m: f'bg-[#856A00]{m.group(1) or ""}'),
    (r'bg-slate-600(/\d+)?',     lambda m: f'bg-[#856A00]{m.group(1) or ""}'),
    (r'bg-slate-500(/\d+)?',     lambda m: f'bg-[#C2B067]{m.group(1) or ""}'),
    (r'bg-slate-400(/\d+)?',     lambda m: f'bg-[#C2B067]{m.group(1) or ""}'),
    (r'bg-slate-300(/\d+)?',     lambda m: f'bg-[#E8D98A]{m.group(1) or ""}'),
    (r'bg-slate-200(/\d+)?',     lambda m: f'bg-[#FDF6DC]{m.group(1) or ""}'),
    (r'bg-slate-100(/\d+)?',     lambda m: f'bg-[#FFF9E6]{m.group(1) or ""}'),
    (r'bg-slate-50(/\d+)?',      lambda m: f'bg-[#FFFDF0]{m.group(1) or ""}'),
    (r'bg-blue-900(/\d+)?',      lambda m: f'bg-[#403301]{m.group(1) or ""}'),
    (r'bg-blue-800(/\d+)?',      lambda m: f'bg-[#403301]{m.group(1) or ""}'),
    (r'bg-blue-700(/\d+)?',      lambda m: f'bg-[#856A00]{m.group(1) or ""}'),
    (r'bg-blue-600(/\d+)?',      lambda m: f'bg-[#856A00]{m.group(1) or ""}'),
    (r'bg-blue-500(/\d+)?',      lambda m: f'bg-[#EFBF04]{m.group(1) or ""}'),
    (r'bg-blue-100(/\d+)?',      lambda m: f'bg-[#FDF6DC]{m.group(1) or ""}'),
    (r'bg-blue-50(/\d+)?',       lambda m: f'bg-[#FFF9E6]{m.group(1) or ""}'),

    # ── Text colors ───────────────────────────────────────────────
    (r'text-slate-900',          'text-[#403301]'),
    (r'text-slate-800',          'text-[#403301]'),
    (r'text-slate-700',          'text-[#856A00]'),
    (r'text-slate-600',          'text-[#856A00]'),
    (r'text-slate-500',          'text-[#C2B067]'),
    (r'text-slate-400',          'text-[#C2B067]'),
    (r'text-slate-300',          'text-[#C2B067]'),
    (r'text-blue-700',           'text-[#856A00]'),
    (r'text-blue-600',           'text-[#856A00]'),
    (r'text-blue-500',           'text-[#EFBF04]'),

    # ── Borders ───────────────────────────────────────────────────
    (r'border-slate-900',        'border-[#403301]'),
    (r'border-slate-800',        'border-[#403301]'),
    (r'border-slate-700',        'border-[#856A00]'),
    (r'border-slate-600',        'border-[#856A00]'),
    (r'border-slate-500',        'border-[#C2B067]'),
    (r'border-slate-400',        'border-[#C2B067]'),
    (r'border-slate-300',        'border-[#E8D98A]'),
    (r'border-slate-200',        'border-[#E8D98A]'),
    (r'border-slate-100',        'border-[#FDF6DC]'),
    (r'border-blue-900',         'border-[#403301]'),
    (r'border-blue-700',         'border-[#856A00]'),
    (r'border-blue-500',         'border-[#EFBF04]'),

    # ── Hover states ──────────────────────────────────────────────
    (r'hover:bg-slate-900',      'hover:bg-[#403301]'),
    (r'hover:bg-slate-800',      'hover:bg-[#403301]'),
    (r'hover:bg-slate-700',      'hover:bg-[#856A00]'),
    (r'hover:bg-slate-100',      'hover:bg-[#FDF6DC]'),
    (r'hover:bg-slate-50',       'hover:bg-[#FFF9E6]'),
    (r'hover:bg-blue-900',       'hover:bg-[#403301]'),
    (r'hover:bg-blue-800',       'hover:bg-[#403301]'),
    (r'hover:bg-blue-700',       'hover:bg-[#856A00]'),
    (r'hover:text-blue-700',     'hover:text-[#856A00]'),
    (r'hover:text-blue-600',     'hover:text-[#856A00]'),
    (r'hover:text-slate-900',    'hover:text-[#403301]'),
    (r'hover:border-blue-500',   'hover:border-[#EFBF04]'),

    # ── Focus states ──────────────────────────────────────────────
    (r'focus:border-slate-400',  'focus:border-[#EFBF04]'),
    (r'focus:ring-slate-200',    'focus:ring-[#EFBF04]/20'),
    (r'focus:ring-blue-500',     'focus:ring-[#EFBF04]'),
    (r'focus:border-blue-500',   'focus:border-[#EFBF04]'),

    # ── Gradients ─────────────────────────────────────────────────
    (r'from-slate-900',          'from-[#403301]'),
    (r'from-slate-800',          'from-[#403301]'),
    (r'from-blue-900',           'from-[#403301]'),
    (r'from-blue-800',           'from-[#403301]'),
    (r'to-slate-900',            'to-[#403301]'),
    (r'to-blue-900',             'to-[#403301]'),
    (r'to-blue-800',             'to-[#856A00]'),
    (r'via-slate-800',           'via-[#856A00]'),

    # ── Shadow colors ─────────────────────────────────────────────
    (r'shadow-slate-900/\d+',    'shadow-[#403301]/20'),
    (r'shadow-blue-900/\d+',     'shadow-[#403301]/20'),

    # ── Decoration ────────────────────────────────────────────────
    (r'decoration-slate-300',    'decoration-[#C2B067]'),
    (r'decoration-blue-300',     'decoration-[#C2B067]'),

    # ── Ring ──────────────────────────────────────────────────────
    (r'ring-slate-200',          'ring-[#E8D98A]'),
    (r'ring-blue-500',           'ring-[#EFBF04]'),
]

EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".css"}

def process_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return False

    original = content
    for pattern, replacement in REPLACEMENTS:
        if callable(replacement):
            content = re.sub(pattern, replacement, content)
        else:
            content = re.sub(pattern, replacement, content)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    skip_dirs = {".git", "node_modules", "dist"}
    updated = 0
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in EXTENSIONS:
                fpath = os.path.join(root, fname)
                if process_file(fpath):
                    print(f"  Updated: {fpath.replace(BASE, '')}")
                    updated += 1
    print(f"\nTotal files updated: {updated}")

if __name__ == "__main__":
    print("FXJ Suits — Tailwind Color Update\n")
    main()
    print("\nDone!")
