# Jolly Jumpers – Simulación / Simulação

import pygame, sys, os
import av, numpy as np

# --------------- Configuración / Configuração ---------------
pygame.init()
W, H = 960, 640
n = 0
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Simulación Jolly Jumpers")

# Configurar el archivo de salida MP4
output = av.open("simulacionJolly.mp4", mode="w")
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

FONT_NUM    = pygame.font.SysFont(None, 48)   # números / números
FONT_MEDIUM = pygame.font.SysFont(None, 50)   # mensajes / mensagens
FONT_OP     = pygame.font.SysFont(None, 56)   # operación grande / operação grande
FONT_SMALL  = pygame.font.SysFont(None, 30)   # |a‑b| debajo / |a‑b| em baixo

COL_BG   = (15, 18, 35)
COL_NUM  = (100, 180, 255)
COL_DIFF = (255, 210, 60)
COL_DUP  = (240,  80,  80)
COL_HL   = (180, 255, 180)
COL_T    = ( 20,  20,  20)
COL_INFO = (235, 235, 235)

delay_ms, paused = 800, False

# ------------------ Dibujar / Desenho ------------------
def draw(seq, diffs, ops_top, ops_mid, hl=None, dup=False, msg=""):
    screen.fill(COL_BG)
    x0, y0, dx = 50, 230, 110        # espacio libre arriba / espaço livre acima

    # ---- operación grande arriba / operação grande em cima ----
    if hl is not None and hl < len(ops_top):
        op_txt = ops_top[hl]
        op_surf = FONT_OP.render(op_txt, True, COL_INFO)
        screen.blit(op_surf, op_surf.get_rect(center=(W // 2, y0 - 90)))


    # ---- Números ----
    for i, n in enumerate(seq):
        rect = pygame.Rect(x0 + i * dx, y0, 100, 80)
        pygame.draw.rect(screen, COL_NUM, rect, border_radius=10)
        if hl is not None and (i == hl or i == hl + 1):
            pygame.draw.rect(screen, COL_HL, rect, width=4, border_radius=10)
        num_surf = FONT_NUM.render(str(n), True, COL_T)
        screen.blit(num_surf, num_surf.get_rect(center=rect.center))
        

    # ---- |a-b| debajo de números ----
    y_mid = y0 + 120
    for i, op in enumerate(ops_mid):
        op_surf = FONT_SMALL.render(op, True, COL_INFO)
        center_x = x0 + i * dx + 92
        screen.blit(op_surf, op_surf.get_rect(center=(center_x, y_mid)))
        

    # ---- Diferencias ----
    y_diff = y0 + 140
    for i, d in enumerate(diffs):
        color = COL_DUP if dup and hl == i else COL_DIFF
        rect = pygame.Rect(x0 + i * dx + 45, y_diff, 100, 80)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        d_surf = FONT_NUM.render(str(d), True, COL_T)
        screen.blit(d_surf, d_surf.get_rect(center=rect.center))
        

    # ---- Mensaje e instrucciones ----
    screen.blit(FONT_MEDIUM.render(msg, True, COL_INFO), (20, 20))
    hint = "P: Pausa | ↑↓ Velocidad | Esc: Salir"
    screen.blit(FONT_MEDIUM.render(hint, True, COL_INFO), (20, H - 40))
    pygame.display.flip()
    grabar_frame()

# ------------------ Eventos / Eventos ------------------
def events():
    global paused, delay_ms
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p: paused = not paused
            elif e.key == pygame.K_UP: delay_ms = max(100, delay_ms - 50)
            elif e.key == pygame.K_DOWN: delay_ms += 50
            elif e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

def wait_key():
    while True:
        for e in pygame.event.get():
            if e.type in (pygame.QUIT, pygame.KEYDOWN): return
        clock.tick(60)

# ------------------ Simulación / Simulação ------------------
def simulate(seq):
    n = len(seq)
    diffs, ops_top, ops_mid, usado = [], [], [], set()
    jolly = True

    draw(seq, diffs, ops_top, ops_mid, msg="Calculando… / Calculando…")
    pygame.time.delay(delay_ms)

    list_d = []
    for i in range(1, n):
        events()
        while paused: events(); clock.tick(60)

        d = abs(seq[i] - seq[i - 1])
        op_big = f"|{seq[i]} - {seq[i - 1]}| = {d}"
        list_d.append(d)
        op_mid = f"|{seq[i]}-{seq[i - 1]}|"
        dup = d in usado or not (1 <= d <= n - 1)
        if dup: jolly = False
        usado.add(d)

        diffs.append(d)
        ops_top.append(op_big)
        ops_mid.append(op_mid)

        msg = f"Paso {i}: diff={d}"
        draw(seq, diffs, ops_top, ops_mid, hl=i - 1, dup=dup, msg=msg)
        pygame.time.delay(delay_ms)
        

    # Verificamos cada condición por separado para dar mensajes detallados
    if jolly and len(usado) == n - 1:
        res = f"Jolly."
    else:
        opcion = 0
        for a in list_d:
            if n < a:
                opcion = a
                break;
        res = f"Not Jolly."
        
    
    draw(seq, diffs, ops_top, ops_mid, msg=f"Resultado: {res} ")
    pygame.time.delay(delay_ms)
    wait_key()

# ------------------ Cargar archivo / Carregar ficheiro ------------------

def cargar_secuencias(archivo="entrada2.txt"):
    if not os.path.isfile(archivo):
        print(f"⚠ Archivo {archivo} no encontrado / Ficheiro {archivo} não encontrado")
        pygame.quit(); sys.exit()
    with open(archivo) as f: tokens = f.read().split()

    i, seqs = 0, []
    while i < len(tokens):
        global n
        n = int(tokens[i]); i += 1
        seq = list(map(int, tokens[i:i + n])); i += n
        if len(seq) < n: break
        seqs.append(seq)
    return seqs

# ------------------ Principal / Principal ------------------
for seq in cargar_secuencias():
    simulate(seq)

pygame.quit()
print("Fin de la simulación / Fim da simulação")
