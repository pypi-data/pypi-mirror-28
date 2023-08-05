# `trapmk`: TrapHack Builder Script

[![PyPI](https://img.shields.io/pypi/v/trapmk.svg)](https://pypi.python.org/pypi/trapmk)

**WARNING: This software is in beta and is unsuitable for production usage.**

Builds a static site by doing these things:

  * Recurses directories, building `index.html` files from [jinja2 template
    files](http://jinja.pocoo.org/docs/latest/templates) named `_page` *or*
    from Markdown files named `_page.md`.
  * Can build a blog consisting of markdown posts named `_post.md`, including
    an index for each category and a blog front page index.
  * Used to create [TrapHack](http://y2k.cafe:8080/gallery/zones/traphack).
  * Used to build [SlimeMaid's website](http://slimemaid.zone)! Checkout the
    [SlimeMaid website repo](https://github.com/slimemaid/slimemaid.github.io/)
    to see `trapmk` in action!

See `example/` for an example site which can be built with `trapmk`!

Install to Python 3: `pip3 install trapmk`.

## Example

There is an example site in `example/`, it includes:

  * Markdown pages (`_page.md`)
  * Jinja2/HTML pages (`_page`)
  * some blog posts (`_post.md`)
  * a homepage (in `_home/`)

All you need to know is that all `_page`, `_page.md`, and `_post.md` files
should get their own directory/folder. Like this:

```
i-like-zelda/
    zelda-game-screenshot.png
    me-playing-zelda.jpg
    _page.md
```

You can make a homepage like this:

```
_home/
    _page
```

In the example above, `_page`'s contents might look like this:

```
{% extends "somebase.template" %}
{% markdown %}
oh cool you can arbitrarily include markdown with the `markdown` block!
you can read more about that
[on the `jinja2-markdown` GitHub repo](https://github.com/danielchatfield/jinja2_markdown)
{% endmarkdown %}
```

However, the blog is a bit trickier. A blog isn't required, but if you want
your site should look like this:

```
blog.template
category.template
page.template
post.template
blog/
    videogames/
        burrito-galaxy-is-good/
            _post.md
            screenshot-burrito-galaxy.jpg
        zelda-breath-of-wild/
            _post.md
            botw.jpg
            gerudo-link.jpg
    music/
        i-made-new-song/
            _post.md
            new-song.ogg
        heres-an-old-album/
            _post.md
            old-song-track-1.ogg
            old-song-track-2.ogg
            old-song-track-3.ogg
```

In the example above there are two categories, `music` and `videogames`, each
containing two blog posts. Each post must at least define the `timestamp`
Markdown meta like this:

```
title: Making Paper Crafts
timestamp: 2017-12-13

# Crafting

this is about contstruction paper crafts
```

You can also define `title` like above if you don't want the title to be the
first heading.

All of the `*.template` files are required to render the site to HTML (see the
ones in `example/` for reference!):

  * `page.template`: template used to render Markdown pages
  * `post.template`: template used to render blog posts
  * `blog.template`: template used to render the front page of the
    blog which displays the latest post from each category
  * `category.template`: template used to render blog category
    indexes

### Build the site

Once your site is prepared use `trapmk` (in terminal).

That's it! Your site will be built *in-place*.
