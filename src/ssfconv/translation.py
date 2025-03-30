# import gettext, locale

# localedir = Path() / "data" / "locales"

# l10n = gettext.translation(
#     "ssfconv",
#     localedir=localedir,
#     fallback=True,
# )
# l10n.install()
# _ = l10n.gettext

#BUG https://github.com/breezy-team/setuptools-gettext/issues/94
# I dont want to use deprecated setup.py so i18n attempt get stuck
_ = lambda x:x #gettext placeholder