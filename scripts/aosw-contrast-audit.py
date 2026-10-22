#!/usr/bin/env python3
"""AOS-W v0.9 *optional developer* visual text-contrast smoke.

Open a LOCAL, generated workflow HTML in Chromium; measure computed foreground
and composed background colors in real desktop/mobile and light/dark themes.
Require WCAG 2.2 AA >=4.5:1 on ordinary text (strict even for large labels)
and >=3:1 on meaningful SVG graph arrows and keyboard focus indicator.
Also detect hidden/near-white-on-white lane headings. Never make network calls.
This audits known solid-background components, not arbitrary images/gradients.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SELECTORS = [
    ".laneLabel",".audienceLaneTitle",".audience-lane-title",".audience-lane-heading",
    ".lane-title",".laneTitle",".laneHeader",".lane-heading",
    ".stepTitle",".stepSummary",".stepState",
    ".overview h2",".overview p",".phase strong",".phase span",
    ".metric",".subtitle",".banner",".panel h2",".section h3",
    ".next-action",".resource",".tag",".action-btn"
]

JS_AUDIT = r"""(selectors) => {
 function color(v){
   const m=String(v).match(/rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s\/]+([\d.]+))?/);
   if(!m)return null;
   return [Number(m[1]),Number(m[2]),Number(m[3]),m[4]===undefined?1:Number(m[4])];
 }
 const combine=(top,bottom)=>{
   const alpha=top[3]+bottom[3]*(1-top[3]);
   if(!alpha)return [0,0,0,0];
   return [0,1,2].map(i=>(top[i]*top[3]+bottom[i]*bottom[3]*(1-top[3]))/alpha).concat(alpha);
 };
 const light=c=>{
   const linear=x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4};
   return .2126*linear(c[0])+.7152*linear(c[1])+.0722*linear(c[2]);
 };
 const contrast=(a,b)=>{const x=light(a),y=light(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
 const bg=element=>{
   let result=[0,0,0,0];
   for(let n=element;n;n=n.parentElement){
     const part=color(getComputedStyle(n).backgroundColor);
     if(part)result=combine(result,part);
     if(result[3]>=.9999)break;
   }
   return combine(result,[255,255,255,1]);
 };
 const visible=e=>{
   for(let n=e;n;n=n.parentElement){
     const s=getComputedStyle(n);
     if(s.display==="none"||s.visibility==="hidden"||s.visibility==="collapse")return false;
   }
   return e.getClientRects().length>0 && !!e.textContent.trim();
 };
 const failures=[],items=[];
 for(const selector of selectors){
   for(const el of document.querySelectorAll(selector)){
     if(!visible(el))continue;
     const style=getComputedStyle(el);
     const fg=color(style.color),background=bg(el);
     if(!fg){failures.push({selector,issue:"unparseable text color",raw:style.color});continue}
     const painted=combine(fg,background);
     const ratio=contrast(painted,background);
     const item={selector,text:el.textContent.trim().slice(0,85),ratio:Number(ratio.toFixed(2)),
       foreground:style.color,background:background.map(v=>Math.round(v)).join(",")};
     items.push(item);
     if(ratio<4.5)failures.push({...item,issue:"text contrast <4.5:1"});
   }
 }
 const labels=items.filter(x=>selectors.slice(0,8).includes(x.selector));
 const edges=Array.from(document.querySelectorAll("#links path[marker-end]"));
 if(edges.length){
   const edgeColor=color(getComputedStyle(document.documentElement).getPropertyValue("--aw-edge").trim());
   const canvasBg=bg(document.getElementById("canvas"));
   const value=edgeColor?contrast(edgeColor,canvasBg):0;
   if(value<3)failures.push({selector:"svg dependency edge",ratio:Number(value.toFixed(2)),issue:"non-text contrast <3:1"});
 }
 const step=document.querySelector(".step:not([hidden])");
 if(step){
   step.focus();
   const outline=color(getComputedStyle(step).outlineColor),back=bg(step);
   const ratio=outline?contrast(outline,back):0;
   if(ratio<3)failures.push({selector:".step:focus-visible",ratio:Number(ratio.toFixed(2)),issue:"focus indicator contrast <3:1"});
 }
 return {checked:items.length,labels:labels.length,edges:edges.length,
  minRatio:items.length?Math.min(...items.map(x=>x.ratio)):0,failures,items};
}"""

def audit(html:Path,output:Path,require_lanes=False):
    if not html.is_file():raise ValueError("Missing HTML file: "+str(html))
    output.mkdir(parents=True,exist_ok=True)
    reports=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for scheme in ("light","dark"):
            for size,width,height in (("desktop",1440,920),("mobile",390,820)):
                page=browser.new_page(viewport={"width":width,"height":height},color_scheme=scheme)
                outbound=[]
                page.on("request",lambda req: outbound.append(req.url) if not req.url.startswith("file://") else None)
                page.goto(html.resolve().as_uri(),wait_until="domcontentloaded")
                if page.locator("#toggle-graph").count() and page.locator("#canvas").is_hidden():
                    page.locator("#toggle-graph").click()
                result=page.evaluate(JS_AUDIT,SELECTORS)
                result.update({"mode":scheme,"size":size,"outboundRequests":outbound})
                if require_lanes and result["labels"]<6:
                    result["failures"].append({"issue":"expected six visible audience lane headings", "found":result["labels"]})
                if outbound:result["failures"].append({"issue":"network requests are not allowed","urls":outbound})
                page.screenshot(path=str(output/(scheme+"-"+size+".png")),full_page=True)
                reports.append(result)
                page.close()
        browser.close()
    summary={"status":"PASS" if all(not x["failures"] for x in reports) else "FAIL",
             "views":len(reports),"textChecks":sum(x["checked"] for x in reports),
             "minContrast":min((x["minRatio"] for x in reports),default=0),
             "failures":[{"view":r["mode"]+"-"+r["size"],"details":r["failures"]} for r in reports if r["failures"]],
             "screenshots":[x["mode"]+"-"+x["size"]+".png" for x in reports],
             "scope":"Rendered solid-color text, key arrows/focus in Chromium; not full WCAG certification."}
    (output/"contrast-report.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    return summary

def main():
    parser=argparse.ArgumentParser(description="Read-only rendered WCAG AA contrast regression audit")
    parser.add_argument("--html",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--six-lanes",action="store_true")
    args=parser.parse_args()
    try:
        report=audit(args.html,args.out,require_lanes=args.six_lanes)
        print(json.dumps(report,indent=2))
        raise SystemExit(0 if report["status"]=="PASS" else 1)
    except (OSError,ValueError) as e:
        print("A11Y AUDIT ERROR: "+str(e),file=sys.stderr);raise SystemExit(2)
if __name__=="__main__":main()
