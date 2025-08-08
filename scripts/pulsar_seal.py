#!/usr/bin/env python3
import hashlib, json, os, datetime, pathlib

LOC_LONGITUDE_DEG = -93.2923
PULSAR_NAME = "PSR B1937+21"
PULSAR_PERIOD_S = 0.00155780644887275

root = pathlib.Path(".").resolve()

def files_to_hash():
    skip_dirs = {".git", ".github", "SEALS"}
    for p in root.rglob("*"):
        if p.is_file() and not (set(p.relative_to(root).parts) & skip_dirs):
            yield p

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()

now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
unix_ts = int(now.timestamp()); iso_utc = now.isoformat().replace("+00:00","Z")
JD = unix_ts/86400.0 + 2440587.5; MJD = JD - 2400000.5
T  = (JD - 2451545.0)/36525.0
gmst_sec = (67310.54841 + (876600.0*3600 + 8640184.812866)*T + 0.093104*(T**2) - 6.2e-6*(T**3)) % 86400.0
if gmst_sec < 0: gmst_sec += 86400.0
GMST_hours = gmst_sec/3600.0
LST_hours  = (GMST_hours + LOC_LONGITUDE_DEG/15.0) % 24.0
phase = ((now.timestamp() % PULSAR_PERIOD_S) / PULSAR_PERIOD_S) % 1.0

seal_dir = root / "SEALS"; seal_dir.mkdir(exist_ok=True)

manifest = seal_dir / f"sha256_manifest_{unix_ts}.txt"
with open(manifest, "w", encoding="utf-8") as mf:
    for f in sorted(files_to_hash()):
        rel = f.relative_to(root).as_posix()
        mf.write(f"{sha256sum(f)}  {rel}\n")

seal = {
  "actor": "Scott Alan Dygert",
  "scope": "Codex-Live-Portal / Public Seal",
  "utc_iso": iso_utc, "unix": unix_ts, "jd": JD, "mjd": MJD,
  "gmst_hours": GMST_hours, "lst_hours": LST_hours,
  "pulsar": {"name": PULSAR_NAME, "period_s": PULSAR_PERIOD_S, "phase_fraction": phase}
}
with open(seal_dir / f"seal_{unix_ts}.json", "w", encoding="utf-8") as sf:
    json.dump(seal, sf, indent=2, sort_keys=True)

print("Wrote:", manifest)
print("Wrote:", seal_dir / f"seal_{unix_ts}.json")
