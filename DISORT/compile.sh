#!/usr/bin/env bash

# compile flies
gfortran -O3 -g -fcheck=all -fdump-core -fbounds-check -Wall \
  getopt.F90  disort_variables.f90 asd_albedo.f90 code.f \
  -o asd_albedo

# Make exectuable
chmod +x asd_albedo
