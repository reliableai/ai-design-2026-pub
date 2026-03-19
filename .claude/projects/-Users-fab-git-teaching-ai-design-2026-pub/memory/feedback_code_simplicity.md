---
name: Code simplicity — no chained operations
description: Never chain file reads with constructors. Load file content into a variable first, then pass it to Template/etc.
type: feedback
---

Never chain file I/O with object construction. Always load file content into a named variable first, then use it.

**Why:** The user finds chained patterns like `Template(Path("x.j2").read_text())` hard to read and debug. Each step should be visible.

**How to apply:** Whenever loading a file and using its content (templates, configs, etc.):
```python
# GOOD
prompt_text = Path("prompt_templates/tool_diy.j2").read_text()
template = Template(prompt_text)

# BAD
template = Template(Path("prompt_templates/tool_diy.j2").read_text())
```
