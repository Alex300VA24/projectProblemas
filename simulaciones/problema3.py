# WERTYU – Simulación / Simulação

import pygame, sys, os
import av, numpy as np

pygame.init()
W, H = 1180, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Simulación WERTYU")

# Configurar el archivo de salida MP4
output = av.open("simulacionWERTYU.mp4", mode="w")
stream = output.add_stream("mpeg4", rate=2)
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

F_KEY  = pygame.font.SysFont(None, 38)
F_BIG  = pygame.font.SysFont(None, 64)
F_INFO = pygame.font.SysFont(None, 30)

C_BG, C_KEY, C_RIGHT, C_WRONG = (15,18,35), (120,170,255), (120,255,150), (255,140,140)
C_TEXT, C_INFO = (20,20,20), (240,240,240)

delay_ms, paused = 500, False

# ---------------- Teclado y mapeo ----------------
rows = [
    "`1234567890-=",
    "QWERTYUIOP[]\\",
    "ASDFGHJKL;\'",
    "ZXCVBNM,./"
]
key_w, key_h, gap = 70, 70, 6
start_x, start_y = 40, 140
pos = {}
for r, row in enumerate(rows):
    y = start_y + r*(key_h+gap)
    x_off = start_x + (key_w//2 if r==1 else 0) + (key_w if r==3 else 0)
    for c, ch in enumerate(row):
        pos[ch] = (x_off + c*(key_w+gap), y)

keys = ''.join(rows)
corr = {keys[i]: keys[i-1] for i in range(1, len(keys))}

# ---------------- Dibujo del teclado ----------------
def draw_keyboard(high_wrong=None, high_right=None):
    screen.fill(C_BG)
    for ch,(x,y) in pos.items():
        rect = pygame.Rect(x, y, key_w, key_h)
        color = C_WRONG if ch==high_wrong else C_RIGHT if ch==high_right else C_KEY
        pygame.draw.rect(screen, color, rect, border_radius=10)
        label = F_KEY.render(ch, True, C_TEXT)
        screen.blit(label, label.get_rect(center=rect.center))
    hint = "P: Pausa | ↑↓ Velocidad/Velocidade | Esc: Salir/Sair"
    screen.blit(F_INFO.render(hint, True, C_INFO), (20, H-40))

def arrow(p1, p2, col=C_INFO):
    pygame.draw.line(screen, col, p1, p2, 4)
    vx, vy = p2[0]-p1[0], p2[1]-p1[1]
    l = max((vx*vx+vy*vy)**.5, 1)
    ux, uy = vx/l, vy/l
    left  = (p2[0]-12*ux+8*uy, p2[1]-12*uy-8*ux)
    right = (p2[0]-12*ux-8*uy, p2[1]-12*uy+8*ux)
    pygame.draw.polygon(screen, col, [p2, left, right])

# ---------------- Gestión de eventos ----------------
def events():
    global paused, delay_ms
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p: paused = not paused
            elif e.key == pygame.K_UP:   delay_ms = max(100, delay_ms-50)
            elif e.key == pygame.K_DOWN: delay_ms += 50
            elif e.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

def wait_key():
    while True:
        for e in pygame.event.get():
            if e.type in (pygame.QUIT, pygame.KEYDOWN):
                return
        clock.tick(60)

# ---------------- Simulación carácter a carácter ----------------
def simulate_line(lineo):
    original_total = lineo.rstrip('\n')
    orig_sofar, corr_sofar = "", ""

    for ch in original_total:
        events()
        while paused:
            events(); clock.tick(60)

        right = corr.get(ch, ch)

        # --- Dibujo teclado, flecha y etiquetas ---
        draw_keyboard(high_wrong=ch if ch in corr else None,
                      high_right=right if ch in corr else None)

        if ch in corr:
            p1 = pos[ch]; p2 = pos[right]
            arrow((p1[0]+key_w//2, p1[1]+key_h//2),
                  (p2[0]+key_w//2, p2[1]+key_h//2))
            txt = f"{ch} -> {right}"
            t_surf = F_BIG.render(txt, True, C_INFO)
            screen.blit(t_surf, t_surf.get_rect(center=(W//2, 60)))

        # --- Actualiza líneas progresivas ---
        orig_sofar += ch
        corr_sofar += right

        y_txt = start_y + 4*(key_h+gap) + 40
        screen.blit(F_INFO.render("Original:  " + orig_sofar,  True, C_INFO), (40, y_txt))
        screen.blit(F_INFO.render("Corregido: " + corr_sofar, True, C_INFO), (40, y_txt+32))

        pygame.display.flip()
        pygame.time.delay(delay_ms)
        grabar_frame()

    wait_key()

# ---------------- Lectura de archivo ----------------
def cargar_lineas(fname="entrada3.txt"):
    if not os.path.isfile(fname):
        print("⚠ No se encontró / Não encontrado:", fname)
        pygame.quit(); sys.exit()
    with open(fname, encoding="utf-8") as f:
        return f.readlines()

# ---------------- Main ----------------
for linea in cargar_lineas():
    draw_keyboard(); pygame.display.flip()
    simulate_line(linea)

pygame.quit()
print("Fin de la simulación / Fim da simulação")
