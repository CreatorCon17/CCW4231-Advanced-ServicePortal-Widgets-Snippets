"""YouTube thumbnail 1280x720 for the long video."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import snlib as S
from PIL import Image, ImageDraw, ImageFilter

S.W, S.H = 1280, 720
img = S._bg()
d = ImageDraw.Draw(img)
# glow
gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
ImageDraw.Draw(gl).ellipse([700, 120, 1300, 720], fill=S.AMBER + (70,))
img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(90)))
d = ImageDraw.Draw(img)
S.logo_badge(img, 40, 36, 330, pad=16)
d.text((48, 180), "30", font=S.font(250), fill=S.AMBER, stroke_width=8, stroke_fill=(0, 0, 0))
d.text((48, 450), "SERVICENOW", font=S.font(86), fill=S.WHITE, stroke_width=6, stroke_fill=(0, 0, 0))
d.text((48, 555), "BEST PRACTICES", font=S.font(86), fill=S.ACCENT, stroke_width=6, stroke_fill=(0, 0, 0))
# code sticker
S.code_card(img, (870, 120, 1250, 330), ["current.update();", "gr.getRowCount();"], 0, size=25, title="✗  STOP")
ImageDraw.Draw(img).rounded_rectangle([870, 120, 1250, 330], 28, outline=S.RED, width=6)
S.code_card(img, (870, 370, 1250, 560), ["setLimit(1);", "GlideAggregate"], 0, size=25, title="✓  DO")
ImageDraw.Draw(img).rounded_rectangle([870, 370, 1250, 560], 28, outline=S.ACCENT, width=6)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumbnail_30_best_practices.jpg")
img.convert("RGB").save(out, quality=92)
print(out)
