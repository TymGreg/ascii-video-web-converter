import math
import random

# Stan animacji
angle_sun = 0.0
angle_moon = 0.0
sun_moon_time = 0.0

donut_A = 0.0
donut_B = 0.0

matrix_drops = [random.randint(-30, 60) for _ in range(180)]
MATRIX_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*+<>"

plasma_time = 0.0

stars = [
    {
        "x": random.randint(10, 1140),
        "y": random.randint(10, 640),
        "char": random.choice(["+", ".", "*", "x", "·"]),
        "brightness": random.random()
    }
    for _ in range(90)
]

def draw_enhanced_sphere(ctx, cx, cy, radius, angle_y, base_col, light_dir, font_size, use_color, is_sun):
    global sun_moon_time
    lx, ly, lz = light_dir
    l_len = math.sqrt(lx*lx + ly*ly + lz*lz)
    lx, ly, lz = lx/l_len, ly/l_len, lz/l_len

    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    step_y = int(font_size * 0.85)
    step_x = int(font_size * 0.6)
    r_int = int(radius)
    chars = " .':;!*=#$@"

    for y in range(-r_int, r_int + 1, step_y):
        for x in range(-r_int, r_int + 1, step_x):
            d_sq = x*x + y*y
            if d_sq <= radius*radius:
                z = math.sqrt(radius*radius - d_sq)
                nx, ny, nz = x/radius, y/radius, z/radius

                rx = nx * cos_y + nz * sin_y
                ry = ny
                rz = -nx * sin_y + nz * cos_y

                diff = max(0.0, rx*lx + ry*ly + rz*lz)
                texture = math.sin(nx * 12.0 + sun_moon_time) * math.cos(ny * 12.0 - sun_moon_time)
                
                if is_sun:
                    diff = min(1.0, max(0.0, diff + texture * 0.15))
                else:
                    if texture > 0.4:
                        diff *= 0.75

                char_idx = int(diff * (len(chars) - 1))
                ch = chars[char_idx]

                if use_color:
                    if is_sun:
                        r = int(min(255, base_col[0] * (0.2 + 0.8 * diff) + (texture * 25)))
                        g = int(min(255, base_col[1] * (0.2 + 0.8 * diff) + (texture * 15)))
                        b = int(base_col[2] * (0.2 + 0.8 * diff))
                    else:
                        r = int(base_col[0] * (0.3 + 0.7 * diff) - (texture * 15))
                        g = int(base_col[1] * (0.3 + 0.7 * diff) - (texture * 15))
                        b = int(base_col[2] * (0.3 + 0.7 * diff) - (texture * 15))
                    ctx.fillStyle = f"rgb({max(0,r)},{max(0,g)},{max(0,b)})"
                else:
                    v = int(255 * diff)
                    ctx.fillStyle = f"rgb({v},{v},{v})"

                ctx.fillText(ch, cx + x, cy + y)

def render_sun_moon(ctx, W, H, font_size, use_color, chars):
    global angle_sun, angle_moon, sun_moon_time
    for s in stars:
        twinkle = math.sin(sun_moon_time * 3.0 + s["brightness"] * 10.0)
        alpha_char = s["char"] if twinkle > 0.0 else "."
        ctx.fillStyle = f"rgba(160, 180, 220, {max(0.2, (twinkle + 1.0) / 2.0)})" if use_color else "#718096"
        ctx.fillText(alpha_char, s["x"], s["y"])

    float_offset_sun = math.sin(sun_moon_time * 1.5) * 8.0
    float_offset_moon = math.cos(sun_moon_time * 1.5) * 8.0

    draw_enhanced_sphere(ctx, W * 0.3, H * 0.5 + float_offset_sun, 195, angle_sun, (255, 170, 30), (0.8, -0.4, 1.0), font_size, use_color, True)
    draw_enhanced_sphere(ctx, W * 0.7, H * 0.5 + float_offset_moon, 195, angle_moon, (100, 180, 255), (-0.8, -0.3, 0.9), font_size, use_color, False)

    angle_sun += 0.03
    angle_moon -= 0.02
    sun_moon_time += 0.04

def render_donut(ctx, W, H, font_size, use_color, chars):
    global donut_A, donut_B
    char_w = max(6, int(font_size * 0.62))
    char_h = font_size
    cols = W // char_w
    rows = H // char_h

    zbuffer = [0.0] * (cols * rows)
    output = [" "] * (cols * rows)
    colors = [(0, 0, 0)] * (cols * rows)

    cosA, sinA = math.cos(donut_A), math.sin(donut_A)
    cosB, sinB = math.cos(donut_B), math.sin(donut_B)

    theta = 0.0
    while theta < 6.28:
        costheta, sintheta = math.cos(theta), math.sin(theta)
        phi = 0.0
        while phi < 6.28:
            cosphi, sinphi = math.cos(phi), math.sin(phi)
            circlex = 2.0 + 1.0 * costheta
            circley = 1.0 * sintheta

            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = 5.0 + cosA * circlex * sinphi + circley * sinA
            ooz = 1.0 / z

            xp = int(cols / 2 + (cols * 0.38) * ooz * x)
            yp = int(rows / 2 - (rows * 0.55) * ooz * y)
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

            if L > 0 and 0 <= xp < cols and 0 <= yp < rows:
                idx = xp + yp * cols
                if ooz > zbuffer[idx]:
                    zbuffer[idx] = ooz
                    lum_idx = min(len(chars) - 1, int(L * 8))
                    output[idx] = chars[lum_idx]
                    r = int(128 + 127 * math.sin(theta))
                    g = int(128 + 127 * math.sin(phi))
                    b = int(200 + 55 * costheta)
                    factor = min(1.0, L / 1.4)
                    colors[idx] = (int(r * factor), int(g * factor), int(b * factor))
            phi += 0.09
        theta += 0.22

    txt_rows = []
    for r_idx in range(rows):
        row_chars = []
        pos_y = (r_idx + 1) * char_h
        for c_idx in range(cols):
            i = c_idx + r_idx * cols
            ch = output[i]
            row_chars.append(ch)
            if ch != " ":
                if use_color:
                    rc, gc, bc = colors[i]
                    ctx.fillStyle = f"rgb({rc},{gc},{bc})"
                else:
                    ctx.fillStyle = "#e2e8f0"
                ctx.fillText(ch, c_idx * char_w, pos_y)
        txt_rows.append("".join(row_chars))

    donut_A += 0.06
    donut_B += 0.04
    return "\n".join(txt_rows)

def render_matrix(ctx, W, H, font_size, use_color):
    char_w = max(6, int(font_size * 0.65))
    char_h = font_size
    cols = min(len(matrix_drops), W // char_w)
    rows = H // char_h

    for c in range(cols):
        head_y = matrix_drops[c]
        for tail in range(16):
            ry = head_y - tail
            if 0 <= ry < rows:
                ch = random.choice(MATRIX_CHARS)
                if tail == 0:
                    ctx.fillStyle = "#ffffff"
                else:
                    intensity = max(35, int(255 * (1 - tail / 16)))
                    if use_color:
                        ctx.fillStyle = f"rgb(0, {intensity}, 65)"
                    else:
                        ctx.fillStyle = f"rgb({intensity}, {intensity}, {intensity})"
                ctx.fillText(ch, c * char_w, (ry + 1) * char_h)

        matrix_drops[c] += 1
        if matrix_drops[c] - 16 > rows and random.random() > 0.92:
            matrix_drops[c] = random.randint(-15, 0)

def render_plasma(ctx, W, H, font_size, use_color, chars):
    global plasma_time
    char_w = max(6, int(font_size * 0.65))
    char_h = font_size
    cols = W // char_w
    rows = H // char_h

    txt_rows = []
    chars_max = len(chars) - 1

    for y in range(rows):
        row_chars = []
        pos_y = (y + 1) * char_h
        ny = y * 0.12
        for x in range(cols):
            nx = x * 0.08
            v = math.sin(nx + plasma_time) + math.sin(ny + plasma_time * 0.8) + math.sin((nx + ny + plasma_time) * 0.7)
            norm = (v + 3.0) / 6.0
            ch = chars[int(norm * chars_max)]
            row_chars.append(ch)

            if norm > 0.15:
                if use_color:
                    r = int(128 + 127 * math.sin(norm * 6.28 + plasma_time))
                    g = int(128 + 127 * math.sin(norm * 6.28 + 2.0))
                    b = int(128 + 127 * math.sin(norm * 6.28 + 4.0))
                    ctx.fillStyle = f"rgb({r},{g},{b})"
                else:
                    lum = int(norm * 255)
                    ctx.fillStyle = f"rgb({lum},{lum},{lum})"
                ctx.fillText(ch, x * char_w, pos_y)
        txt_rows.append("".join(row_chars))

    plasma_time += 0.08
    return "\n".join(txt_rows)
