from pathlib import Path
import re

path = Path("test_soog_corrigibility.py")

if not path.exists():
    raise SystemExit("PATCH FAILED: test_soog_corrigibility.py not found.")

text = path.read_text(encoding="utf-8")

new_func = '''def q_0_93(z: float) -> float:
    """Q(Z) = ε_min + (σ_max - ε_min) · Z / (1 + Z)

    Keeps σ in (0.07, 0.93), preserving:
      - lower truth signal above EPSILON_MIN
      - unknown gap ε = 1 - σ >= EPSILON_MIN
    """
    if z <= 0:
        z = 1e-9
    return EPSILON_MIN + (SIGMA_MAX - EPSILON_MIN) * (z / (1.0 + z))
'''

pattern = r'def q_0_93\(z: float\) -> float:\n.*?(?=\ndef evaluate_gate\()'

updated, count = re.subn(pattern, new_func + "\n", text, count=1, flags=re.DOTALL)

if count != 1:
    if "return EPSILON_MIN + (SIGMA_MAX - EPSILON_MIN)" in text:
        print("PATCH SKIP: q_0_93 already appears patched.")
    else:
        raise SystemExit("PATCH FAILED: could not locate q_0_93 block before evaluate_gate.")
else:
    path.write_text(updated, encoding="utf-8")
    print("PATCH OK: q_0_93 now preserves Truth Gap.")
