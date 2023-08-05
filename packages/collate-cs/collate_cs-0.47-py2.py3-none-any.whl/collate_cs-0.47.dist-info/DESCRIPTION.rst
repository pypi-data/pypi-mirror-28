## description

The thin format for source code is designed to minimise visual distraction when coding. Methods and variable declarations are separated into different files. Whitespace is syntactically significant.

This repository contains the python code used to translate thin format csharp code into normal csharp code.

## usage

collate_cs from_path to_path depth

## getting started

To work on developing this repository, add a file called local.zsh with the following format:

\#!/bin/zsh
nunit_path='nunit.framework.dll Windows path'
csc='csc.exe path'
nunit_runner='nunitlite-runner.exe path'


