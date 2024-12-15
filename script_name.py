import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Parametrlər
planet_data = [
    {"name": "Yer", "radius": 1.0, "speed": 1.0, "color": "blue", "orbit_radius": 1.0, "orbit_color": "lightblue"},
    {"name": "Yupiter", "radius": 0.5, "speed": 0.0843, "color": "red", "orbit_radius": 5.2, "orbit_color": "orange"},
    {"name": "Saturn", "radius": 0.4, "speed": 0.033, "color": "gold", "orbit_radius": 9.5, "orbit_color": "yellow"},
    {"name": "Mars", "radius": 0.3, "speed": 1.5, "color": "orange", "orbit_radius": 1.52, "orbit_color": "brown"}
]

steps = 5000  # Addımların sayı
x_coords = []
y_coords = []
is_animating = True  # Animasiya vəziyyəti

# Günəşi əlavə etmək
def draw_sun(ax):
    """Günəşi təsvir edir."""
    ax.scatter(0, 0, color="yellow", s=500, label="Günəş", zorder=5)

# Hər bir planetin mövqeyini hesablamaq
def calculate_position(planet, t):
    """Verilən planetin zamanın t mövqeyini hesablamaq."""
    x = planet['orbit_radius'] * np.cos(planet['speed'] * t)
    y = planet['orbit_radius'] * np.sin(planet['speed'] * t)
    return x, y

# Planetlərin orbitini çəkmək
def draw_orbit(ax, planet):
    """Orbitin rəngini çəkmək."""
    theta = np.linspace(0, 2 * np.pi, 100)
    x = planet['orbit_radius'] * np.cos(theta)
    y = planet['orbit_radius'] * np.sin(theta)
    ax.plot(x, y, color=planet['orbit_color'], linestyle="--", alpha=0.6, zorder=1)

# Planetlərin əlavə edilməsi
def add_planets(ax, t):
    """Planetləri əlavə edir."""
    for planet in planet_data:
        x, y = calculate_position(planet, t)
        ax.plot(x, y, 'o', color=planet['color'], label=planet['name'], zorder=4)

# Orbitin keçmiş trajektoriyasını göstərmək
def show_past_trajectory(x_coords, y_coords, ax):
    """Keçmiş trajektoriyanı göstərir."""
    ax.plot(x_coords, y_coords, color="gray", linewidth=0.5, alpha=0.2, zorder=3)

# Orbitin sürətini dinamik olaraq dəyişdirmək
def update_speed(frame, base_speed=1.0):
    """Animasiya sürətini zamanla dəyişdirir."""
    return base_speed * (1 + np.sin(frame / 10))

# Etiketləri əlavə etmək
def add_labels(ax, x, y, planet_name):
    """Planetin adını göstərmək üçün etiket əlavə edir."""
    ax.text(x, y, planet_name, color="white", fontsize=10, ha='center', zorder=6)

# Qalaktika və ulduzları əlavə etmək (yanıb-sönən ulduzlar)
def add_galaxy_and_stars(ax):
    """Qalaktika və ulduzları təsvir edir."""
    for _ in range(100):
        star_x = random.uniform(-15, 15)
        star_y = random.uniform(-15, 15)
        alpha = random.uniform(0.2, 1.0)
        ax.scatter(star_x, star_y, color="white", s=random.uniform(5, 20), alpha=alpha, zorder=2)

# Keçmiş orbitlərin yaddaşa alınması
def store_trajectory(x, y):
    """Trajektoriyanı yaddaşa alır."""
    x_coords.append(x)
    y_coords.append(y)

# Zaman göstəricisi
def add_time_display(ax, time):
    """Animasiya zamanı üçün zaman göstəricisi əlavə edir."""
    ax.text(0.5, 1.05, f"Zaman: {time:.2f} il", ha='center', va='bottom', color='white', fontsize=12, zorder=7)

# Orbit animasiyası
def animate_orbit(frame):
    """Orbitin animasiyasını təmin edir."""
    ax.clear()
    ax.set_facecolor('black')
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)

    # Qalaktika və ulduzları əlavə etmək
    add_galaxy_and_stars(ax)

    # Günəşin əlavə edilməsi
    draw_sun(ax)

    # Keçmiş orbitləri göstərmək
    show_past_trajectory(x_coords, y_coords, ax)

    # Planetləri əlavə etmək və hər planetin orbitini çəkmək
    for planet in planet_data:
        x, y = calculate_position(planet, frame)
        store_trajectory(x, y)
        draw_orbit(ax, planet)
        add_planets(ax, frame)

    # Etiketləri əlavə etmək
    for planet in planet_data:
        x, y = calculate_position(planet, frame)
        add_labels(ax, x, y, planet['name'])

    # Zamanın göstəricisini əlavə edirik
    add_time_display(ax, frame)

    # Orbitin cari vəziyyəti
    ax.set_title("Günəş Sistemi Simulyasiyası", fontsize=18, color="yellow")
    ax.set_xlabel("X Oxu")
    ax.set_ylabel("Y Oxu")
    ax.legend(loc="upper right")

    ax.grid(True, color='gray', linestyle='--', linewidth=0.2, alpha=0.5)

# Animasiya dayandırma və başlatma funksiyası
def toggle_animation(event):
    global is_animating
    is_animating = not is_animating

# Şəkil yaradılması
fig, ax = plt.subplots(figsize=(10, 10), dpi=100)

# Dəyişiklik üçün düymələr əlavə etmək
fig.canvas.mpl_connect('key_press_event', toggle_animation)

# Animasiya yaradılması
ani = FuncAnimation(fig, animate_orbit, frames=steps, interval=50, repeat=False)

# Görüntüləmək
plt.show()

# Animasiya dayandırıldıqdan sonra şəkil və koordinatları yadda saxlamaq
if not is_animating:
    ani.save("solar_system_simulation.png", dpi=300)
    with open("orbit_coordinates.txt", "w") as file:
        for planet in planet_data:
            for i, (x, y) in enumerate(zip(x_coords, y_coords)):
                file.write(f"{planet['name']} - {x:.2f}, {y:.2f}, Step: {i}\n")
