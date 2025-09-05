from typing import Union

from fastapi import FastAPI, Response

from report.lib import add_suffix_key, year_stats
from report.template import DefaultTemplate

app = FastAPI()


@app.get("/")
def read_root():
    # actual = year_stats(0)
    # historic = add_suffix_key(year_stats(1), "_hist")
    # template = DefaultTemplate(**actual, **historic)
    # pdf_bytes = template.make_file()
    with open("report.pdf", "rb") as f:
        pdf_bytes = f.read()

    headers = {"Content-Disposition": "inline; filename=sample.pdf"}
    return Response(pdf_bytes, media_type="application/pdf", headers=headers)
