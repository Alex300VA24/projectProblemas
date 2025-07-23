# Problema: 3n + 1 Cinemática de Collatz

import pygame
import sys
import av, numpy as np

# Configuração

pygame.init()
W, H = 960, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Cinemática Collatz: 3n + 1")

# Configurar el archivo de salida MP4
output = av.open("simulacionCollatz.mp4", mode="w")
stream = output.add_stream("mpeg4", rate=3)
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

#Fontes
FONT_SUPER_BIG   = pygame.font.SysFont(None, 130)
FONT_BIG   = pygame.font.SysFont(None, 80)
FONT_MEDIUM   = pygame.font.SysFont(None, 50)
FONT_SMALL_2   = pygame.font.SysFont(None, 32)
FONT_SMALL = pygame.font.SysFont(None, 28)
FONT_SMALLY = pygame.font.SysFont(None, 20)

# Paleta vibrante (RGB)
COL_BG        = (18, 18, 28)      # Fundo
COL_BOX_EVEN  = ( 50, 205,  50)   # Caixa par  (verde)
COL_BOX_ODD   = (255, 140,   0)   # Impar (naranja)
COL_TEXT_NUM  = ( 32,  32,  32)   # Número
COL_TEXT_INFO = (245, 245, 245)   # Texto

# Controle de tempo
delay_ms = 400
paused   = False
skip_rng = False

# Funções auxiliares

def draw_step(n, op, extra=""):
    # Desenha um passo
    screen.fill(COL_BG)

    #  Escolher cor conforme paridade
    box_color = COL_BOX_EVEN if n % 2 == 0 else COL_BOX_ODD
    rect = pygame.Rect(W//2-240, H//2-80, 480, 240) 
    pygame.draw.rect(screen, box_color, rect, border_radius=16)

    # Número / Número
    num_surf = FONT_SUPER_BIG.render(str(n), True, COL_TEXT_NUM)
    num_rect = num_surf.get_rect(center=rect.center)
    screen.blit(num_surf, num_rect)

    # Operación / Operação
    op_surf = FONT_MEDIUM.render(op, True, COL_TEXT_INFO)
    screen.blit(op_surf, (330, 100))

    # Información extra / Informação extra
    extra_surf = FONT_MEDIUM.render(extra, True, COL_TEXT_INFO)
    screen.blit(extra_surf, (310, 150))

    # Instrucciones / Instruções
    hint = "P: Pausa | + - Velocidad | S: Saltar rango | Esc: Salir"
    hint_surf = FONT_MEDIUM.render(hint, True, COL_TEXT_INFO)
    screen.blit(hint_surf, (12, H-36))
    pygame.display.flip()

def handle_events():
    """Gestiona eventos / Gerencia eventos"""
    global paused, delay_ms, skip_rng
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: paused = not paused
            elif event.key == pygame.K_UP:   delay_ms = max(100, delay_ms-50)
            elif event.key == pygame.K_DOWN: delay_ms += 50
            elif event.key == pygame.K_s:    skip_rng = True
            elif event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

def wait_key():
    """Espera una tecla / Espera uma tecla"""
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN: return
        clock.tick(60)

# ------------------ Núcleo Collatz / Núcleo Collatz ------------------

def visualize_collatz(n, etiqueta=""):
    """Muestra colisiones de n / Mostra colapsos de n"""
    global skip_rng
    sec = [n]
    while n != 1:
        handle_events()
        if skip_rng: return sec
        while paused:
            handle_events()
            clock.tick(60)
            if skip_rng: return sec

        # Cálculo / Cálculo
        if n % 2 == 0:
            nxt = n // 2
            op = f"{n}  par  -->  {n}  /  2  =  {nxt}"
        else:
            nxt = 3*n + 1
            op = f"{n}  impar  -->  3  x  {n}  +  1  =  {nxt}"

        draw_step(n, op, etiqueta)
        grabar_frame() 
        pygame.time.delay(delay_ms)
        n = nxt
        sec.append(n)

    draw_step(1, "Fin  |  Fim", etiqueta)
    grabar_frame() 
    pygame.time.delay(delay_ms)
    return sec

# ------------------ Lógica de rango / Lógica de intervalo ------------------

def procesa_par(i, j):
    """Analiza rango y visualiza / Analisa intervalo e visualiza"""
    global skip_rng
    skip_rng = False
    if i > j: i, j = j, i

    # Encontrar secuencia más larga / Encontrar sequência mais longa
    max_len, best = 0, i
    for a in range(i, j+1):
        t, cnt = a, 1
        while t != 1:
            t = t//2 if t%2==0 else 3*t+1
            cnt += 1
        if cnt > max_len:
            max_len, best = cnt, a

    etiqueta = f"{i} - {j} mejor | melhor: {best}"
    secuencias = []
    for a in range(i, j+1):
        sec = visualize_collatz(a, etiqueta)
        secuencias.append(sec)
        if skip_rng: break  # Salto solicitado / Pular solicitado

    # Mostrar lista breve / Mostrar lista breve
    screen.fill(COL_BG)
    y = 60
    header = FONT_MEDIUM.render(f"Rango | Intervalo {i} - {j}", True, COL_TEXT_INFO)
    screen.blit(header, (12, 8))
    for seq in secuencias:
        s = ' > '.join(map(str, seq))
        surf = FONT_SMALL_2.render(s, True, COL_TEXT_INFO)
        screen.blit(surf, (12, y))
        y += 50
        if y > H-60:
            pygame.display.flip()
            grabar_frame()
            for _ in range(3):
                grabar_frame()
                clock.tick(60)
            wait_key()
            screen.fill(COL_BG)
            y = 40
    pygame.display.flip()
    grabar_frame()
    wait_key()
    return max_len

# ------------------ Entrada por archivo / Entrada por ficheiro ------------------

pares = []
try:
    with open('entrada.txt', 'r') as f:
        for line in f:
            if line.strip():
                i, j = map(int, line.split())
                pares.append((i, j))
except FileNotFoundError:
    print("⚠  No se encontró entrada.txt / Não foi encontrado entrada.txt")
    pygame.quit(); sys.exit()

# ------------------ Ejecución principal / Execução principal ------------------


resultados = []
for i, j in pares:

    long_max = procesa_par(i, j)

    resultados.append((i, j, long_max))

# Resumen final / Resumo final
screen.fill(COL_BG)
y = 100
tit = FONT_BIG.render("RESULTADOS", True, COL_TEXT_INFO)
screen.blit(tit, (W//2 - tit.get_width()//2, 20))
for a, b, ln in resultados:
    txt = f"{a} - {b} ==>  Longitud | Comprimento máx = {ln}"
    surf = FONT_MEDIUM.render(txt, True, COL_TEXT_INFO)
    screen.blit(surf, (W//2 - surf.get_width()//2, y))
    y += 40
pygame.display.flip()

grabar_frame()          # ← ¡captura el cuadro de resumen!
# (opcional) manténlo 2 s en el vídeo:
for _ in range(3):
    grabar_frame()
    clock.tick(60)

wait_key()

# Vacía el búfer y cierra el archivo
for packet in stream.encode():
    output.mux(packet)
output.close()
pygame.quit()