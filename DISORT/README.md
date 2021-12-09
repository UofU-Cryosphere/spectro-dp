# DISORT model

Setup to run the DIScrete Ordinate Radiative Transfer 
(DISORT; http://www.rtatmocn.com/disort/)
model using single scattering albedo for pure ice.

## Files
### `compile.sh`
Compiles DISORT model code and ice parameters into a `ssa_ice` executable.

#### `ssa_ice`
Command line program.

Required command line options: 
```shell
  --asymmetry <path_to_file> 
  --ssa <path_to_file> 
  --solar-zenith <angle_in_degrees>
```
