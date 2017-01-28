#!/bin/sh
sort -T /non-persistent $1 | uniq -c
