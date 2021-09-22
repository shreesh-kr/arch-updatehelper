#!/usr/bin/bash

mkdir -p $HOME/.local/arch-updatehelper/


cp update.py $HOME/.local/arch-updatehelper
cp data $HOME/.local/arch-updatehelper

echo "alias update='python $HOME/.local/arch-updatehelper/update.py'" >> $HOME/.bashrc
