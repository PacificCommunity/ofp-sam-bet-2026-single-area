# 01 Single-Area

Single-area BET model imported from the provided single-area BET input bundle.

## Snapshot

| Field | Value |
| --- | --- |
| Model folder | `steps/01-SingleArea/model` |
| Run mode | `doitall` |
| Final par | `09.par` |
| Region count | `1` |

## Notes

The source archive contains both input files and previous fitted outputs. This
repo tracks only the files needed to rerun the model from `00.par`. The existing
fitted output folder `69-01-01-00/`, generated reports, Hessian files, fit
files, and later `.par` files are excluded from version control.

`doitall.sh` uses `${PROGRAM_PATH:-mfclo64}` for every MFCL call. Kflow sets
`PROGRAM_PATH=/home/mfcl/mfclo64` through the runner, while local direct runs can
still fall back to `mfclo64` on `PATH`.

The final phase uses `BET_PHASE10_11_CONVERGENCE`, defaulting to `-3`, so Kflow
e-3 submissions are reflected inside the `doitall` switch block.
