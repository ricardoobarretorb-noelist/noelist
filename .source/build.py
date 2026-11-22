# Gera, a partir de noelist.html: a versão para o Artifact (claude.ai) e a pasta app/ (site instalável)
import re, shutil, os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB=sys.argv[1] if len(sys.argv)>1 else None   # pasta com firebase-*-compat.js
ART=sys.argv[2] if len(sys.argv)>2 else None  # destino da versão Artifact
s=open(os.path.join(ROOT,'noelist.html')).read()
head=s.split('<head>')[1].split('</head>')[0]; body=s.split('<body>')[1].split('</body>')[0]
if ART:
    h=re.sub(r'<meta charset[^>]*>\n|<meta name="viewport"[^>]*>\n','',head)
    open(ART,'w').write(h.strip()+'\n'+body)
app=os.path.join(ROOT,'app')
extra_head='''<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#24150c">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Noel'ist">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="icon-192.png">
'''
scripts='''<script src="firebase-app-compat.js"></script>
<script src="firebase-auth-compat.js"></script>
<script src="firebase-firestore-compat.js"></script>
<script src="config.js"></script>
<script>if('serviceWorker' in navigator&&location.protocol==='https:')navigator.serviceWorker.register('sw.js');</script>
'''
out=s.replace('</head>',extra_head+'</head>',1)
i=out.rindex('<script>\nconst KEY')
out=out[:i]+scripts+out[i:]
open(os.path.join(app,'index.html'),'w').write(out)
if FB:
    for f in ['app','auth','firestore']:
        shutil.copy(os.path.join(FB,f'firebase-{f}-compat.js'),app)
print('ok')
