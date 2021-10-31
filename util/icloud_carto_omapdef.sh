#!/bin/bash
#
# Writes out a map definition file that can be easiy imported in Cartograph.
# See Cartograph online map definition file:
# https://www.cartograph.eu/help_onlinemapimport

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

python3 ../carto_strava_omapdef.py > "$OUTDIR/carto_strava.onlinemap"
