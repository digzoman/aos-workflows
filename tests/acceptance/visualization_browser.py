#!/usr/bin/env python3
"""Browser acceptance of generated AOS-W read-only workflow visualization.

Run against the sanitized example only. Never opens live Meta/CRM or transmits
workflow content. Page stays local file://; any outbound request fails the test.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--html",required=True,type=Path)
    ap.add_argument("--compound",type=Path,help="offline generated compound template preview")
    ap.add_argument("--human-six",type=Path,help="v0.9 illustrative six-audience workflow")
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    assert args.html.exists()
    args.out.mkdir(parents=True,exist_ok=True)
    results=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":1440,"height":920},device_scale_factor=1)
        errors=[]
        page.on("pageerror",lambda error: errors.append(str(error)))
        requests=[]
        page.on("request",lambda req: requests.append(req.url) if not req.url.startswith("file://") else None)
        page.goto(args.html.resolve().as_uri(),wait_until="domcontentloaded")
        page.locator(".step").first.wait_for()
        assert page.locator(".step").count()==11
        results.append("11 nodes rendered")
        assert page.locator("#links path[marker-end]").count()==sum(
            len(n["needs"]) for n in json.loads(
                (args.html.parent/"snapshot.json").read_text())["nodes"])
        results.append("all expected arrows rendered")
        page.locator(".step[data-id='creative']").click()
        details=page.locator("#details")
        assert "Image creative" in details.inner_text()
        assert "1080x1350" in details.inner_text()
        assert "image-review" in details.inner_text()
        results.append("real click shows saved prompt and QC gate")
        page.locator("#search").fill("human launch")
        assert page.locator(".step:not(.dimmed)").count()==1
        assert page.locator(".step.dimmed").count()==10
        results.append("search filters visually without removing dependency graph")
        page.locator(".step[data-id='launch']").click()
        assert "Require a new explicit owner authorization" in details.inner_text()
        assert "WAIT_APPROVAL" in details.inner_text()
        results.append("pending launch authorization visibly remains blocked")
        page.screenshot(path=str(args.out/"desktop.png"),full_page=True)
        page.set_viewport_size({"width":390,"height":820})
        page.locator("#search").fill("")
        page.locator(".step[data-id='agency-research']").click()
        assert "Research experienced advertisers" in details.inner_text()
        # The detail pane stacks below the graph at <=860 CSS breakpoint.
        positions=page.evaluate("""() => ({
          workspace: document.getElementById('workspace').getBoundingClientRect().bottom,
          panel: document.getElementById('details').getBoundingClientRect().top,
          detailWidth: document.getElementById('details').getBoundingClientRect().width
        })""")
        assert positions["panel"]>=positions["workspace"]-2, positions
        assert positions["detailWidth"]<=391, positions
        page.screenshot(path=str(args.out/"mobile.png"),full_page=True)
        results.append("mobile layout remains navigable, details stack beneath graph")
        # Real keyboard activation of native button.
        page.locator(".step[data-id='agency-research']").focus()
        page.keyboard.press("Enter")
        assert "Agency research" in details.locator("h2").inner_text()
        results.append("keyboard activation")
        assert not errors,errors
        assert not requests,requests
        results.append("no browser exceptions or outgoing network requests")
        if args.compound:
            page.goto(args.compound.resolve().as_uri(),wait_until="domcontentloaded")
            page.locator(".step").first.wait_for()
            assert page.locator(".step").count()>=20
            page.locator("#toggle-graph").click()
            snapshot=json.loads((args.compound.parent/"snapshot.json").read_text())
            verified=[n for n in snapshot["nodes"] if n.get("child_resolution")=="PINNED_LOCAL_MODULE_VERIFIED"]
            assert verified,"No pinned child modules found"
            step=verified[0]
            page.locator(".step[data-id='"+step["id"]+"']").click()
            assert "verified child workflow steps" in page.locator("#details").inner_text().casefold()
            page.locator("#details details summary").first.click()
            assert step["child_steps"][0]["prompt"] in page.locator("#details").inner_text()
            page.screenshot(path=str(args.out/"compound-drilldown.png"),full_page=True)
            results.append("full pinned child module prompts revealed by nested browser drilldown")
        if args.human_six:
            page.goto(args.human_six.resolve().as_uri(),wait_until="domcontentloaded")
            page.locator(".step").first.wait_for()
            assert page.locator(".step").count()==56
            assert page.locator("#overview").is_visible()
            assert "6 reviews ready" in page.locator("#overview").inner_text().lower()
            assert "Stage 1" not in page.locator(".workspace").inner_text()
            assert page.locator("#canvas").is_hidden()
            page.locator("#toggle-graph").click()
            assert page.locator("#canvas").is_visible()
            node=page.locator(".step[data-id='hvac-installation-owners--qc-research']")
            assert "Review HVAC business owners research" in node.inner_text()
            assert "--qc-research" not in node.inner_text()
            node.click()
            detail=page.locator("#details")
            assert "What happens next" in detail.inner_text()
            assert "Meta Ad Library" in detail.inner_text()
            assert "Do not stop or invent a human gate" in detail.inner_text()
            assert "Full instructions and technical details" in detail.inner_text()
            page.screenshot(path=str(args.out/"v09-six-audience-overview.png"),full_page=True)
            results.append("v0.9 56-node human-first view, six ready reviews, hidden raw IDs, source access and no fake gate")
        browser.close()
    (args.out/"results.json").write_text(json.dumps({"status":"PASS","checks":results,"count":len(results)},indent=2)+"\n")
    print(json.dumps({"status":"PASS","checks":len(results),"screenshots":["desktop.png","mobile.png"]}))
if __name__=="__main__":
    main()
