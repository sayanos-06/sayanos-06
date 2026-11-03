# Profile refresh

Updated November 3, 2026. Published to sayanos-06/sayanos-06. The included GitHub Actions workflow keeps the contribution graphics updated.

The included workflow runs daily around 06:53 IST and supports manual runs from GitHub Actions. Repository policy must allow workflow writes. Scheduled runs can be delayed or disabled by GitHub after extended inactivity.

Manual refresh from this directory:

```sh
python -m pip install -r scripts/requirements-profile.txt
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
python scripts/render_stats_svg.py
python scripts/make_ascii_svg.py
python scripts/update_image_versions.py
```

Commit the JSON and SVG outputs together. Counts use the publicly visible contribution calendar. Enable Private contributions under profile Contribution settings to include anonymous private daily counts and match the signed-in profile. Repository names and code remain private. Failed requests or unreadable counts stop the fetch before replacing the snapshot.

The knight artwork and avi-ascii.svg filename are retained for compatibility. Visible names now identify Sayantan Sen. Replace source-prepped.png to change the artwork. Optional photo preparation uses the additional dependencies in scripts/requirements.txt.
