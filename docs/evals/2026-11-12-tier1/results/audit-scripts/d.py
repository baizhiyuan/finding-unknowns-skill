import json,glob,collections,re,sys
from a import events,R
def final_mu(run,turn):
    mu=None
    for l in open(f'{R}/{run}/turn-{turn:02d}.jsonl'):
        try:e=json.loads(l)
        except:continue
        if e.get('type')=='result' and e.get('modelUsage'): mu=e['modelUsage']
    return mu
def analyze(run):
    m=json.load(open(f'{R}/{run}/meta.json'))
    last={};prev={};rows=[]
    agent_turn=[]
    for t in m['turn_detail']:
        s=t['session'];d=t['cost']-prev.get(s,0);prev[s]=t['cost'];last[s]=t['turn']
        uses,_=events(run,t['turn'])
        tools=collections.Counter(n for _,n,_ in uses)
        fu=sum(len(re.findall(r'fu\.py|\$FU\b|\$F ',i.get('command',''))) for _,n,i in uses if n=='Bash')
        rows.append((t['turn'],round(d,3),dict(tools),fu))
    tot=collections.Counter()
    for s,tn in last.items():
        mu=final_mu(run,tn)
        for model,v in mu.items():
            for k in('cacheReadInputTokens','cacheCreationInputTokens','outputTokens','inputTokens','costUSD'): tot[k]+=v[k]
    return m,rows,tot
if __name__=='__main__':
    for run in sys.argv[1:]:
        m,rows,tot=analyze(run)
        print('==',run,'true$',round(tot['costUSD'],3),{k:v for k,v in tot.items() if k!='costUSD'})
        for r in rows: print('   ',r)
