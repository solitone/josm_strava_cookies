#!/bin/bash
#
# Saves a text file with the Strava Heatmap TMS URLs
# https://www.cartograph.eu

# writes file to current directory by default
OUTDIR="."

while (( "$#" )); do
  case "$1" in
    --icloud) # writes file on iCloud if --icloud flag is selected
      OUTDIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Cartograph Pro"
      if [ ! -d "$OUTDIR" ]; then
        mkdir "$OUTDIR"
      fi
      shift
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
  esac
done

./gen_urls.sh -c -R > "$OUTDIR/strava_urls.txt"
echo -e "\n" >> "$OUTDIR/strava_urls.txt"
./gen_urls.sh -c -b >> "$OUTDIR/strava_urls.txt"
echo -e "\n" >> "$OUTDIR/strava_urls.txt"
./gen_urls.sh -c -r >> "$OUTDIR/strava_urls.txt"
echo -e "\n" >> "$OUTDIR/strava_urls.txt"
./gen_urls.sh -c -w >> "$OUTDIR/strava_urls.txt"
