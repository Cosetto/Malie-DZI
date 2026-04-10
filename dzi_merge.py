import os
from PIL import Image

def stitch_dzi(dzi_path, texture_root, output_png):
    with open(dzi_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Parse metadata
    total_w, total_h = map(int, lines[1].split(','))
    
    # We target Level 0 (the first grid defined in the file)
    # Finding the line that defines Level 0 grid (usually line index 3)
    grid_dims = lines[3].split(',')
    cols, rows = int(grid_dims[0]), int(grid_dims[1])
    
    print(f"Detected Grid: {cols}x{rows} for resolution {total_w}x{total_h}")

    canvas = Image.new('RGBA', (total_w, total_h))
    tile_size = 256

    current_line = 4
    for r in range(rows):
        tiles_in_row = [t for t in lines[current_line].split(',')]
        for c, tile_ref in enumerate(tiles_in_row):
            rel_path = tile_ref.replace('\\', '/') + ".png" # or .webp
            full_path = os.path.join(texture_root, rel_path)
            
            if os.path.exists(full_path):
                tile = Image.open(full_path)
                # Paste at (col * 256, row * 256)
                canvas.paste(tile, (c * tile_size, r * tile_size))
        
        current_line += 1

    canvas.save(output_png)
    print(f"Successfully stitched into {output_png}")

stitch_dzi('select.dzi', './tex', 'akire.png')