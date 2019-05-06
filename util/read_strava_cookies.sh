#!/bin/bash

echo "Key-Pair-Id: "
python BinaryCookieReader.py ~/Library/Cookies/Cookies.binarycookies |grep CloudFront-Key-Pair-Id|cut -d"=" -f2|cut -d";" -f1
echo "Policy: "
python BinaryCookieReader.py ~/Library/Cookies/Cookies.binarycookies |grep CloudFront-Policy|cut -d"=" -f2|cut -d";" -f1
echo "Signature: "
python BinaryCookieReader.py ~/Library/Cookies/Cookies.binarycookies |grep CloudFront-Signature|cut -d"=" -f2|cut -d";" -f1
