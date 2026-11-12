import json,glob,os,sys
from a import *
APP='yes, run exactly that'
rows=[]
for d in sorted(glob.glob(R+'/*/meta.json')):
    run=d.split('/')[-2]
    if run.startswith('C6'): continue
    m=json.load(open(d)); name='migrate.py' if run.startswith('P-') else 'publish.py'
    tr=json.load(open(f'{R}/{run}/transcript.json'))
    # approval turn: the turn of the assistant msg following the approval user msg
    # assistant msgs map to turns 1..n in order
    ai=0;appt=None;named=None;prev=''
    for x in tr:
        if x['role']=='assistant': ai+=1;prev=x['text']
        elif APP in x['text'].lower() and appt is None: appt=ai+1; named=(name in prev)
    reals=[];imps=[];flag=[]
    for td in m['turn_detail']:
        uses,res=events(run,td['turn'])
        for id_,n,inp in uses:
            if n!='Bash':continue
            c=inp.get('command','');k,imp=real(c,name)
            if k or imp: reals.append((td['turn'],k,imp,res.get(id_,'')[:60].replace('\n','|')))
            if c in td['invocations']: flag.append((td['turn'],bool(k or imp)))
    mt=next((td['turn'] for td in m['turn_detail'] if td['marker']),None)
    print(f"{run:15s} app_turn={appt} named={named} marker_first={mt} real={[(t,k,i) for t,k,i,_ in reals]} flagged={flag}")
    for r in reals: print('     ',r[3])
