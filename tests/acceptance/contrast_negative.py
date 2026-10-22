#!/usr/bin/env python3
"""Negative regression: intentional white-on-white lane titles MUST fail audit.

Runs only on a PUBLIC fictional fixture, never real customer workflows.
"""
from __future__ import annotations
import argparse,importlib.util,json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("contrast_audit",ROOT/"scripts/aosw-contrast-audit.py")
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--html",required=True,type=Path)
    args=parser.parse_args()
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":1440,"height":920},color_scheme="light")
        page.goto(args.html.resolve().as_uri(),wait_until="domcontentloaded")
        # Simulate the user-observed mistake (e.g. host title token inherited white).
        page.add_style_tag(content=".laneLabel{color:#ffffff!important;background:#ffffff!important;}")
        result=page.evaluate(audit.JS_AUDIT,audit.SELECTORS)
        contrast_failures=[x for x in result["failures"] if x.get("selector")==".laneLabel"
                           and x.get("ratio",100)<1.1]
        assert result["labels"]>=6, result
        assert len(contrast_failures)>=6, result
        assert result["minRatio"]<=1.01, result
        print(json.dumps({"status":"EXPECTED_FAILURE_DETECTED",
            "injected":"white lane titles on white background",
            "failedLaneHeadings":len(contrast_failures)}))
        browser.close()
if __name__=="__main__":main()
