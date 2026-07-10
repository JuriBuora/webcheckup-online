# Bundled font

`LiberationSans-Regular.ttf`, `LiberationSans-Bold.ttf` and `LiberationSans-Italic.ttf` are the Liberation Sans font family (a metric-compatible Arial/Helvetica replacement with full Latin Extended-A coverage, including Polish, Romanian and Nordic diacritics), licensed under the SIL Open Font License 1.1.

`scripts/generate_report_pdf.py` embeds these fonts so generated PDFs render correctly regardless of what fonts happen to be installed on the machine running the script, and so accented characters (Polish `ń ś ć ł ź ż ą ę ó`, Nordic `å ä ö æ ø`, Romanian `ă â î ș ț`) don't fall back to the PDF base-14 fonts, which only support Western European (WinAnsi) accents and render everything else as garbled boxes.

Source: https://github.com/liberationfonts/liberation-fonts (SIL Open Font License 1.1 - free to embed and redistribute).
