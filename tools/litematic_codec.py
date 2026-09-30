from __future__ import annotations
import gzip,io,struct
from collections import OrderedDict
from pathlib import Path
TAG_BYTE=1;TAG_SHORT=2;TAG_INT=3;TAG_LONG=4;TAG_BYTE_ARRAY=7;TAG_STRING=8;TAG_LIST=9;TAG_COMPOUND=10;TAG_INT_ARRAY=11;TAG_LONG_ARRAY=12
class B:
 def __init__(self,v):self.v=int(v)
class I:
 def __init__(self,v):self.v=int(v)
class L:
 def __init__(self,v):self.v=int(v)
class LA:
 def __init__(self,v):self.v=[int(x) for x in v]
class LT:
 def __init__(self,etype,v):self.etype=etype;self.v=v
def i64(v):
 v&=(1<<64)-1;return v-(1<<64) if v>=(1<<63) else v
def typ(v):
 if isinstance(v,B):return TAG_BYTE
 if isinstance(v,I):return TAG_INT
 if isinstance(v,L):return TAG_LONG
 if isinstance(v,LA):return TAG_LONG_ARRAY
 if isinstance(v,LT):return TAG_LIST
 if isinstance(v,str):return TAG_STRING
 if isinstance(v,dict):return TAG_COMPOUND
 raise TypeError(type(v))
def wstr(f,s):b=s.encode();f.write(struct.pack('>H',len(b)));f.write(b)
def wp(f,v,t=None):
 t=typ(v) if t is None else t
 if t==TAG_BYTE:f.write(struct.pack('>b',v.v))
 elif t==TAG_INT:f.write(struct.pack('>i',v.v))
 elif t==TAG_LONG:f.write(struct.pack('>q',i64(v.v)))
 elif t==TAG_STRING:wstr(f,v)
 elif t==TAG_LONG_ARRAY:
  f.write(struct.pack('>i',len(v.v)))
  for x in v.v:f.write(struct.pack('>q',i64(x)))
 elif t==TAG_LIST:
  f.write(struct.pack('>b',v.etype));f.write(struct.pack('>i',len(v.v)))
  for x in v.v:wp(f,x,v.etype)
 elif t==TAG_COMPOUND:
  for k,x in v.items():
   tt=typ(x);f.write(struct.pack('>b',tt));wstr(f,k);wp(f,x,tt)
  f.write(b'\0')
 else:raise ValueError(t)
def write(path,root,name=''):
 raw=io.BytesIO();raw.write(bytes([TAG_COMPOUND]));wstr(raw,name);wp(raw,root,TAG_COMPOUND)
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('wb') as fh:
  with gzip.GzipFile(fileobj=fh,mode='wb',compresslevel=6,mtime=0) as g:g.write(raw.getvalue())
class R:
 def __init__(self,d):self.d=d;self.p=0
 def take(self,n):b=self.d[self.p:self.p+n];self.p+=n;return b
 def b(self):return struct.unpack('>b',self.take(1))[0]
 def s(self):return struct.unpack('>h',self.take(2))[0]
 def i(self):return struct.unpack('>i',self.take(4))[0]
 def l(self):return struct.unpack('>q',self.take(8))[0]
 def st(self):n=struct.unpack('>H',self.take(2))[0];return self.take(n).decode('utf8')
 def payload(self,t):
  if t==TAG_BYTE:return self.b()
  if t==TAG_SHORT:return self.s()
  if t==TAG_INT:return self.i()
  if t==TAG_LONG:return self.l()
  if t==TAG_STRING:return self.st()
  if t==TAG_BYTE_ARRAY:return self.take(self.i())
  if t==TAG_INT_ARRAY:
   n=self.i();return [self.i() for _ in range(n)]
  if t==TAG_LONG_ARRAY:
   n=self.i();return [self.l() for _ in range(n)]
  if t==TAG_LIST:
   et=self.b();n=self.i();return [self.payload(et) for _ in range(n)]
  if t==TAG_COMPOUND:
   o={}
   while True:
    tt=self.b()
    if tt==0:return o
    key=self.st();o[key]=self.payload(tt)
  raise ValueError(t)
def read(path):
 r=R(gzip.decompress(Path(path).read_bytes()));assert r.b()==TAG_COMPOUND;r.st();return r.payload(TAG_COMPOUND)
def bits_for(n):return max(2,(n-1).bit_length())
def pack(indices,palette_size):
 bits=bits_for(palette_size);arr=[0]*((len(indices)*bits+63)//64);mask=(1<<bits)-1
 for i,val in enumerate(indices):
  bit=i*bits;li=bit//64;off=bit%64;val&=mask;arr[li]|=(val<<off)&((1<<64)-1);spill=off+bits-64
  if spill>0:arr[li+1]|=val>>(bits-spill)
 return [i64(x) for x in arr]
def unpack(longs,count,palette_size):
 u=[x&((1<<64)-1) for x in longs];bits=bits_for(palette_size);mask=(1<<bits)-1;out=[]
 for i in range(count):
  bit=i*bits;li=bit//64;off=bit%64;v=(u[li]>>off)&mask;spill=off+bits-64
  if spill>0:v|=(u[li+1]&((1<<spill)-1))<<(bits-spill)
  out.append(v)
 return out
def parse_state(s):
 if '[' not in s:return s,{}
 n,r=s.split('[',1);r=r[:-1];p={}
 if r:
  for kv in r.split(','):k,v=kv.split('=',1);p[k]=v
 return n,p
def state_tag(s):
 n,p=parse_state(s);d=OrderedDict(Name=n)
 if p:d['Properties']=OrderedDict((k,str(v)) for k,v in sorted(p.items()))
 return d
def make(path,name,size,blocks,block_entities=None,desc='Compiled BuildWright fixture',dataversion=4903):
 W,H,D=size;block_entities=block_entities or [];states=['minecraft:air']+sorted(set(blocks.values()));pi={s:i for i,s in enumerate(states)};indices=[];nonair=0
 for y in range(H):
  for z in range(D):
   for x in range(W):
    s=blocks.get((x,y,z),'minecraft:air');indices.append(pi[s]);nonair+=s!='minecraft:air'
 empty=LT(TAG_COMPOUND,[]);now=1760000000000
 root=OrderedDict([('MinecraftDataVersion',I(dataversion)),('Version',I(6)),('SubVersion',I(1)),('Metadata',OrderedDict([('Name',name),('Author','BuildWright'),('Description',desc),('RegionCount',I(1)),('TimeCreated',L(now)),('TimeModified',L(now)),('TotalBlocks',I(nonair)),('TotalVolume',I(W*H*D)),('EnclosingSize',OrderedDict(x=I(W),y=I(H),z=I(D)))])),('Regions',OrderedDict([('fixture',OrderedDict([('BlockStatePalette',LT(TAG_COMPOUND,[state_tag(s) for s in states])),('BlockStates',LA(pack(indices,len(states)))),('TileEntities',LT(TAG_COMPOUND,block_entities)),('PendingBlockTicks',empty),('PendingFluidTicks',empty),('Entities',empty),('Position',OrderedDict(x=I(0),y=I(0),z=I(0))),('Size',OrderedDict(x=I(W),y=I(H),z=I(D)))]))]))])
 write(path,root);return nonair
