# DeuChi

- Ein Echtzeit-Tool, Deutsch zu übersetzen
- 一个翻译德（英）语的实时工具
- Reason
  - Es gitb keinen Untertitel für Deutsch-Videos. Die meinsten Videos zeigen nur Untertitel in einer Sprache. Das ärgert mich.
  - There are no subtitles for German videos. Most videos only show subtitles in one language. That annoys me.
- How
  - pyauotogui bekommt das Bild
  - cv2 konvertiert das Bild zu cv2.COLOR_BGRA2GRAY
  - pytesseract erkennt den Untertitel
  - googletrans übersetzt den Untertitel ins Chinesische
- Based on
  - pyauotogui
  - cv2
  - pytesseract
  - googletrans
