# Django-bureaucracy

Django-Bureaucracy is a small wrapper around the [bureacracy](https://bitbucket.org/maykinmedia/bureaucracy)
package that can be used to generate word and pdf documents from .docx-templates 
using Mailmerge fields.


## Installation:

```
pip install --process-dependency-links -e git+https://bitbucket.org/maykinmedia/django-bureaucracy.git#egg=django_bureaucracy-0.1
```

(Note that setuptools is annoying and that this doesn't work without the
`--process-dependency-links` flag which is deprecated. Have fun figuring out
how to do this when it's removed.)

... and then add `django_bureaucracy` to `INSTALLED_APPS`.

## Usage 

### Example


```python

from django_bureaucracy.models import Document

# The document model is used to store a template and render documents from a context:

doc = Document(
    template_file=File(open('sample.docx')),
    type='tps_report',
    validate_fields=True,
)

doc.save()


context = {
    'table': Table(data=[['this is the first cell of the first row', 'this is the second cell of the first row'],
                          ['the second row', 'etc'], 
                          ['etc', 'etc']], 
                   headers=['header 1', 'header 2']),
    'image': Image('pigeon.jpg')
    'html': HTML("<h1>This is a header from html. And the styling works! Right?</h1><p><strong>bold</strong>-notbold</p><ul><li>hop</li><li>la</li><li>kee</li></ul>")
    'text': 'some text',
}

# return bytes of the document generated from the template file and the context
doc_bytes = doc.render(context)  

# idem but for pdf bytes:
pdf_bytes = doc.render(context, format='pdf')


# save to a file:
doc.render_to_file(context, '/path/to/file') # docx
doc.render_to_file(context, '/path/to/file', format='pdf') # pdf
```


### Rendering to HTTPResponse with the correct mimetype.

```python

from django_bureaucracy.shortcuts import render_to_download

def view(request)

    # (...)

    resp = render_to_download(Document.objects.get(...), context, format='docx')
    # or... 
    resp = render_to_download(DocxTemplate(...), context, format='pdf')
    # or ... 
    resp = render_to_download(DocxTemplate('/path/to/file', context)
    # or ...
    resp = render_to_download(DocxTemplate(file_like_object, context)

    return resp

```


### Admin Integration

When the package is installed, `Document`-objects can be created in the 
admin. When the `validate_fields` box is checked, the model's `clean` method 
will check the `DOCX_TEMPLATE_VARS` setting to see whether the fields in
the template file and the document type match the ones provided in the setting and 
raise a `ValidationError` if this is not the case.


```python

# in settings.py

DOCX_TEMPLATE_VARS = {
    'tps_report': ['image', 'table', 'html', 'text'],
    'letter': ['graph']
}
```

