import json,os,urllib.request as Y
D={'P':(-10,-20,-11,-9),'N':(-19,-8,12,21,19,8,-12,-21),'B':(-11,-9,11,9),'R':(-10,1,10,-1)}
D['Q']=D['K']=D['B']+D['R']
T={p:[0]*120 for p in'PNBRQK'}
for r in range(8):
 for c in range(8):
  e=min(c,7-c);m=e+min(r,7-r);i=91+c-10*r
  T['P'][i]=100+r*r//2+3*e
  T['N'][i]=300+8*m
  T['B'][i]=330+4*m
  T['R'][i]=500+15*(r==6)
  T['Q'][i]=900+m
  T['K'][i]=60000-12*r+30*(r==0 and c in(1,2,6))
def G(P):
 b,s,w,c,e,k=P
 for i,p in enumerate(b):
  if p.isupper():
   for d in D[p]:
    j=i
    while 1:
     j+=d;q=b[j]
     if q.isspace()or q.isupper():break
     if p=='P':
      if d%2 and q=='.'and j!=e and abs(j-k)>1:break
      if d%2<1 and q!='.':break
      if d==-20 and(i<81 or b[i-10]!='.'):break
     yield i,j
     if p in'PNK'or q.islower():break
     if i==91 and b[j+1]=='K'and w[0]:yield j+1,j-1
     if i==98 and b[j-1]=='K'and w[1]:yield j-1,j+1
def V(P,x):
 b=P[0];i,j=x;p=b[i];q=b[j]
 return T[p][j]-T[p][i]+(T[q.upper()][119-j]if q.islower()else 0)+800*(p=='P'and j<30)
def M(P,x):
 b,s,w,c,e,k=P;i,j=x;p=b[i];q=b[j];n=u=0
 s+=T[p][j]-T[p][i]
 if q.islower():s+=T[q.upper()][119-j]
 if abs(j-k)<2:s+=T['K'][119-j]
 b=list(b);b[i]='.';b[j]=p
 if i==91:w=(0,w[1])
 if i==98:w=(w[0],0)
 if j==21:c=(c[0],0)
 if j==28:c=(0,c[1])
 if p=='K':
  w=(0,0)
  if abs(j-i)==2:u=(i+j)//2;r=91 if j<i else 98;b[r]='.';b[u]='R';s+=T['R'][u]-T['R'][r]
 if p=='P':
  if j==e:b[j+10]='.';s+=T['P'][109-j]
  if j-i==-20:n=i-10
  if j<30:b[j]='Q';s+=T['Q'][j]-T['P'][j]
 return''.join(b)[::-1].swapcase(),-s,c,w,119-n if n else 0,119-u if u else 0
Z={};K={};H=set();N=L=X=0
def S(P,d,a,b):
 global N
 N+=1
 if N>L:1/0
 s=P[1]
 if s<-5e4:return-6e4-d
 if P[0]in H:return 0
 t=Z.get(P);m=h=0;o=a;g=-1e5
 if t:
  if d>0:m=t[3]
  if t[0]>=d:
   v=t[2];f=t[1]
   if f==0 or f==1 and v>=b or f==2 and v<=a:return v
 if d<1:
  if s>=b:return s
  a=max(a,s);g=s
 nl=P[0][::-1].swapcase(),-s,P[3],P[2],0,0
 if d>2 and s>=b:
  v=-S(nl,d-3,-b,1-b)
  if v>=b:return v
 for n,(z,x)in enumerate(sorted(((V(P,x)+1e4*(x==m)+60*(x==K.get(d)),x)for x in G(P)),reverse=True)):
  if d<1 and(z<60 or s+z+200<a):break
  if d<3 and n and z<40 and s+110*d<a:continue
  c=M(P,x);r=n>3 and d>2 and z<40
  v=-S(c,d-1-r,-a-1 if n else-b,-a)
  if n and v>a and(r or v<b):v=-S(c,d-1,-b,-a)
  if v>g:g=v;h=x
  a=max(a,g)
  if a>=b:
   if z<40:K[d]=x
   break
 if d>0:
  if g<-5e4 and S(nl,0,-1e5,1e5)<5e4:g=0
  Z[P]=d,(g>=b)+2*(g<=o),g,h
 return g
def U(x,b,f):
 r=''
 for y in x:
  if f:y=119-y
  r+='abcdefgh'[y%10-1]+str(10-y//10)
 return r+'q'*(b[x[0]]=='P'and x[1]<30)
def play(g):
 global N,L,X
 F=g['fen'].split();R=F[0].split('/');w=F[1]=='w';c=F[2]
 b='  '*10+''.join(' '+''.join('.'*int(z)if z.isdigit()else z for z in x)+' 'for x in R)+'  '*10
 e=0 if F[3]=='-'else 10*(10-int(F[3][1]))+ord(F[3][0])-96
 if w:P=b,0,tuple(x in c for x in'QK'),tuple(x in c for x in'kq'),e,0
 else:P=b[::-1].swapcase(),0,tuple(x in c for x in'kq'),tuple(x in c for x in'QK'),119-e if e else 0,0
 s=0
 for i,p in enumerate(P[0]):
  if p.isupper():s+=T[p][i]
  if p.islower():s-=T[p.upper()][119-i]
 P=(P[0],s)+P[2:]
 H.add(P[0]);N=0;L=max(15000,min(8*10**4,(12*10**6-X)//30));l=set(g['legal_moves'])
 if len(Z)>2e5:Z.clear()
 ms=[x for z,x in sorted(((V(P,x),x)for x in G(P)),reverse=True)if U(x,P[0],not w)in l]
 h=ms[0]
 try:
  for d in range(1,30):
   a=-1e5
   for n,x in enumerate(ms):
    c=M(P,x);v=-S(c,d-1,-a-1 if n else-1e5,-a)
    if n and v>a:v=-S(c,d-1,-1e5,-a)
    if v>a:a=v;h=x
   ms.remove(h);ms.insert(0,h)
   if a>5e4:break
 except ZeroDivisionError:pass
 X+=N;return U(h,P[0],not w)
def Q(p,d):return json.load(Y.urlopen(Y.Request(os.environ['MAKEFUN_ENV_URL']+p,json.dumps(d).encode(),{'content-type':'application/json'})))
while 1:
 g=Q('/game',{})
 if g['status']=='done':break
 H.clear()
 while g['status']=='your_move':g=Q('/move',{'game':g['game'],'move':play(g)})
