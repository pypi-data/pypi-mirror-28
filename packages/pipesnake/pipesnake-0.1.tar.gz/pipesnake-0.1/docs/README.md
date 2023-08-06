# To Generate Sphinx Docs for `pipesnake`

Run `sphinx-apidoc -o source ../pipesnake`.

This will generate `modules.rst` and the other `pipesnake.rst`.

Then include `modules.rst` in your `index.rst` file.

Then run `make html`.
