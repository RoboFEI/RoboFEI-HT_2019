#!/bin/bash

find -iname "*.sh" -not -iname "*avell*" -exec sed -i "s/\/research//g" {} \;

sed -i "s/~/~\/Documents\//g" check.py
