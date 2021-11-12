#!/usr/bin/env bash

EXECUTABLE="ssa_ice"

# Remove old binary
if [[ -f "${EXECUTABLE}" ]]; then
  rm ${EXECUTABLE}
fi

# compile flies
gfortran -O3 -g -fcheck=all -fdump-core -fbounds-check -Wall \
  getopt.F90  disort_variables.f90 ${EXECUTABLE}.f90 code.f \
  -o ${EXECUTABLE}

# Make executable
chmod +x ${EXECUTABLE}
