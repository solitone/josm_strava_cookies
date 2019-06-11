#!/bin/bash
#
# Saves a text file with the Strava Heatmap TMS URLs in the Cartograph
# folder on iCloud
# https://www.cartograph.eu

OUTDIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Cartograph Pro"
./gen_urls.sh -c -R > "$OUTDIR/strava_urls.txt"
echo -e "\n" >> "$OUTDIR/strava_urls.txt"
./gen_urls.sh -c -b >> "$OUTDIR/strava_urls.txt"
echo -e "\n" >> "$OUTDIR/strava_urls.txt"
./gen_urls.sh -c -r >> "$OUTDIR/strava_urls.txt"
echo -e "\n" >> "$OUTDIR/strava_urls.txt"
./gen_urls.sh -c -w >> "$OUTDIR/strava_urls.txt"
