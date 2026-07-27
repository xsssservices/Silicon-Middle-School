from pathlib import Path
import re

root = Path(r"c:\Users\shell\OneDrive\Documents\Bubbles Assignment")
order = [
    "index.html",
    "tableofcontents.html",
    "eventoverview.html",
    "smartgoals.html",
    "needsassessment.html",
    "brainstorm.html",
    "actionplan.html",
    "equityinclusion.html",
    "exitsurvey.html",
    "reflection.html",
]
nav_css = '''    .next-btn,
    .nav-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 10px 18px;
      background: linear-gradient(135deg, #1f5f3d, #2e8b57);
      color: #fff;
      text-decoration: none;
      border-radius: 999px;
      font-size: 14px;
      font-weight: 600;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .next-btn:hover,
    .nav-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.16);
      background: linear-gradient(135deg, #2e8b57, #1f5f3d);
    }
    .page-nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 32px;
      gap: 12px;
    }
    .nav-back {
      background: linear-gradient(135deg, #5b6c7d, #6f8294);
    }
    .nav-back:hover {
      background: linear-gradient(135deg, #6f8294, #5b6c7d);
    }
    .page-nav span {
      flex: 1;
    }
'''

nav_pattern = re.compile(r'<div class="page-nav">.*?</div>', re.DOTALL)
style_rule_pattern = re.compile(r'(?ms)^\s*(?:\.next-btn(?:,\s*\.nav-btn)?|\.next-btn:hover|\.nav-btn|\.nav-btn:hover|\.nav-back|\.nav-back:hover|\.page-nav|\.page-nav span)\s*\{.*?^\s*\}\s*')

for name in order:
    path = root / name
    if not path.exists():
        print(f"MISSING {name}")
        continue
    text = path.read_text(encoding='utf-8')
    if '</style>' in text:
        text = text.replace('</style>', nav_css + '</style>', 1)

    text = nav_pattern.sub('', text)
    text = style_rule_pattern.sub('', text)

    idx = order.index(name)
    prev_page = order[idx - 1] if idx > 0 else None
    next_page = order[idx + 1] if idx < len(order) - 1 else None

    if name == 'index.html':
        nav = '<div class="page-nav"><span></span><a class="nav-btn nav-next" href="tableofcontents.html">Next</a></div>'
    elif name == 'tableofcontents.html':
        nav = '<div class="page-nav"><a class="nav-btn nav-back" href="index.html">Back</a><a class="nav-btn nav-next" href="eventoverview.html">Next</a></div>'
    elif next_page:
        nav = f'<div class="page-nav"><a class="nav-btn nav-back" href="{prev_page}">Back</a><a class="nav-btn nav-next" href="{next_page}">Next</a></div>'
    else:
        nav = f'<div class="page-nav"><a class="nav-btn nav-back" href="{prev_page}">Back</a><span></span></div>'

    if '</div>\n  </div>\n</body>' in text:
        text = text.replace('</div>\n  </div>\n</body>', f'{nav}\n    </div>\n  </div>\n</body>', 1)
    elif '</div>\n</body>' in text:
        text = text.replace('</div>\n</body>', f'{nav}\n</body>', 1)

    path.write_text(text, encoding='utf-8')
    print(f'Updated {name}')
