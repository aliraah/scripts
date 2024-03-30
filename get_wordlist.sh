#!/bin/bash

echo "Fetching trickests subdomains..."
wget https://raw.githubusercontent.com/trickest/wordlists/main/inventory/subdomains.txt
echo "Fetchng assetnote's 9m dns wordlist..."
wget https://wordlists-cdn.assetnote.io/data/manual/best-dns-wordlist.txt
echo "Fetchng assetnote's 2m sub wordlist..."
wget https://wordlists-cdn.assetnote.io/data/manual/2m-subdomains.txt
echo "Fetching python cleaner..."
wget https://raw.githubusercontent.com/aliraah/scripts/main/clean.py

echo "Cleaning subdomains.txt..."
cat subdomains.txt | tr '[:upper:]' '[:lower:]' | sort -u > 1 
python3 clean.py 1 > 2
echo "done."

echo "Cleaning 2m-subdomains.txt..."
cat 2m-subdomains.txt | tr '[:upper:]' '[:lower:]' | sort -u > 1 
python3 clean.py 1 > 2
echo "done."

echo "Cleaning best-dns-wordlist.txt..."
cat best-dns-wordlist.txt | tr '[:upper:]' '[:lower:]' | sort -u > 1 
python3 clean.py 1 > 2
echo "done."

echo "Merging final results and cleaning..."
cat 2 | sort -u > wordlist-passive.txt

rm 1 2 subdomains.txt 2m-subdomains.txt best-dns-wordlist.txt
echo "Job done!"
