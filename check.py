from matplotlib.font_manager import FontManager
import subprocess

fm = FontManager()
mat_fonts = set(f.name for f in fm.ttflist)

output = subprocess.check_output('fc-list :lang=zh -f "%{family}\n"', shell=True)
output = output.decode('utf-8')
# print output
zh_fonts = set(f.split(',', 1)[0] for f in output.split('\n'))
available = mat_fonts & zh_fonts

for f in available:
    print(f)
