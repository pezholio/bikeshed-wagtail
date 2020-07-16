from os import path
from django_assets import Bundle, register
from webassets.filter import get_filter

LIBSASS = get_filter("libsass")
css_filters = [LIBSASS]

core_css_files = ["_dev/scss/screen.scss"]

css_core_bundle = Bundle(
    *core_css_files,
    depends="_dev/scss/**/*.scss",
    filters=css_filters,
    output="dist/css/main.min.css"
)
register("css_core", css_core_bundle)
