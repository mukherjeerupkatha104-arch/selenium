"""Apply the wxPython 4.3 DirSelector keyword compatibility fix required by RIDE."""
from pathlib import Path
import robotide


target = Path(robotide.__file__).resolve().parent / "ui" / "mainframe.py"
source = target.read_text(encoding="utf-8")
old = "default_path=self.controller.default_dir"
new = "defaultPath=self.controller.default_dir"

if new in source:
    print("RIDE wxPython compatibility fix is already applied.")
elif old in source:
    target.write_text(source.replace(old, new), encoding="utf-8")
    print(f"Applied RIDE wxPython compatibility fix: {target}")
else:
    raise RuntimeError(f"Expected RIDE DirSelector call was not found: {target}")
