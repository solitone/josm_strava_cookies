#!/bin/bash
ACTIVITY="both" #default
MODE="cartograph" #default

set_base_urls() {
  BASE_URL_CARTO="https://heatmap-external-a.strava.com/tiles-auth/$ACTIVITY/bluered/{z}/{x}/{y}.png"
  BASE_URL_JOSM="https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/$ACTIVITY/hot/{zoom}/{x}/{y}.png"
  BASE_URL_ORUX="https://heatmap-external-{\$s}.strava.com/tiles-auth/$ACTIVITY/bluered/{\$z}/{\$x}/{\$y}.png?px=256"
}

display_usage() {
  echo
  echo "Usage: $0 [-h] [-c|-j|-o] [-b|-R|-r|-w]"
  echo
  echo " -h   Display usage instructions"
  echo
  echo " -c   Generate Strava URL for Cartograph"
  echo " -j   Generate Strava URL for JOSM"
  echo " -o   Generate Strava URL for Oruxmaps"
  echo
  echo " -b   Activity type: all activities"
  echo " -R   Activity type: ride"
  echo " -r   Activity type: run"
  echo " -w   Activity type: winter sports"
  echo
}

get_cookies() {
  KEY_PAIR_ID=$(python3 ../BinaryCookieReader.py ~/Library/Cookies/Cookies.binarycookies |grep CloudFront-Key-Pair-Id|cut -d"=" -f2|cut -d";" -f1)
  POLICY=$(python3 ../BinaryCookieReader.py ~/Library/Cookies/Cookies.binarycookies |grep CloudFront-Policy|cut -d"=" -f2|cut -d";" -f1)
  SIGNATURE=$(python3 ../BinaryCookieReader.py ~/Library/Cookies/Cookies.binarycookies |grep CloudFront-Signature|cut -d"=" -f2|cut -d";" -f1)
}

out_url() {
  URL="$BASE_URL?Key-Pair-Id=$KEY_PAIR_ID&Policy=$POLICY&Signature=$SIGNATURE"
  echo $URL
}

if [ "$#" -lt 1 ]; then
  display_usage
  exit 1
fi

while getopts ":hcjobRrw" opt; do
  case ${opt} in
    h)
      display_usage
      exit 0
      ;;
    c)
      MODE="cartograph"
      ;;
    j)
      MODE="josm"
      ;;
    o)
      MODE="oruxmaps"
      ;;
    b)
      ACTIVITY="both"
      ;;
    R)
      ACTIVITY="ride"
      ;;
    r)
      ACTIVITY="run"
      ;;
    w)
      ACTIVITY="winter"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" #1>&2
      display_usage
      exit 1
      ;;
  esac
done
#shift $((OPTIND -1))

get_cookies
set_base_urls

case $MODE in
  cartograph)
    BASE_URL=$BASE_URL_CARTO
    ;;
  josm)
    BASE_URL=$BASE_URL_JOSM
    ;;
  oruxmaps)
    BASE_URL=$BASE_URL_ORUX
    ;;
esac

out_url
