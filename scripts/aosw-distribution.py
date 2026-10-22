#!/usr/bin/env python3
"""OPTIONAL maintainer-only AOS-W ZIP builder & installer. Python stdlib only.
Downloaded aos-w itself NEVER needs Python, Git, MCP, or a scheduler.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, stat, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath

PROTECTED = ('AGENTS.md', 'README.md', 'PROTOCOL.md', 'VERSION.json', 'spec/', 'references/', 'templates/')
SEED = ('README.md', 'config/settings.json', 'config/capabilities.json',
        'config/sync.json', 'config/sync-state.json', 'custom-templates/README.md',
        'instances/README.md', 'indexes/README.md', 'cache/README.md',
        'coordination/README.md', 'visualizations/README.md')
USER_DIRS = ('config', 'custom-templates', 'instances', 'indexes', 'cache', 'coordination', 'visualizations')
MAX_FILE = 8_000_000
MAX_TOTAL = 60_000_000
MAX_FILES = 600
MAX_ZIP_BYTES = 30_000_000
EPOCH = (2020, 1, 1, 0, 0, 0)
MANIFEST = 'DISTRIBUTION-MANIFEST.json'
class DistributionError(ValueError): pass

def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(o): return json.dumps(o, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
def jsonpretty(o): return (json.dumps(o, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()

def safe_pure(name):
    if not isinstance(name, str) or '\\' in name or not name.startswith('aos-w/'):
        raise DistributionError('Unsafe ZIP member prefix')
    # Explicitly reject path traversal, absolute/empty/case-colliding components
    p = PurePosixPath(name)
    if any(c in ('', '.', '..') for c in name.split('/')) or p.is_absolute() or '\x00' in name:
        raise DistributionError('Unsafe ZIP member path')
    return p

def permitted(rel):
    """Exact public framework shapes and a small, clean agent-files seed allowlist.
    Anything else is never copied into a public distributable archive.
    """
    parts=PurePosixPath(rel).parts
    if rel in ('AGENTS.md','README.md','PROTOCOL.md','VERSION.json',MANIFEST):return True
    if parts[:1]==('spec',):
        return (len(parts)==2 and parts[1].endswith('.md') or
                len(parts)==3 and parts[1]=='schemas' and (parts[2].endswith('.schema.json') or parts[2]=='README.md'))
    if parts[:1]==('references',):return len(parts)==2 and (parts[1].endswith('.md') or parts[1]=='visualization-viewer.html')
    if parts[:1]==('templates',):
        return (len(parts)==2 and parts[1] in ('README.md','MARKETING-LIBRARY.md') or
                len(parts)==3 and parts[2] in ('README.md','template.yaml') or
                len(parts)==5 and parts[2]=='skills' and parts[4]=='SKILL.md' or
                len(parts)>=4 and parts[2]=='assets' and parts[-1].lower().endswith(('.png','.jpg','.jpeg','.svg','.webp')))
    if parts[:1]==('agent-files',):return rel[len('agent-files/'):] in SEED
    return False

def no_symlink(path, root):
    path = Path(path)
    if not path.resolve().is_relative_to(root.resolve()): raise DistributionError('Outside scaffold source')
    if path.is_symlink() or any(x.is_symlink() for x in (path, *path.parents) if x.exists() and x != root.parent):
        raise DistributionError('Symlinks not accepted: ' + str(path))

def build(source: Path, dest: Path):
    source = source.resolve(); dest = dest.resolve()
    if not source.is_dir() or not (source/'VERSION.json').is_file(): raise DistributionError('Expected real scaffold/aos-w source')
    no_symlink(source,source)
    version=json.loads((source/'VERSION.json').read_text())['aosw_version']
    files={}
    for p in sorted(source.rglob('*')):
        if p.is_symlink(): raise DistributionError('Source symlink: '+str(p))
        if not p.is_file(): continue
        no_symlink(p,source)
        rel=p.relative_to(source).as_posix()
        if not permitted(rel): continue  # privacy: no active user content or sample instance
        data=p.read_bytes()
        if len(data)>MAX_FILE: raise DistributionError('Oversized distribution file')
        if len(data)+sum(map(len,files.values()))>MAX_TOTAL: raise DistributionError('Oversized distribution')
        files[rel]=data
    for req in ('README.md','PROTOCOL.md','VERSION.json','spec/README.md',
                'templates/README.md','references/README.md','agent-files/README.md','agent-files/config/settings.json'):
        if req not in files: raise DistributionError('Missing required framework file: '+req)
    if len(files)>MAX_FILES: raise DistributionError('Too many files')
    manifest={'format':'aos-w-standalone-zip-v1','version':version,'user_data_policy':'clean_seed_only',
              'protected_roots':list(PROTECTED),'user_seed_files':list(SEED),
              'entries':{p:{'sha256':sha(b),'bytes':len(b)} for p,b in sorted(files.items())}}
    files[MANIFEST]=jsonpretty(manifest)
    dest.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=dest.parent,prefix='.aosw-zip-',suffix='.zip',delete=False) as tf: tmp=Path(tf.name)
    try:
        with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for d in ('aos-w/','aos-w/agent-files/',*[f'aos-w/agent-files/{x}/' for x in USER_DIRS]):
                zi=zipfile.ZipInfo(d,EPOCH);zi.external_attr=(0o40755<<16);z.writestr(zi,b'')
            for p,b in sorted(files.items()):
                zi=zipfile.ZipInfo('aos-w/'+p,EPOCH);zi.compress_type=zipfile.ZIP_DEFLATED
                zi.external_attr=(0o100644<<16)
                z.writestr(zi,b)
        if tmp.stat().st_size>MAX_ZIP_BYTES: raise DistributionError('ZIP over size limit')
        verify(tmp)
        os.replace(tmp,dest)
    finally: tmp.unlink(missing_ok=True)
    return {'zip':str(dest),'version':version,'files':len(files),'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes())}

def verify(archive: Path):
    archive=Path(archive)
    if not archive.is_file() or archive.stat().st_size>MAX_ZIP_BYTES:raise DistributionError('ZIP missing/oversize')
    seen=set();files={};total=0
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            if info.filename.endswith('/'):
                # only predefined scaffold root or empty user directory skeleton
                valid={'aos-w/','aos-w/agent-files/',*[f'aos-w/agent-files/{x}/' for x in USER_DIRS]}
                if info.filename not in valid:raise DistributionError('Unexpected directory record')
                continue
            name=info.filename
            p=safe_pure(name);rel=p.relative_to('aos-w').as_posix()
            if not permitted(rel):raise DistributionError('Unexpected or private file: '+rel)
            if name.lower() in seen:raise DistributionError('Duplicate or case-colliding ZIP entry')
            seen.add(name.lower())
            if (info.external_attr>>16)&0o170000 == 0o120000:raise DistributionError('Archive symlink')
            if info.file_size>MAX_FILE:raise DistributionError('Archive file too large')
            total+=info.file_size
            if total>MAX_TOTAL or len(seen)>MAX_FILES:raise DistributionError('Archive total exceeds limits')
            files[rel]=z.read(info)
    if MANIFEST not in files:raise DistributionError('Manifest missing')
    m=json.loads(files.pop(MANIFEST))
    if m.get('format')!='aos-w-standalone-zip-v1' or m.get('user_data_policy')!='clean_seed_only':raise DistributionError('Invalid format/policy')
    if set(files)!=set(m['entries']):raise DistributionError('Manifest file list mismatch')
    for k,v in m['entries'].items():
        if len(files[k])!=v['bytes'] or sha(files[k])!=v['sha256']:
            raise DistributionError('SHA256 mismatch: '+k)
    if json.loads(files['VERSION.json'])['aosw_version']!=m['version']:raise DistributionError('Version mismatch')
    for p in ('README.md','PROTOCOL.md','VERSION.json','spec/README.md','templates/README.md',
              'agent-files/README.md','agent-files/config/settings.json'):
        if p not in files:raise DistributionError('Required installed content absent: '+p)
    if tuple(map(int,m['version'].split('.')[:2])) >= (0,9) and 'AGENTS.md' not in files:
        raise DistributionError('v0.9+ archive requires AGENTS.md')
    return m,files

def _safe_user_tree(existing: Path):
    # Reject symlinked user-owned trees. Upgrade must not follow links outside root.
    if existing.is_symlink(): raise DistributionError('Agent-files symlink prohibited on upgrade')
    if existing.exists():
        for p in existing.rglob('*'):
            if p.is_symlink():raise DistributionError('Symlink under user data; upgrade blocked')

def install(archive: Path, destination: Path, upgrade=False):
    """destination is final .../aos-w directory; fail safe with preserved previous tree."""
    manifest,files=verify(archive);dest=Path(destination).absolute()
    if dest.name!='aos-w':raise DistributionError('Destination must end in aos-w')
    if dest.is_symlink():raise DistributionError('Destination symlink prohibited')
    if dest.exists()!=bool(upgrade):raise DistributionError('Use upgrade only for existing destination; install only for absent destination')
    dest.parent.mkdir(parents=True,exist_ok=True)
    original_user=dest/'agent-files'
    if upgrade:
        if not original_user.is_dir():raise DistributionError('Existing installation has no agent-files')
        _safe_user_tree(original_user)
        current=json.loads((dest/'VERSION.json').read_text())
        if str(current['schema_version']).split('.')[0] != '1':raise DistributionError('Unknown schema major version, migration required')
    stage=Path(tempfile.mkdtemp(dir=dest.parent,prefix='.aosw-staging-'))
    backup=None
    try:
        for rel,content in files.items():
            if rel.startswith('agent-files/') and upgrade: continue
            target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as f:f.write(content)
        user=stage/'agent-files'
        if upgrade:
            shutil.copytree(original_user,user,copy_function=shutil.copy2,dirs_exist_ok=False)
        else:
            for d in USER_DIRS:(user/d).mkdir(parents=True,exist_ok=True)
        # No accidental missing agent-files area or normal runtime writes outside it.
        if not (user/'config').is_dir():raise DistributionError('Missing user configuration')
        if upgrade:
            backup=Path(tempfile.mkdtemp(dir=dest.parent,prefix='.aosw-backup-'))
            backup.rmdir() # reserve unique name; then rename original atomically when supported
            os.replace(dest,backup)
        try:os.replace(stage,dest)
        except BaseException:
            if backup is not None and backup.exists():os.replace(backup,dest)
            raise
        return {'version':manifest['version'],'installed':str(dest),'upgraded':bool(upgrade),
                'backup':str(backup) if backup else None,'preserved_agent_files':bool(upgrade)}
    finally:
        if stage.exists():shutil.rmtree(stage)

def main(argv=None):
    ap=argparse.ArgumentParser(description='OPTIONAL portable AOS-W distributor (Python stdlib); not a runtime requirement')
    cmd=ap.add_subparsers(dest='action',required=True)
    b=cmd.add_parser('build');b.add_argument('source',type=Path);b.add_argument('zip',type=Path)
    v=cmd.add_parser('verify');v.add_argument('zip',type=Path)
    for name in ('install','upgrade'):
        p=cmd.add_parser(name);p.add_argument('zip',type=Path);p.add_argument('destination',type=Path)
    a=ap.parse_args(argv)
    try:
        result=build(a.source,a.zip) if a.action=='build' else ({'verified':True,'version':verify(a.zip)[0]['version']} if a.action=='verify' else install(a.zip,a.destination,upgrade=a.action=='upgrade'))
        print(json.dumps(result,indent=2,sort_keys=True));return 0
    except (DistributionError,OSError,KeyError,ValueError,zipfile.BadZipFile) as exc:
        print('BLOCKED: '+str(exc),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
