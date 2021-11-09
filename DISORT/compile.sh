#!/usr/bin/env bash

EXECUTABLE="asd_albedo"

# Remove old binary
if [[ -f "${EXECUTABLE}" ]]; then
  rm ${EXECUTABLE}
fi

# compile flies
gfortran -O3 -g -fcheck=all -fdump-core -fbounds-check -Wall \
  getopt.F90  disort_variables.f90 asd_albedo.f90 code.f \
  -o ${EXECUTABLE}

# Make exectuable
chmod +x asd_albedo
