#!/usr/bin/env bash

MODEL_CODE="disort_model"
EXECUTABLE="ssa_ice"

# Remove old binary
if [[ -f "${EXECUTABLE}" ]]; then
  rm ${EXECUTABLE}
fi

pushd disort-4.0.99
cat DISOTESTAUX.f DISORT.f BDREF.f DISOBRDF.f ERRPACK.f LINPAK.f LAPACK.f RDI1MACH.f > ../${MODEL_CODE}.f
popd

# compile flies
gfortran -O3 -g -fcheck=all -fdump-core -fbounds-check -Wall \
  getopt.F90  disort_variables.f90 ${EXECUTABLE}.f90 ${MODEL_CODE}.f \
  -o ${EXECUTABLE}

# Make executable
chmod +x ${EXECUTABLE}
