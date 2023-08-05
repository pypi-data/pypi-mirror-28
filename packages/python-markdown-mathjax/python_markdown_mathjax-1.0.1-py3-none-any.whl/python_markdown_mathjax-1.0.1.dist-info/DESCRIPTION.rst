=====================================
MarkJax extension for Python-Markdown
=====================================
.. note::

    "\" is a escape character and use "\\" to show "\".

TeX or LaTeX
============
::

    ```markdown
    inline preprocess : \( E = mc^2 \)
    display preprocess: $$ E = mc^2 $$
    display preprocess: \[ E = mc^2 \]

    ```
html output::

    ```html
    <script type="math/tex">E = mc^2</script>
    <script type="math/tex; mode=display">E = mc^2</script>

    ```

.. note::

    "$" is USD unit, so ignore it.

AsciiMath
=========
::

    ```markdown
    preprocess: \` E = mc^2 \`

    ```

html output::

    ```html
    <script type="math/asciimath; mode=display">E = mc^2</script>
    ```


