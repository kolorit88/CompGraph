import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans
import webcolors
from DMC_COLORS import DMC_COLORS

def load_image(image_path, max_size):
    img = Image.open(image_path)
    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return np.array(img)


def quantize_colors(image, num_colors):
    pixels = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors, random_state=0, n_init=10)
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_.astype(int)
    return centers[labels].reshape(image.shape), centers


def find_nearest_dmc(color):
    min_dist = float('inf')
    nearest_dmc = None
    for name, dmc_color in DMC_COLORS.items():
        dist = np.linalg.norm(np.array(color) - np.array(dmc_color))
        if dist < min_dist:
            min_dist = dist
            nearest_dmc = (name, dmc_color)
    return nearest_dmc


def create_pattern(image_array, color_centers):
    pattern = []
    color_map = {}
    for center in color_centers:
        dmc_name, dmc_color = find_nearest_dmc(center)
        color_map[tuple(center)] = (dmc_name, dmc_color)

    for row in image_array:
        pattern_row = []
        for pixel in row:
            dmc_name, dmc_color = color_map[tuple(pixel)]
            pattern_row.append(dmc_name)
        pattern.append(pattern_row)
    return pattern, color_map


def draw_pattern(pattern, color_info, cell_size=20):
    rows = len(pattern)
    cols = len(pattern[0])

    img_width = cols * cell_size + 100
    img_height = rows * cell_size + 100
    img = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()

    for i in range(rows):
        for j in range(cols):
            color_name = pattern[i][j]
            color_rgb = DMC_COLORS[color_name]
            x0 = j * cell_size + 50
            y0 = i * cell_size + 50
            draw.rectangle([x0, y0, x0 + cell_size, y0 + cell_size], fill=color_rgb, outline='black')

            symbol = chr(65 + list(DMC_COLORS.keys()).index(color_name) % 58)
            draw.text((x0 + cell_size // 3, y0 + cell_size // 3), symbol, fill='black', font=font)

    for i in range(0, cols + 1, 10):
        x = i * cell_size + 50
        draw.line([x, 50, x, rows * cell_size + 50], fill='red', width=2)
    for i in range(0, rows + 1, 10):
        y = i * cell_size + 50
        draw.line([50, y, cols * cell_size + 50, y], fill='red', width=2)

    legend_x = cols * cell_size + 60
    legend_y = 50
    for i, (color_name, color_rgb) in enumerate(DMC_COLORS.items()):
        if color_name in [c for row in pattern for c in row]:
            draw.rectangle([legend_x, legend_y, legend_x + 20, legend_y + 20], fill=color_rgb, outline='black')
            symbol = chr(65 + list(DMC_COLORS.keys()).index(color_name) % 58)
            draw.text((legend_x + 25, legend_y + 5), f"{symbol} - {color_name}", fill='black', font=font)
            legend_y += 25

    return img


def main(image_path, max_colors, max_size):
    image = load_image(image_path, max_size)
    quantized, centers = quantize_colors(image, max_colors)
    pattern, color_map = create_pattern(quantized, centers)
    result_image = draw_pattern(pattern, color_map)
    result_image.save('cross_stitch_pattern.png')
    print("Схема сохранена в cross_stitch_pattern.png")


if __name__ == "__main__":
    main("images/pic.jpg", 10, 200)