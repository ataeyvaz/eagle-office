"""Eagle Office kurulum paketini derler (Inno Setup). Sürümleri üç uygulamanın `__version__` değerinden okur.

Kullanım (depo kökünden):
    python kurulum\\derle.py            tam derleme (lzma2/max; dist\\EagleOffice-<sürüm>-kurulum.exe)
    python kurulum\\derle.py --hizli    sıkıştırmasız deneme derlemesi
    python kurulum\\derle.py --test --sozcuk-dist D --tabcel-dist D --eaglepdf-dist D --cikis D
        ayrı AppId/kayıt anahtarıyla (gerçek kurulumu ezmez) ve verilen sahte klasörlerle derleme (testler kullanır)

Uygulamalar şu sırayla aranır: bu deponun alt modülleri (`sozcuk/`, `tabcel/`, `eaglepdf/`), yoksa masaüstündeki kardeş klasörler
(`..\\sozcuk`, `..\\tabcel`, `..\\EaglePDF`). Her uygulamanın PyInstaller çıktısı (`dist\\...`) ÖNCEDEN derlenmiş olmalıdır:
Sözcük ve Tabcel için `python -m PyInstaller <ad>.spec --noconfirm`, EaglePDF için `python yapi\\paketle.py`.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

KLASOR = Path(__file__).resolve().parent
DEPO = KLASOR.parent
MASAUSTU = DEPO.parent
ISCC_ADAYLARI = (r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe", r"C:\Program Files\Inno Setup 6\ISCC.exe")

# anahtar: (depo klasör adı, python paketi, PyInstaller çıktı klasörü adı, exe)
UYGULAMALAR = {
    "Sozcuk": ("sozcuk", "sozcuk", "Sozcuk", "Sozcuk.exe"),
    "Tabcel": ("tabcel", "tabcel", "Tabcel", "Tabcel.exe"),
    "EaglePdf": ("eaglepdf", "eaglepdf", "EaglePDF", "EaglePDF.exe"),
}


def uygulama_klasoru(anahtar: str) -> Path:
    """Alt modül ya da kardeş klasör: önce derlenmiş çıktısı (exe) olan, yoksa kaynağı olan, yoksa kardeş klasör."""
    klasor, paket, dist, exe = UYGULAMALAR[anahtar]
    adaylar = [DEPO / klasor, MASAUSTU / klasor]
    for a in adaylar:
        if (a / "dist" / dist / exe).exists():
            return a
    for a in adaylar:
        if (a / paket / "__init__.py").exists():
            return a
    return adaylar[1]


def surum_oku(yol: Path) -> str:
    m = re.search(r'^__version__\s*=\s*"([^"]+)"', yol.read_text(encoding="utf-8"), re.M)
    if not m:
        raise SystemExit(f"Sürüm bulunamadı: {yol}")
    return m.group(1)


def iscc_bul() -> str:
    for a in ISCC_ADAYLARI:
        if Path(a).exists():
            return a
    raise SystemExit("Inno Setup 6 bulunamadı (winget install JRSoftware.InnoSetup).")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hizli", action="store_true", help="sıkıştırmasız deneme derlemesi")
    ap.add_argument("--test", action="store_true", help="ayrı AppId ve kayıt anahtarı (/DTEST=1)")
    ap.add_argument("--suite-surum", default="1.2", help="paket (Eagle Office) sürümü")
    ap.add_argument("--sozcuk-dist")
    ap.add_argument("--tabcel-dist")
    ap.add_argument("--eaglepdf-dist")
    ap.add_argument("--sozcuk-surum")
    ap.add_argument("--tabcel-surum")
    ap.add_argument("--eaglepdf-surum")
    ap.add_argument("--cikis", help="çıktı klasörü (varsayılan: depo\\dist)")
    a = ap.parse_args()

    verilen_dist = {"Sozcuk": a.sozcuk_dist, "Tabcel": a.tabcel_dist, "EaglePdf": a.eaglepdf_dist}
    verilen_surum = {"Sozcuk": a.sozcuk_surum, "Tabcel": a.tabcel_surum, "EaglePdf": a.eaglepdf_surum}
    dist, surum = {}, {}
    for ad, (klasor, paket, dist_ad, exe) in UYGULAMALAR.items():
        kok = uygulama_klasoru(ad)
        dist[ad] = Path(verilen_dist[ad]) if verilen_dist[ad] else kok / "dist" / dist_ad
        if not (dist[ad] / exe).exists():
            raise SystemExit(f"{ad} paketi yok: {dist[ad] / exe} (önce PyInstaller derlemesi)")
        surum[ad] = verilen_surum[ad] or surum_oku(kok / paket / "__init__.py")
    komut = [iscc_bul(), f"/DSuiteVersion={a.suite_surum}"]
    for ad in dist:
        komut += [f"/D{ad}Version={surum[ad]}", f"/D{ad}Dist={dist[ad]}"]
    if a.hizli:
        komut.append("/DHIZLI=1")
    if a.test:
        komut.append("/DTEST=1")
    komut.append(f"/DCikisKlasoru={a.cikis or (DEPO / 'dist')}")
    komut.append(str(KLASOR / "eagle-office.iss"))
    print("Sürümler:", ", ".join(f"{k} {v}" for k, v in surum.items()), "· paket", a.suite_surum)
    return subprocess.call(komut)


if __name__ == "__main__":
    sys.exit(main())
