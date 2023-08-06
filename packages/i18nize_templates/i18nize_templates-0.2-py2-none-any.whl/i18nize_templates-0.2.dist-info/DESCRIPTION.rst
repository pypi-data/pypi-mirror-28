i18nize-templates
=================

A tool to automatically add i18n markup to jinja2 and handlebars
templates.  It may also work for django, though this is not tested.

This is part of a process to make a non-i18n-aware jinja2 or
handlebars file i18n-aware.  i18n-ness support is mostly a matter of
marking natural-language text in the file that needs to be translated.
While some complicated natural language constructs (like plurals)
require a bit more work, the simple case is very simple: replace

    <p>Hello <b>world</b></p>

with

    <p>{{ _("Hello <b>world</b>") }}</p>

This script helps with that process.


Use
---
    i18nize_templates <file> ...
OR
    i18nize_templates [--handlebars] < <infile> > <outfile>


