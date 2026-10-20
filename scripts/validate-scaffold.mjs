#!/usr/bin/env node
/**
 * OPTIONAL developer check. No packages required, but Node itself is NOT an AOS-W dependency.
 * Usage: node scripts/validate-scaffold.mjs [path/to/aos-w]
 * Structural read-only checks; not a graph engine, ACL validator or YAML schema validator.
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const root = path.resolve(process.argv[2] ?? path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "scaffold", "aos-w"));
const required = [
  "README.md", "PROTOCOL.md", "VERSION.json", "templates/README.md", "spec/README.md",
  "references/START-A-RUN.md", "references/UPGRADE-AND-PORTABILITY.md",
  "templates/research-starter/template.yaml", "templates/research-starter/skills/evidence-handling/SKILL.md",
  "templates/periodic-review-example/template.yaml",
  "agent-files/README.md", "agent-files/config/settings.json", "agent-files/config/capabilities.json",
  "agent-files/config/sync.json", "agent-files/custom-templates/README.md", "agent-files/instances/README.md",
  "agent-files/indexes/README.md", "agent-files/cache/README.md", "agent-files/coordination/README.md"
];
const schemas = ["sync-config","sync-state","approval","attempt","checkpoint","claim","common","compound-template","custom-template","event",
 "handoff","instance","retry-policy","review","run","state","template-lock","template"].map(x => x + ".schema.json");
let checks = 0;
function check(ok, message) { checks++; if (!ok) throw new Error(message); }
const read = relative => fs.readFileSync(path.join(root, relative), "utf8");
for(const p of required) check(fs.existsSync(path.join(root,p)), "Missing scaffold path: " + p);
const version = JSON.parse(read("VERSION.json"));
check(version.aosw_version === "0.5.0", "Unexpected framework version");
check(version.mandatory_git === false && version.mandatory_programming_runtime === false, "Required runtime unexpectedly configured");
const sync=JSON.parse(read("agent-files/config/sync.json"));
check(sync.enabled === false && sync.status === "not_configured", "Bundled Git mirror must default off");
const configs=["agent-files/config/settings.json","agent-files/config/capabilities.json"];
for(const x of configs)check(JSON.parse(read(x)).schema_version==="1.0.0","Invalid config JSON: "+x);

const schemaDir=path.join(root,"spec","schemas");
const by={};
for(const n of schemas){
 const p=path.join(schemaDir,n);
 check(fs.existsSync(p),"Missing JSON Schema: "+n);
 by[n]=JSON.parse(fs.readFileSync(p,"utf8"));
 check(by[n].$schema === "https://json-schema.org/draft/2020-12/schema","Unsupported JSON Schema root: "+n);
}
function pointer(rootObj,fragment){
 let value=rootObj;
 for(const x of fragment.split("/").slice(1)){
  const field=x.replace(/~1/g,"/").replace(/~0/g,"~");
  value=value?.[field];
 }
 return value;
}
let refs=0;
function walk(from,v){
 if(!v||typeof v!=="object")return;
 if(typeof v.$ref==="string"){
  refs++;
  const [rel,hash] = v.$ref.split("#");
  const other=rel||from;
  check(Object.hasOwn(by,other) && (hash===undefined||pointer(by[other],hash)!==undefined),
    "Broken JSON Schema ref "+from+" -> "+v.$ref);
 }
 for(const child of Object.values(v))walk(from,child);
}
for(const [name,doc] of Object.entries(by))walk(name,doc);

for(const n of ["research-starter","periodic-review-example"]){
 const t=read("templates/"+n+"/template.yaml");
 check(/^schema_version: "1\.0\.0"/m.test(t) && t.includes("template_id: "+n) && t.includes("graph:"),
  "Bundled YAML lacks required structural markers: "+n);
}
const base="agent-files/instances/demo-local-research/";
const records=["instance.json","template-lock.json","graph-revisions/g0001.yaml","runs/run-001/run.json",
 "runs/run-001/events.jsonl","runs/run-001/state.json","runs/run-001/handoff.json",
 "runs/run-001/handoff.md","runs/run-001/checkpoints/checkpoint-0001.json"];
for(const p of records)check(fs.existsSync(path.join(root,base,p)),"Practice run record missing: "+p);
const inst=JSON.parse(read(base+"instance.json"));
const lock=JSON.parse(read(base+"template-lock.json"));
const run=JSON.parse(read(base+"runs/run-001/run.json"));
const state=JSON.parse(read(base+"runs/run-001/state.json"));
const cp=JSON.parse(read(base+"runs/run-001/checkpoints/checkpoint-0001.json"));
const handoff=JSON.parse(read(base+"runs/run-001/handoff.json"));
const events=read(base+"runs/run-001/events.jsonl").trimEnd().split("\n").map(x=>JSON.parse(x));
check(inst.instance_id==="demo-local-research"&&inst.current_graph_revision==="g0001","Practice instance pointer wrong");
check(lock.template_id==="research-starter"&&lock.version==="0.1.0","Practice template pin missing");
const master=read("templates/research-starter/template.yaml");
const snapshot=read(base+"template-snapshots/master-v0-1-0/template.yaml");
check(snapshot===read(base+"graph-revisions/g0001.yaml"),"Pinned practice template mismatch");
check(master!==snapshot && master.includes('version: 0.2.0'),"Updated master should not rewrite pinned 0.1.0 run");
const blobHash=crypto.createHash("sha1").update("blob "+Buffer.byteLength(snapshot)+"\0").update(snapshot).digest("hex");
check(lock.content_digest==="git-blob-sha1:"+blobHash,"Pinned template digest differs from actual blob");
check(events.length===2 && events.every((e,i)=>e.seq===i+1 && e.run_id==="run-001"),"Practice run event order invalid");
check(run.trigger_kind==="manual" && run.mode==="standalone_single_writer","Practice mode unexpectedly automated");
check(state.last_event_seq===2 && cp.event_seq===2 && handoff.last_event_seq===2,"Event anchor disagreement");
check(state.run_status==="CREATED" && state.tasks["define-scope"]?.status==="READY" &&
 state.eligible_tasks.includes("define-scope"),"Practice next task not ready");
check(Object.values(state.tasks).every(x=>x.attempts===0) && events.every(x=>x.type!=="task_completed"),
 "Practice run must not claim any executed tasks");
check(handoff.ready.includes("define-scope") && !handoff.pending_approvals?.length, "Handoff disagrees with safe starter");
console.log("PASS: "+checks+" read-only structural checks, "+schemas.length+" schemas, "+refs+" local $ref links.");
console.log("PASS: protected scaffold and user workspace, pinned practice example, no fake completed work.");
console.log("NOT TESTED: full YAML/JSON Schema validation, graph engine, provider APIs, distributed locks or scheduler.");
