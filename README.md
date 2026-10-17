# Eagle Office

Türkçe, sade, **bilgisayarınızda çalışan** üç masaüstü uygulaması ve bunları tek pakette kuran kurulum betikleri.
Belgeleriniz hiçbir sunucuya gönderilmez; telemetri, hesap ve bulut yapay zekâ yoktur. **Developed By Usta ve Ata**

| Uygulama | Ne yapar | Depo |
|---|---|---|
| **Sözcük** | Türkçe kelime işlemci (yazım denetimi, sesle yazma, sesli okuma, çeviri) | [ataeyvaz/sozcuk](https://github.com/ataeyvaz/sozcuk) |
| **Tabcel** | Türkçe hesap tablosu | [ataeyvaz/tabcel](https://github.com/ataeyvaz/tabcel) |
| **EaglePDF** | Türkçe PDF görüntüleyici ve düzenleyici (OCR, dönüştürme, imza, filigran temizleme…) | [ataeyvaz/eaglepdf](https://github.com/ataeyvaz/eaglepdf) |

Üç uygulama bu depoya **git alt modülü** (submodule) olarak bağlıdır: `sozcuk/`, `tabcel/`, `eaglepdf/`. Her biri kendi deposunda, kendi sürümüyle ve kendi lisansıyla geliştirilir; bu depo yalnızca onları bir araya getirir.

## Kurulum paketi (akıllı kurulum)

`EagleOffice-<sürüm>-kurulum.exe` (Inno Setup, Türkçe sihirbaz) bilgisayarınızı denetler:

- Kurulu olmayan uygulamalar **kurulur**.
- Kurulu sürüm paketten **eskiyse güncellenir**.
- Kurulu sürüm paketle aynı ya da daha yeniyse **dokunulmaz** (örn. yalnızca Sözcük ve Tabcel kuruluysa yalnızca EaglePDF kurulur).
- Sürüm kaydı olmayan eski (1.1) kurulumlar varsayılan olarak korunur; isterseniz sihirbazda işaretleyip yeniden kurabilirsiniz.
- Hepsi kurulu ve güncelse "yapılacak bir şey yok" der.
- Sessiz kurulumda `/COMPONENTS=sozcuk,tabcel,eaglepdf` verilirse bu denetim atlanır, belirtilenler kurulur.

Kurulum dosyaları **Releases** bölümünden indirilir (depoya konmaz). İmzasız olduğu için ilk çalıştırmada Windows SmartScreen uyarısı çıkabilir: `kurulum/OKUBENI.txt` dosyasında adımlar var.

## Derleme (geliştirici)

Gereken: Windows, Python 3.11, [Inno Setup 6](https://jrsoftware.org/isinfo.php). Önce üç uygulamanın PyInstaller çıktısı hazır olmalı
(Sözcük ve Tabcel: `python -m PyInstaller <ad>.spec --noconfirm`; EaglePDF: `python yapi\paketle.py`).

```
git clone --recurse-submodules https://github.com/ataeyvaz/eagle-office.git
python kurulum\derle.py            # tam derleme  -> dist\EagleOffice-<sürüm>-kurulum.exe
python kurulum\derle.py --hizli    # sıkıştırmasız deneme derlemesi
```

`derle.py`, her uygulamanın sürümünü kendi `__version__` değerinden okur ve uygulamaları önce bu deponun alt modüllerinde, yoksa masaüstündeki kardeş klasörlerde (`..\sozcuk`, `..\tabcel`, `..\EaglePDF`) arar.
Alt modülleri güncel sürüme almak için: `git submodule update --remote`.

### Test

Kurulum mantığı gerçek Inno Setup ile derlenip sessiz kurulumlarla sınanır (sahte uygulama klasörleri, ayrı AppId ve geçici klasör; gerçek kurulumunuza dokunmaz, ~2 dk):

```
python -m pytest tests -q
```

## Klasörler

```
kurulum/        eagle-office.iss (Inno Setup betiği), derle.py, gorsel/, OKUBENI.txt
tests/          test_kurulum.py (akıllı kurulum senaryoları)
sozcuk/         alt modül → ataeyvaz/sozcuk
tabcel/         alt modül → ataeyvaz/tabcel
eaglepdf/       alt modül → ataeyvaz/eaglepdf
```

## Lisans

Bu depodaki kurulum betikleri, testler ve belgeler **GNU Affero Genel Kamu Lisansı v3 (AGPL-3.0)** altındadır: bkz. [`LICENSE`](LICENSE).

Üç uygulama bu depoya alt modül olarak bağlıdır ve **kendi lisanslarını korur**; lisansları kendi depolarındadır (EaglePDF: AGPL-3.0, PyMuPDF AGPL olduğu için). Kurulum paketi onları yalnızca bir araya getirir; her uygulamanın tam kaynak kodu kendi deposunda (ve burada alt modül olarak) herkese açıktır. Uygulamaların kullandığı açık kaynak bileşenlerin lisansları, her uygulamanın kendi `Hakkında` penceresinde ve depolarındaki lisans dosyalarında listelenir.

İletişim: ataeyvaz@gmail.com
