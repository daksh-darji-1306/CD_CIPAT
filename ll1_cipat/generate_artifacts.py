import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def create_image(text, filename):
    lines = text.split('\n')
    # Use a generic font (Pillow's default) or ImageFont.load_default()
    font = ImageFont.load_default()
    # Or load a monospace font if available, but for simplicity we can just use default
    # To get better rendering we can try to use a truetype font if available on windows
    try:
        font = ImageFont.truetype("consola.ttf", 16)
    except:
        pass
    
    # Calculate image size
    # Rough estimation if textbbox not perfect
    line_height = 20
    try:
        _, _, _, line_height = font.getbbox("A")
    except:
        pass
        
    img_height = len(lines) * line_height + 40
    # Find max width
    max_width = 100
    for line in lines:
        try:
            _, _, w, _ = font.getbbox(line)
        except:
            w = len(line) * 10
        if w > max_width:
            max_width = w
            
    img_width = max_width + 40
    
    img = Image.new('RGB', (img_width, img_height), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    
    y = 20
    for line in lines:
        d.text((20, y), line, font=font, fill=(200, 200, 200))
        y += line_height
        
    img.save(filename)

def run_cmd(cmd, outfile=None):
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    out = res.stdout
    if outfile:
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(out)
    return out

def main():
    tables_out = run_cmd([sys.executable, "ll1.py", "tables"], "output_tables.txt")
    create_image(tables_out, "shot_tables.png")
    
    accept_out = run_cmd([sys.executable, "ll1.py", "id+id*id"], "output_accept.txt")
    create_image(accept_out, "shot_accept.png")
    
    reject_out = run_cmd([sys.executable, "ll1.py", "id+*id"], "output_reject.txt")
    create_image(reject_out, "shot_reject.png")
    
    # Also test Gate 1 conditions
    test1 = run_cmd([sys.executable, "ll1.py", "(id+id)*id"])
    print("Test 1 ((id+id)*id):")
    print(test1)
    
    test2 = run_cmd([sys.executable, "ll1.py", "id id"])
    print("Test 2 (id id):")
    print(test2)

if __name__ == "__main__":
    main()
