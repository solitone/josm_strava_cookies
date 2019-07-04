#!/bin/bash
#
# Saves on iCloud a map definition file that can be easiy imported in Cartograph
# See Cartograph online map definition file:
# https://www.cartograph.eu/help_onlinemapimport

OUTDIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Cartograph Pro"

if [ ! -d "$OUTDIR" ]; then
  mkdir "$OUTDIR"
fi

python ../carto_strava_omapdef.py > "$OUTDIR/carto_strava.onlinemap"
