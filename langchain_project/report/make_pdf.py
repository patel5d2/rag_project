"""Render report.md -> report.pdf.  Run from langchain_project/:  python report/make_pdf.py
Needs: pip install markdown xhtml2pdf"""
import markdown
from xhtml2pdf import pisa

md = open("report/report.md", encoding="utf-8").read().replace("../figure_comparison.png", "figure_comparison.png")
body = markdown.markdown(md, extensions=["tables"])
css = """@page{size:letter;margin:0.85in 0.8in}
body{font-family:Helvetica;font-size:10.5pt;line-height:1.4}
h1{font-size:17pt;margin-bottom:2pt} h2{font-size:13pt;margin-top:12pt;border-bottom:1px solid #999}
table{border:0.5px solid #888;margin:6pt 0} td,th{padding:3pt 4pt;font-size:8.5pt;border:0.5px solid #bbb}
th{background:#eee} code{font-family:Courier;font-size:8.5pt} img{width:6.9in}
blockquote{margin-left:12pt;color:#333;font-style:italic}"""
html = f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
with open("report/report.pdf", "wb") as f:
    assert not pisa.CreatePDF(html, dest=f, path=".").err
print("wrote report/report.pdf")
