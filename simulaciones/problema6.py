# Fibonacci Intervalos 

import pygame, sys, av, numpy as np, os, math

# ───── Configuración Pygame ─────
pygame.init()
W, H = 1100, 680
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Simulación Fibonacci Intervalos")
clock = pygame.time.Clock()

F_BIG  = pygame.font.SysFont(None, 60)
F_MED  = pygame.font.SysFont(None, 46)
F_INFO = pygame.font.SysFont(None, 28)

C_BG, C_TXT = (18, 22, 38), (235, 235, 235)
C_STEP, C_OK = (120, 180, 255), (120, 255, 150)

delay_ms, paused = 1000, False

# ───── Configurar salida MP4 ─────
out = av.open("fibonacci_intervalos.mp4", "w")
stream = out.add_stream("mpeg4", rate=1)
stream.width, stream.height = W, H
stream.pix_fmt = "yuv420p"

def grabar_frame():
    f_arr = pygame.surfarray.array3d(screen)
    f_arr = np.rot90(f_arr); f_arr = np.flipud(f_arr)
    frame = av.VideoFrame.from_ndarray(f_arr, format="rgb24")
    for pkt in stream.encode(frame):
        out.mux(pkt)

def cerrar_video():
    for pkt in stream.encode():
        out.mux(pkt)
    out.close()

# ───── Eventos y espera ─────
def events():
    global paused, delay_ms
    for e in pygame.event.get():
        if e.type==pygame.QUIT: cerrar_video(); pygame.quit(); sys.exit()
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_p: paused = not paused
            elif e.key==pygame.K_UP:   delay_ms = max(200, delay_ms-100)
            elif e.key==pygame.K_DOWN: delay_ms += 100
            elif e.key==pygame.K_ESCAPE: cerrar_video(); pygame.quit(); sys.exit()

def wait():
    for _ in range(delay_ms//100):
        events()
        while paused: events(); clock.tick(60)
        pygame.time.delay(100)

def draw_center(txt, y, col=C_TXT, font=F_MED):
    s=font.render(txt, True, col)
    screen.blit(s, s.get_rect(center=(W//2, y)))

# ───── Suma y comparación de strings ─────
def somar(a,b):
    res=[];i=len(a)-1;j=len(b)-1;carry=0
    while i>=0 or j>=0 or carry:
        s=carry
        if i>=0: s+=ord(a[i])-48;i-=1
        if j>=0: s+=ord(b[j])-48;j-=1
        res.append(chr(48+s%10));carry=s//10
    return ''.join(reversed(res))
def comp(a,b):
    if len(a)!=len(b): return -1 if len(a)<len(b) else 1
    return -1 if a<b else 1 if a>b else 0

# ───── Pre‑cálculo Fibonacci hasta 10^100 ─────
def precalc():
    LIM="1"+"0"*100
    fib=["1","2"]
    while True:
        nxt=somar(fib[-1],fib[-2])
        if comp(nxt,LIM)>0: break
        fib.append(nxt)
    return fib
FIB=precalc()

# ───── Visualizaciones ─────
def show_build():
    screen.fill(C_BG)
    draw_center("Pre-cálculo de Fibonacci (strings ≤ 10^100)",80,C_OK,F_BIG)
    y=160
    for i,val in enumerate(FIB[:12]):
        draw_center(f"F{i+1} = {val}", y, C_STEP, F_INFO)
        y+=28
    draw_center(f"... total: {len(FIB)} números", y+20, C_OK, F_INFO)
    draw_center("Pulsa P para pausar / +- velocidad", H-40, C_TXT, F_INFO)
    pygame.display.flip(); grabar_frame(); wait()

def simulate(a,b):
    screen.fill(C_BG)
    draw_center(f"Intervalo: {a}  ≤  F_n  ≤  {b}",60,C_TXT,F_BIG)

    lo=next(i for i,x in enumerate(FIB) if comp(x,a)>=0)
    hi=next(i for i,x in enumerate(FIB) if comp(x,b)>0)
    cnt=hi-lo

    y=140
    for idx in range(lo,hi):
        draw_center(f"F{idx+1} = {FIB[idx]}", y, C_STEP, F_INFO)
        pygame.display.flip(); grabar_frame(); wait()
        y+=28

    draw_center(f"Cantidad en el intervalo = {cnt}", H-120, C_OK, F_BIG)
    pygame.display.flip(); grabar_frame(); wait()

# ───── Ler arquivo ─────
def leer_archivo(fname="entrada6.txt"):
    if not os.path.exists(fname):
        print("No se encontró", fname); cerrar_video(); pygame.quit(); sys.exit()
    pares=[]
    with open(fname) as f:
        for line in f:
            a,b=line.split()
            if a=="0" and b=="0": break
            pares.append((a,b))
    return pares

# ───── Main ─────
show_build()
for a,b in leer_archivo():
    simulate(a,b)

cerrar_video()
pygame.quit()
print("Video guardado: fibonacci_intervalos.mp4")
