import os
import math
from PIL import Image

def split_png(input_path, asset_name, texture_root, output_format="WEBP"):
    img = Image.open(input_path).convert("RGBA")
    base_w, base_h = img.size
    tile_size = 256
    
    output_format = output_format.upper()
    ext = "webp" if output_format == "WEBP" else "png"

    # Header
    dzi_lines = ["DZI", f"{base_w},{base_h}", "3"] 

    for level in range(3):
        scale = 1 / (2**level)
        w, h = int(base_w * scale), int(base_h * scale)
        
        level_img = img.resize((w, h), Image.LANCZOS) if level > 0 else img
        
        cols = math.ceil(w / tile_size)
        rows = math.ceil(h / tile_size)
        
        dzi_lines.append(f"{cols},{rows}")
        
        level_dir = os.path.join(texture_root, asset_name, str(level))
        os.makedirs(level_dir, exist_ok=True)

        for r in range(rows):
            row_slots = []
            for c in range(cols):
                left, top = c * tile_size, r * tile_size
                tile = level_img.crop((left, top, left + tile_size, top + tile_size))
                
                # Check if tile has any visible pixels
                alpha_extrema = tile.getchannel('A').getextrema()
                
                # If tile is NOT empty (alpha max > 0)
                if alpha_extrema and alpha_extrema[1] > 0:
                    tile_idx = f"{r * cols + c:02d}" 
                    tile_filename = f"{tile_idx}.{ext}"
                    save_path = os.path.join(level_dir, tile_filename)

                    if output_format == "WEBP":
                        tile.save(
                            save_path, 
                            "WEBP", 
                            lossless=False, 
                            quality=92, 
                            method=6, 
                            exact=True
                        )
                    else:
                        tile.save(
                            save_path, 
                            "PNG", 
                            optimize=True
                        )
                    
                    row_slots.append(f"{asset_name}\\{level}\\{tile_idx}")
                else:
                    row_slots.append("")
            
            dzi_lines.append(",".join(row_slots))

    with open(f"{asset_name}.dzi", "w") as f:
        f.write("\n".join(dzi_lines))
        
    print(f"Split complete ({output_format}). File: {asset_name}.dzi")

if __name__ == "__main__":
    split_png('select.png', 'up_o', './tex', output_format="PNG")