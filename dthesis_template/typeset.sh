#!/bin/sh

cp main.tex temp.tex
platex temp
pbibtex temp
platex temp
platex temp
dvipdfmx -o thesis.pdf temp
open thesis.pdf 
rm temp*
