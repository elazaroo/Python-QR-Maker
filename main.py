from PIL import Image, ImageDraw

def draw_finder_pattern(draw, top_left, module_size):
    x, y = top_left
    size = 7 * module_size
    # Outer square
    draw.rectangle([x, y, x + size -1, y + size -1], fill='black')
    # White square
    offset = module_size
    draw.rectangle([x + offset, y + offset, x + size - offset -1, y + size - offset -1], fill='white')
    # Black square
    inner_offset = 2 * module_size
    draw.rectangle([x + inner_offset, y + inner_offset, x + size - inner_offset -1, y + size - inner_offset -1], fill='black')

def determine_qr_parameters(url_length):
    if url_length <= 25:
        version = 1
        module_size = 10
    elif url_length <= 50:
        version = 2
        module_size = 8
    elif url_length <= 75:
        version = 3
        module_size = 7
    else:
        version = 4
        module_size = 6
    return version, module_size

def draw_alignment_pattern(draw, center, module_size):
    size = 5 * module_size
    x, y = center
    top_left = (x - 2 * module_size, y - 2 * module_size)
    bottom_right = (x + 2 * module_size, y + 2 * module_size)
    # Outer square
    draw.rectangle([top_left, bottom_right], fill='black')
    # Inner white square
    offset = module_size
    draw.rectangle([x - offset, y - offset, x + offset, y + offset], fill='white')
    # Center black square
    center_offset = module_size // 2
    draw.rectangle([x - center_offset, y - center_offset, x + center_offset, y + center_offset], fill='black')

def get_alignment_positions(version):
    if version == 1:
        return []
    # Alignment pattern locations for versions 2 to 4
    alignment_patterns = {
        2: [6, 18],
        3: [6, 22],
        4: [6, 26],
    }
    return alignment_patterns.get(version, [])

def create_qr_skeleton(version, module_size=10, output='qr_skeleton.png'):
    grid_size = 21 + (version -1)*4
    img_size = grid_size * module_size
    image = Image.new('RGB', (img_size, img_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw finder patterns
    positions = [(0,0), (img_size - 7*module_size,0), (0, img_size -7*module_size)]
    for pos in positions:
        draw_finder_pattern(draw, pos, module_size)
    
    # Draw alignment patterns
    alignment_centers = get_alignment_positions(version)
    for x in alignment_centers:
        for y in alignment_centers:
            # Skip the finder pattern areas
            if (x == 6 and y == 6) or (x == 6 and y == grid_size - 7) or (x == grid_size - 7 and y == 6):
                continue
            center = (x * module_size, y * module_size)
            draw_alignment_pattern(draw, center, module_size)
    
    image.save(output)

if __name__ == "__main__":
    url = input("Enter URL: ")
    version, size = determine_qr_parameters(len(url))
    create_qr_skeleton(version, size)
    print("QR skeleton generated as qr_skeleton.png")