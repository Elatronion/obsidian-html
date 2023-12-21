# Obsidian to HTML converter

This is a short Python script to convert an [Obsidian](https://obsidian.md/) vault into a vault of HTML files, with the goal of publishing them as static files. It is heavily dependent on the excellent [markdown2](https://github.com/trentm/python-markdown2) by [trentm](https://github.com/trentm), but also deals with some parsing and file handling that makes it compatible with Obsidian's flavor of Markdown.

## Installation

```
pip install -r requirements.txt
```

## Usage

`obsidian-html` will by default convert all the Markdown documents in the folder you're running it in recursively, and place the HTML files in a directory called `html`. It will also copy all other files to this new directory following the same structure as it's source. You might not want to run it directly in your vault or place the converted files in another directory. This is specified by this syntax:

    obsidian-html <path to vault> -o <path to html files>

Any extra directories may be supplied to the `-d` flag, like in this example:

    obsidian-html <vault> -d "Daily notes" "Zettels"

### Templates

The output is not very exiting from the get-go. It needs some style and structure. This is done by using a HTML template. A template must have the formatters `{title}` and `{content}` present. Their value should be obvious. The template file is supplied to `obsidian-html` by the `-t` flag, like this:

    obsidian-html <vault> -t template.html

Here you can add metadata, link to CSS-files and add unified headers/footers to all the pages.

### TeX support via KaTeX

By loading KaTeX in the HTML template and initializing it with `$` and `$$` as delimiters, you will have TeX support on the exported documents.

<details>
<summary>Add this to the bottom of you template's body</summary>
<code>
<!-- KaTeX -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.css"
  integrity="sha384-zB1R0rpPzHqg7Kpt0Aljp8JPLqbXI3bhnPWROx27a9N0Ll6ZP/+DiW/UqRcLbRjq" crossorigin="anonymous">

<!-- The loading of KaTeX is deferred to speed up page rendering -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.js"
  integrity="sha384-y23I5Q6l+B6vatafAwxRu/0oK/79VlbSz7Q9aiSZUvyWYIYsd+qj+o24G5ZU2zJz"
  crossorigin="anonymous"></script>

<!-- To automatically render math in text elements, include the auto-render extension: -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/contrib/auto-render.min.js"
  integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI"
  crossorigin="anonymous"></script>

<!-- Parsing single dollar signs -->
<script>
  document.addEventListener("DOMContentLoaded", function () {{
      renderMathInElement(document.body, {{
        delimiters: [
          {{left: "$$", right: "$$", display: true}},
        {{left: "\\[", right: "\\]", display: true}},
    {{left: "$", right: "$", display: false}},
    {{left: "\\(", right: "\\)", display: false}}
      ]
  }});
  }});
</script>
</code>
</details>

### Syntax highlighting of code blocks

Using [highlight.js](https://highlightjs.org/), syntax highlighting is easily achieved.


<details>
<summary>Just add this to the bottom of you template's body</summary>
<code>
<!-- Syntax highlighting through highlight.js -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@10.1.2/styles/github-gist.css">
<script src="//cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.1.2/build/highlight.min.js"></script>

<script>hljs.initHighlightingOnLoad();</script>
</code>
</details>

## Deploying vault with GitHub Actions

Make a GitHub Actions workflow using the YAML below, and your vault will be published to GitHub Pages every time you push to the repository.

1. Make sure you have GitHub Pages set up in the vault, and that it has `gh-pages` `/root` as its source.
2. Modify the following YAML job to match your repository.

    ```yaml
    name: Deploy to GitHub Pages

    on:
      push:
        branches: [ master ]
      
    jobs:
      deploy:
        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v2

        - name: Set up Python 3.8
          uses: actions/setup-python@v2
          with:
            python-version: 3.8

      - name: Install obsidian-html
        run: |
          python -m pip install --upgrade pip
          pip install git+https://github.com/kmaasrud/obsidian-html.git
          
      - name: Generate HTML through obsidian-html
        run: obsidian-html ./vault -o ./out -t ./template.html -d daily

      - name: Deploy
        uses: s0/git-publish-subdir-action@develop
        env:
          REPO: self
          BRANCH: gh-pages
          FOLDER: out
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    ```

## To do

- [ ] Support the `[[]]` embedding syntax

## Known issues

- Windows & Linux weirdness with paths
