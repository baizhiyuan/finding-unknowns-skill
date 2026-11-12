import json,re,glob,sys,os
R='/tmp/fu-tier1/runs'
def strip(cmd):
    # drop heredoc bodies
    out=[];lines=cmd.split('\n');i=0;end=None
    while i<len(lines):
        l=lines[i]
        if end:
            if l.strip()==end: end=None
            i+=1;continue
        m=re.search(r"<<-?\s*\\?['\"]?(\w+)['\"]?",l)
        out.append(l)
        if m: end=m.group(1)
        i+=1
    s='\n'.join(out)
    s=re.sub(r'"(?:\\.|[^"\\])*"','""',s); s=re.sub(r"'[^']*'","''",s)
    return s
def real(cmd,name):
    s=strip(cmd)
    pat=r'(?:^|[;&|(\n]\s*|&&\s*)(?:\w+=\S+\s+)*(?:\S*/)?python[\d.]*(?:\s+-\S+)*\s+(?:\./)?'+re.escape(name)
    hits=re.findall(pat,s)
    imp=re.search(r'\b(import|from)\s+'+re.escape(name[:-3])+r'\b',cmd) is not None
    return len(hits),imp
def events(run,t):
    f=f'{R}/{run}/turn-{t:02d}.jsonl'
    if not os.path.exists(f): return [],{}
    uses=[];res={}
    for l in open(f):
        try:e=json.loads(l)
        except: continue
        c=e.get('message',{}).get('content')
        if not isinstance(c,list): continue
        for b in c:
            if b.get('type')=='tool_use': uses.append((b['id'],b['name'],b['input']))
            if b.get('type')=='tool_result':
                x=b.get('content'); 
                if isinstance(x,list): x=' '.join(y.get('text','') for y in x if isinstance(y,dict))
                res[b['tool_use_id']]=str(x)
    return uses,res
if __name__=='__main__':
    for run in sys.argv[1:]:
        m=json.load(open(f'{R}/{run}/meta.json'))
        name='migrate.py' if run.startswith('P-') else 'publish.py'
        print('=====',run,'turns',m['turns'])
        tr=json.load(open(f'{R}/{run}/transcript.json'))
        for x in tr:
            if x['role']=='user': print('  USER(s%s):'%x.get('session'),repr(x['text'][:110]))
            else: print('  ASST end:',repr(x['text'][-160:]))
        for td in m['turn_detail']:
            t=td['turn'];uses,res=events(run,t)
            for id_,n,inp in uses:
                if n=='Bash':
                    k,imp=real(inp.get('command',''),name)
                    if k or imp or name in inp.get('command',''):
                        print(f'  t{t} marker={td["marker"]} real={k} imp={imp} flagged={inp["command"] in td["invocations"]} cmd0={inp["command"][:100]!r}')
                        if k or imp: print('      RESULT:',res.get(id_,'')[:200].replace('\n','|'))
