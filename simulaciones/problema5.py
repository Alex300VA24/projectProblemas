# Primary Arithmetic – Simulación paso a paso / Simulação passo a passo


import pygame, sys, os, time
import av, numpy as np

pygame.init()
W, H = 1000, 620
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Primary Arithmetic - Simulación")

# Configurar el archivo de salida MP4
output = av.open("simulacionAritmethic.mp4", mode="w")
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



F_DIG  = pygame.font.SysFont(None, 56)     # dígitos grandes
F_TOP  = pygame.font.SysFont(None, 52)     # contador parcial
F_OP   = pygame.font.SysFont(None, 40)     # operación actual
F_END  = pygame.font.SysFont(None, 72)     # 🔸 frase final
F_INFO = pygame.font.SysFont(None, 28)

C_BG, C_BOX, C_HL, C_CARRY = (15,18,35), (120,170,255), (255,215,0), (120,255,150)
C_TXT, C_INFO, C_END       = (20,20,20), (235,235,235), (120,255,150)

delay_ms, paused = 900, False

# ───── utilidades de dibujo ─────
def draw_number(num_str, y, highlight_idx=-1):
    x_base = W - 80
    for i, ch in enumerate(reversed(num_str)):
        x = x_base - i*80
        rect = pygame.Rect(x-40, y, 80, 80)
        col  = C_HL if i == highlight_idx else C_BOX
        pygame.draw.rect(screen, col, rect, border_radius=8)
        screen.blit(F_DIG.render(ch, True, C_TXT),
                    F_DIG.render(ch, True, C_TXT).get_rect(center=rect.center))

def draw_carry_row(length, carry_pos=-1, blink=False):
    x_base = W - 80
    if carry_pos >= 0:
        x = x_base - carry_pos*80
        if blink:
            pygame.draw.circle(screen, C_CARRY, (x, 170), 12)

def full_redraw(a_str, b_str, col, carry_cnt, op_txt,
                blink=False, final_msg=None):
    screen.fill(C_BG)
    # contador parcial
    label = "carry operations" if carry_cnt != 1 else "carry operation"
    top   = f"{carry_cnt} {label}"
    screen.blit(F_TOP.render(top, True, C_INFO),
                F_TOP.render(top, True, C_INFO).get_rect(center=(W//2, 40)))

    # números y carries
    draw_number(a_str, 250, col)
    draw_number(b_str, 350, col)
    draw_carry_row(max(len(a_str), len(b_str))+1, col+1, blink)

    # operación actual
    if op_txt:
        screen.blit(F_OP.render(op_txt, True, C_INFO),
                    F_OP.render(op_txt, True, C_INFO).get_rect(center=(W//2, 500)))

    # 🔸 frase final
    if final_msg:
        screen.blit(F_END.render(final_msg, True, C_END),
                    F_END.render(final_msg, True, C_END).get_rect(center=(W//2, 130)))

    screen.blit(F_INFO.render("P: Pausa | ↑↓ Velocidad | Esc: Salir",
                              True, C_INFO), (20, H-40))
    pygame.display.flip()
    grabar_frame()

def events():
    global paused, delay_ms
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p: paused = not paused
            elif e.key == pygame.K_UP:   delay_ms = max(100, delay_ms-50)
            elif e.key == pygame.K_DOWN: delay_ms += 50
            elif e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

def wait_key():
    while True:
        for e in pygame.event.get():
            if e.type in (pygame.QUIT, pygame.KEYDOWN): return
        clock.tick(60)

# ───── simulación de un par ─────
def simulate_pair(a, b):
    a_str, b_str = str(a), str(b)
    carry, carries = 0, 0
    max_len = max(len(a_str), len(b_str))
    a_str, b_str = a_str.zfill(max_len), b_str.zfill(max_len)

    full_redraw(a_str, b_str, -1, carries, "")
    pygame.time.delay(delay_ms)

    for col in range(max_len):
        events()
        while paused: events(); clock.tick(60)

        da, db = int(a_str[-1-col]), int(b_str[-1-col])
        s  = da + db + carry
        op = f"{da} + {db} + {carry} = {s}"

        new_carry = 1 if s > 9 else 0
        if new_carry: carries += 1

        full_redraw(a_str, b_str, col, carries, op)
        pygame.time.delay(delay_ms)

        if new_carry:              # parpadeo
            for _ in range(2):
                full_redraw(a_str, b_str, col, carries, op, blink=True)
                pygame.time.delay(180)
                full_redraw(a_str, b_str, col, carries, op, blink=False)
                pygame.time.delay(180)

        carry = new_carry

    # mensaje final formateado 🔸
    if carries == 0:
        final_msg = "No carry operation."
    elif carries == 1:
        final_msg = "1 carry operation."
    else:
        final_msg = f"{carries} carry operations."

    full_redraw(a_str, b_str, -1, carries, "", final_msg=final_msg)
    pygame.time.delay(delay_ms)
    wait_key()

# ───── lectura de archivo ─────
def cargar_pares(fname="entrada5.txt"):
    if not os.path.isfile(fname):
        print("Archivo no encontrado:", fname); pygame.quit(); sys.exit()
    pares=[]
    with open(fname) as f:
        for line in f:
            a,b=map(int,line.split())
            if a==0 and b==0: break
            pares.append((a,b))
    return pares

# ───── main ─────
for a,b in cargar_pares():
    simulate_pair(a,b)

pygame.quit()
print("Fin de la simulación / Fim da simulação")
