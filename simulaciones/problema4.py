# Vito’s Family – Simulación paso a paso (versión 2)

import pygame, sys, os
import av, numpy as np

# ────────── Configuración ──────────
pygame.init()
W, H = 1180, 680
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Vito's Family - Simulación paso a paso")

# Configurar el archivo de salida MP4
output = av.open("simulacionVitos.mp4", mode="w")
stream = output.add_stream("mpeg4", rate=1)
stream.width = W
stream.height = H
stream.pix_fmt = "yuv420p"

def grabar_frame():
    # Captura frame
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    frame = np.rot90(frame)  # Corrige orientación
    frame = np.flipud(frame) # Voltea eje vertical
    frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
    packet = stream.encode(frame)
    if packet:
        output.mux(packet)

clock = pygame.time.Clock()

F_NUM  = pygame.font.SysFont(None, 46)
F_TOP  = pygame.font.SysFont(None, 56)   # suma parcial / mínima arriba
F_OP   = pygame.font.SysFont(None, 40)   # operación individual
F_EXPR = pygame.font.SysFont(None, 32)   # expresión acumulada
F_INFO = pygame.font.SysFont(None, 28)

C_BG, C_ADDR, C_MED, C_LINE = (15,18,35), (100,180,255), (120,255,150), (255,210,80)
C_TXT, C_INFO               = (20,20,20), (235,235,235)

delay_ms, paused = 800, False

# ────────── Dibujo ──────────
def draw(addrs, med_idx, step=-1, d=0, expr="", total=0, final=False):
    screen.fill(C_BG)
    base_y = 210
    # 1️⃣ ‑‑‑­ Suma parcial / mínima arriba
    etiqueta = "Suma mínima = " if final else "Suma parcial = "
    sum_surf = F_TOP.render(etiqueta + str(total), True, C_INFO)
    screen.blit(sum_surf, sum_surf.get_rect(center=(W//2, 40)))

    # Línea de la calle
    pygame.draw.line(screen, C_INFO, (60, base_y+40), (W-60, base_y+40), 3)
    span = max(max(addrs) - min(addrs), 1)
    xp = lambda v: 60 + (W-120)*(v - min(addrs))/span

    # Rectángulos de direcciones
    for i, v in enumerate(addrs):
        x = xp(v)
        rect = pygame.Rect(x-40, base_y-40, 80, 80)
        pygame.draw.rect(screen, C_MED if i==med_idx else C_ADDR, rect, border_radius=10)
        num_surf = F_NUM.render(str(v), True, C_TXT)
        screen.blit(num_surf, num_surf.get_rect(center=rect.center))

    # Línea de distancia acumulada
    med_x = xp(addrs[med_idx])
    for i in range(step+1):
        pygame.draw.line(screen, C_LINE, (med_x, base_y+80),
                         (xp(addrs[i]), base_y+80), 4)

    # Operación individual
    if 0 <= step < len(addrs):
        op_txt = f"| {addrs[step]} – {addrs[med_idx]} |  =  {d}"
        screen.blit(F_OP.render(op_txt, True, C_INFO),
                    F_OP.render(op_txt, True, C_INFO).get_rect(center=(W//2, base_y-90)))

    # Expresión acumulada
    screen.blit(F_EXPR.render("S = " + expr, True, C_INFO), (60, base_y+120))

    # Ayuda
    hint="P: Pausa | ↑↓ Velocidad | Esc: Salir"
    screen.blit(F_INFO.render(hint, True, C_INFO), (20, H-40))
    pygame.display.flip()
    grabar_frame()

# ────────── Eventos ──────────
def eventos():
    global paused, delay_ms
    for e in pygame.event.get():
        if e.type==pygame.QUIT: pygame.quit(); sys.exit()
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_p: paused=not paused
            elif e.key==pygame.K_UP:   delay_ms=max(100, delay_ms-50)
            elif e.key==pygame.K_DOWN: delay_ms+=50
            elif e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()

def esperar():
    while True:
        for e in pygame.event.get():
            if e.type in (pygame.QUIT, pygame.KEYDOWN): return
        clock.tick(60)

# ────────── Simulación ──────────
def sim_case(addrs):
    addrs.sort()
    m_idx = len(addrs)//2
    expr_parts, total = [], 0

    draw(addrs, m_idx, -1, 0, "", 0) # pantalla inicial
    pygame.time.delay(delay_ms)

    for i, v in enumerate(addrs):
        eventos()
        while paused: eventos(); clock.tick(60)

        d = abs(v - addrs[m_idx])
        expr_parts.append(str(d))
        total += d
        expr_text = ' + '.join(expr_parts)
        draw(addrs, m_idx, i, d, expr_text, total)
        pygame.time.delay(delay_ms)

    # Pantalla final con “Suma mínima”
    expr_final = ' + '.join(expr_parts) + f" = {total}"
    draw(addrs, m_idx, len(addrs)-1, d, expr_final, total, final=True)
    pygame.time.delay(delay_ms)
    esperar()


# ────────── Lectura de archivo ──────────
def cargar(fname="entrada4.txt"):
    if not os.path.isfile(fname):
        print("⚠ archivo", fname, "no encontrado"); pygame.quit(); sys.exit()
    with open(fname) as f:
        t = int(f.readline())
        return [list(map(int, f.readline().split()))[1:] for _ in range(t)]

# ────────── Main ──────────
for caso in cargar():
    sim_case(caso)

pygame.quit()
print("Fin de la simulación / Fim da simulação")
