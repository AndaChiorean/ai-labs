import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

WINDOW_W = 1000
WINDOW_H = 750
CUBE_SIZE = 2.0
GRID_N = 3

class Particle:
    def __init__(self, pos, vel, radius=0.02):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.radius = radius

def init_particles(n, speed_mult=1.0):
    particles = []
    for _ in range(n):
        pos = [random.uniform(0.05, CUBE_SIZE - 0.05) for _ in range(3)]
        vel = [random.uniform(-1, 1) * speed_mult for _ in range(3)]
        particles.append(Particle(pos, vel))
    return particles

def update_physics(particles, dt, speed_mult):
    for p in particles:
        p.pos += p.vel * dt * speed_mult

        for axis in range(3):
            if p.pos[axis] - p.radius < 0:
                p.pos[axis] = p.radius
                p.vel[axis] = abs(p.vel[axis])
            elif p.pos[axis] + p.radius > CUBE_SIZE:
                p.pos[axis] = CUBE_SIZE - p.radius
                p.vel[axis] = -abs(p.vel[axis])

    n = len(particles)
    if n < 300:
        for i in range(n):
            for j in range(i + 1, n):
                diff = particles[i].pos - particles[j].pos
                dist = np.linalg.norm(diff)
                min_dist = particles[i].radius + particles[j].radius
                if dist < min_dist and dist > 0:
                    normal = diff / dist
                    particles[i].vel, particles[j].vel = (
                        particles[i].vel - normal * np.dot(particles[i].vel - particles[j].vel, normal),
                        particles[j].vel - normal * np.dot(particles[j].vel - particles[i].vel, normal)
                    )
                    overlap = min_dist - dist
                    particles[i].pos += normal * overlap / 2
                    particles[j].pos -= normal * overlap / 2

def count_in_subcubes(particles, grid_n):
    counts = np.zeros((grid_n, grid_n, grid_n))
    cell_size = CUBE_SIZE / grid_n
    for p in particles:
        ix = min(int(p.pos[0] / cell_size), grid_n - 1)
        iy = min(int(p.pos[1] / cell_size), grid_n - 1)
        iz = min(int(p.pos[2] / cell_size), grid_n - 1)
        counts[ix][iy][iz] += 1
    return counts

def compute_shannon_entropy(particles, grid_n):
    counts = count_in_subcubes(particles, grid_n)
    total = len(particles)
    if total == 0:
        return 0.0
    entropy = 0.0
    for ix in range(grid_n):
        for iy in range(grid_n):
            for iz in range(grid_n):
                if counts[ix][iy][iz] > 0:
                    p = counts[ix][iy][iz] / total
                    entropy -= p * math.log2(p)
    return entropy

def compute_boltzmann_entropy(particles, grid_n):
    counts = count_in_subcubes(particles, grid_n)
    total = len(particles)
    if total == 0:
        return 0.0
    log_w = math.lgamma(total + 1)
    for ix in range(grid_n):
        for iy in range(grid_n):
            for iz in range(grid_n):
                log_w -= math.lgamma(int(counts[ix][iy][iz]) + 1)
    kb = 1.380649e-23
    return kb * log_w

def get_subcube_entropies(particles, grid_n):
    counts = count_in_subcubes(particles, grid_n)
    total = len(particles)
    entropies = np.zeros((grid_n, grid_n, grid_n))
    if total == 0:
        return entropies
    for ix in range(grid_n):
        for iy in range(grid_n):
            for iz in range(grid_n):
                n_in = int(counts[ix][iy][iz])
                n_out = total - n_in
                if n_in > 0 and n_out > 0:
                    p_in = n_in / total
                    p_out = n_out / total
                    entropies[ix][iy][iz] = -(p_in * math.log2(p_in) + p_out * math.log2(p_out))
                else:
                    entropies[ix][iy][iz] = 0.0
    return entropies

def entropy_to_color(val, max_val):
    if max_val == 0:
        return (0.0, 0.0, 1.0, 0.15)
    t = val / max_val
    r = t
    g = 1.0 - abs(2 * t - 1)
    b = 1.0 - t
    return (r, g, b, 0.12 + 0.15 * t)

def draw_cube_wireframe():
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1.5)
    glBegin(GL_LINES)
    edges = [
        (0,0,0),(CUBE_SIZE,0,0), (0,CUBE_SIZE,0),(CUBE_SIZE,CUBE_SIZE,0),
        (0,0,CUBE_SIZE),(CUBE_SIZE,0,CUBE_SIZE), (0,CUBE_SIZE,CUBE_SIZE),(CUBE_SIZE,CUBE_SIZE,CUBE_SIZE),
        (0,0,0),(0,CUBE_SIZE,0), (CUBE_SIZE,0,0),(CUBE_SIZE,CUBE_SIZE,0),
        (0,0,CUBE_SIZE),(0,CUBE_SIZE,CUBE_SIZE), (CUBE_SIZE,0,CUBE_SIZE),(CUBE_SIZE,CUBE_SIZE,CUBE_SIZE),
        (0,0,0),(0,0,CUBE_SIZE), (CUBE_SIZE,0,0),(CUBE_SIZE,0,CUBE_SIZE),
        (0,CUBE_SIZE,0),(0,CUBE_SIZE,CUBE_SIZE), (CUBE_SIZE,CUBE_SIZE,0),(CUBE_SIZE,CUBE_SIZE,CUBE_SIZE),
    ]
    for v in edges:
        glVertex3f(*v)
    glEnd()

def draw_subcubes(particles, grid_n):
    entropies = get_subcube_entropies(particles, grid_n)
    max_e = np.max(entropies) if np.max(entropies) > 0 else 1.0
    cell = CUBE_SIZE / grid_n

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)

    for ix in range(grid_n):
        for iy in range(grid_n):
            for iz in range(grid_n):
                color = entropy_to_color(entropies[ix][iy][iz], max_e)
                glColor4f(*color)
                x0, y0, z0 = ix * cell, iy * cell, iz * cell
                x1, y1, z1 = x0 + cell, y0 + cell, z0 + cell
                glBegin(GL_QUADS)
                # front
                glVertex3f(x0, y0, z1); glVertex3f(x1, y0, z1)
                glVertex3f(x1, y1, z1); glVertex3f(x0, y1, z1)
                # back
                glVertex3f(x0, y0, z0); glVertex3f(x0, y1, z0)
                glVertex3f(x1, y1, z0); glVertex3f(x1, y0, z0)
                # top
                glVertex3f(x0, y1, z0); glVertex3f(x0, y1, z1)
                glVertex3f(x1, y1, z1); glVertex3f(x1, y1, z0)
                # bottom
                glVertex3f(x0, y0, z0); glVertex3f(x1, y0, z0)
                glVertex3f(x1, y0, z1); glVertex3f(x0, y0, z1)
                # right
                glVertex3f(x1, y0, z0); glVertex3f(x1, y1, z0)
                glVertex3f(x1, y1, z1); glVertex3f(x1, y0, z1)
                # left
                glVertex3f(x0, y0, z0); glVertex3f(x0, y0, z1)
                glVertex3f(x0, y1, z1); glVertex3f(x0, y1, z0)
                glEnd()

    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)

def draw_grid_lines(grid_n):
    glColor4f(0.5, 0.5, 0.5, 0.3)
    glLineWidth(0.5)
    cell = CUBE_SIZE / grid_n
    glBegin(GL_LINES)
    for i in range(1, grid_n):
        c = i * cell
        for j in range(grid_n + 1):
            v = j * cell
            glVertex3f(c, 0, v); glVertex3f(c, CUBE_SIZE, v)
            glVertex3f(0, c, v); glVertex3f(CUBE_SIZE, c, v)
            glVertex3f(v, c, 0); glVertex3f(v, c, CUBE_SIZE)
    glEnd()

def draw_particles(particles):
    for p in particles:
        glPushMatrix()
        glTranslatef(*p.pos)

        speed = np.linalg.norm(p.vel)
        max_speed = 3.0
        t = min(speed / max_speed, 1.0)
        r = t
        g = 0.3
        b = 1.0 - t
        glColor3f(r, g, b)

        quad = gluNewQuadric()
        gluSphere(quad, p.radius, 8, 8)
        gluDeleteQuadric(quad)
        glPopMatrix()

def draw_entropy_chart(surface, entropy_history, max_entropy, chart_rect, font):
    pygame.draw.rect(surface, (20, 20, 30, 200), chart_rect)
    pygame.draw.rect(surface, (100, 100, 100), chart_rect, 1)

    if len(entropy_history) < 2:
        return

    draw_text_2d(surface, "Entropy over time", (chart_rect.x + 5, chart_rect.y - 16), font, (200, 200, 200))

    # max entropy reference line
    if max_entropy > 0:
        max_y = chart_rect.y + 5
        min_y = chart_rect.y + chart_rect.h - 5
        ref_y = int(min_y - (max_entropy / max_entropy) * (min_y - max_y))
        pygame.draw.line(surface, (100, 100, 100), (chart_rect.x, ref_y), (chart_rect.x + chart_rect.w, ref_y), 1)
        draw_text_2d(surface, f"max={max_entropy:.2f}", (chart_rect.x + chart_rect.w + 5, ref_y - 7), font, (150, 150, 150))

    # plot the entropy curve
    n = len(entropy_history)
    visible = min(n, 300)
    data = entropy_history[-visible:]

    y_min = 0
    y_max = max_entropy * 1.05 if max_entropy > 0 else 1.0
    x_start = chart_rect.x + 2
    x_end = chart_rect.x + chart_rect.w - 2
    y_top = chart_rect.y + 5
    y_bottom = chart_rect.y + chart_rect.h - 5

    points = []
    for i, val in enumerate(data):
        x = x_start + (i / max(len(data) - 1, 1)) * (x_end - x_start)
        y = y_bottom - ((val - y_min) / (y_max - y_min)) * (y_bottom - y_top)
        points.append((int(x), int(y)))

    if len(points) >= 2:
        pygame.draw.lines(surface, (50, 200, 50), False, points, 2)

    # current value label
    current = entropy_history[-1]
    ratio = current / max_entropy * 100 if max_entropy > 0 else 0
    draw_text_2d(surface, f"H={current:.3f} ({ratio:.1f}%)", (chart_rect.x + 5, chart_rect.y + chart_rect.h + 3), font, (50, 200, 50))


def save_entropy_plot(entropy_history, max_entropy):
    if len(entropy_history) < 10:
        return
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(entropy_history, color='green', linewidth=0.8, label='Shannon Entropy')
    ax.axhline(y=max_entropy, color='red', linestyle='--', linewidth=1, label=f'Maximum Entropy ({max_entropy:.4f})')
    ax.set_xlabel('Time Step (frame)')
    ax.set_ylabel('Shannon Entropy (bits)')
    ax.set_title('Entropy Evolution Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max_entropy * 1.15)
    plt.tight_layout()
    plt.savefig('entropy_evolution.png', dpi=150)
    plt.close()
    print(f"Saved entropy evolution plot ({len(entropy_history)} frames) to entropy_evolution.png")


def draw_text_2d(surface, text, pos, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, val, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = val
        self.label = label
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_val(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_val(event.pos[0])

    def _update_val(self, mx):
        t = (mx - self.rect.x) / self.rect.w
        t = max(0, min(1, t))
        self.val = self.min_val + t * (self.max_val - self.min_val)

    def draw(self, surface, font):
        pygame.draw.rect(surface, (60, 60, 60), self.rect)
        fill_w = int((self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.w)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.rect.h)
        pygame.draw.rect(surface, (80, 140, 210), fill_rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)

        if isinstance(self.val, float):
            txt = f"{self.label}: {self.val:.2f}"
        else:
            txt = f"{self.label}: {int(self.val)}"
        text_surf = font.render(txt, True, (255, 255, 255))
        surface.blit(text_surf, (self.rect.x + 5, self.rect.y + 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), DOUBLEBUF | OPENGL | pygame.RESIZABLE)
    pygame.display.set_caption("Particle Simulation - Entropy Visualization")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.05, 0.05, 0.1, 1.0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, WINDOW_W / WINDOW_H, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    font = pygame.font.SysFont("consolas", 14)

    num_particles = 200
    speed_mult = 1.0
    particles = init_particles(num_particles, speed_mult)

    slider_particles = Slider(20, WINDOW_H - 45, 300, 25, 10, 1000, num_particles, "Number of Particles")
    slider_speed = Slider(350, WINDOW_H - 45, 300, 25, 0.1, 5.0, speed_mult, "Temperature (Speed)")

    rot_x, rot_y = 25, -35
    mouse_down = False
    last_mouse = (0, 0)

    entropy_history = []
    chart_rect = pygame.Rect(WINDOW_W - 320, WINDOW_H - 170, 300, 100)

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        if dt > 0.05:
            dt = 0.05

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            slider_particles.handle_event(event)
            slider_speed.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if event.pos[1] < WINDOW_H - 60:
                    mouse_down = True
                    last_mouse = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_down = False
            elif event.type == pygame.MOUSEMOTION and mouse_down:
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                rot_y += dx * 0.5
                rot_x += dy * 0.5
                last_mouse = event.pos

        new_count = int(slider_particles.val)
        if new_count != len(particles):
            particles = init_particles(new_count, slider_speed.val)
            entropy_history.clear()
        speed_mult = slider_speed.val

        update_physics(particles, dt, speed_mult)

        shannon_e = compute_shannon_entropy(particles, GRID_N)
        boltzmann_e = compute_boltzmann_entropy(particles, GRID_N)
        max_shannon = math.log2(GRID_N ** 3)
        entropy_history.append(shannon_e)

        # 3D rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-CUBE_SIZE / 2, -CUBE_SIZE / 2, -7)
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        draw_subcubes(particles, GRID_N)
        draw_grid_lines(GRID_N)
        draw_cube_wireframe()
        draw_particles(particles)

        # 2D overlay
        overlay = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)

        slider_particles.draw(overlay, font)
        slider_speed.draw(overlay, font)

        info_texts = [
            f"Particles: {len(particles)}",
            f"Shannon Entropy: {shannon_e:.4f} / {max_shannon:.4f}",
            f"Boltzmann Entropy: {boltzmann_e:.4e}",
            f"Grid: {GRID_N}x{GRID_N}x{GRID_N}",
            f"FPS: {clock.get_fps():.0f}",
        ]
        for i, txt in enumerate(info_texts):
            draw_text_2d(overlay, txt, (10, 10 + i * 18), font)

        # color legend
        draw_text_2d(overlay, "Low entropy", (WINDOW_W - 160, 10), font, (100, 100, 255))
        draw_text_2d(overlay, "High entropy", (WINDOW_W - 160, 30), font, (255, 100, 100))

        # entropy evolution chart
        draw_entropy_chart(overlay, entropy_history, max_shannon, chart_rect, font)

        # blit 2D overlay onto OpenGL
        tex_data = pygame.image.tostring(overlay, "RGBA", True)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, WINDOW_W, 0, WINDOW_H, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glRasterPos2i(0, 0)
        glDrawPixels(WINDOW_W, WINDOW_H, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)

        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        pygame.display.flip()

    save_entropy_plot(entropy_history, max_shannon)
    pygame.quit()


if __name__ == "__main__":
    main()
