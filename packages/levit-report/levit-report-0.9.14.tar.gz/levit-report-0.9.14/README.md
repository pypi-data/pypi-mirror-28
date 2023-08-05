# Levit-report

This library makes it easy to manage and render a set of relatorio-based reports in a Django application

## Installation

`pip install levit-report`

## Configuration

Add `levit_report` to your `INSTALLED_APPS`:

```
## settings.py

INSTALLED_APPS = (
    ...
    'levit_report',
)
```

Import the built-in urls into your `urls.py`

```
## urls.py

...
from levit_report import urls as report_urls

...
urlpattern = [
    ...
    url(r'^reports/', include(report_urls)),
]
```

## Usage

Before being able to use this package you will first have to create a
[Relatorio](http://relatorio.readthedocs.io/en/latest/index.html) template. The "object"
of the report will be available inside the report as `o` (as in object).

Once you have created your templte, go to the admin and add a new `Document` (in the 
`Levit_Report` section).

![admin screenshot](./docs/document-admin.png)

You'll then be able to upload your relatorio template and associate it with a ContentType.

In order to use the "convert to" feature, you'll need you have LibreOffice headless installed.

:warning: LibreOffice headless fails silently when a regular LibreOffice window is open on
the same machine.

In order to use the "Merge with tos" feature (only available for pdf's), you'll need:

- to have pdfunite installed
- have given the full path to a pdf `TOS_FILE` in your `settings.py` like this

```
## settings.py

TOS_FILE = os.path.join(BASE_DIR, 'documents', 'tos.pdf')
```

Once this is done, you'll be able to download a rendered version of your report at
http://localhost:8000/reports/&lt;document_slug&gt;/&lt;target_object_id&gt;/

You'll also be able to download a ip containing several rendered reports by pointing
your browser at
http://localhost:8000/reports/&lt;document_slug&gt;/?ids[]=&lt;target_object_id&gt;&ids[]=&lt;target_object_2_id&gt;...


This project is licensed under the [MIT License](http://opensource.org/licenses/MIT)
