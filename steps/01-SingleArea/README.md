# 01 Single-Area

Single-area BET model from the curated BET input set. The default Kflow path
runs briefly from the fitted `09.par` checkpoint and packages the generated
MFCL output for fast diagnostics smoke tests.

## Snapshot

| Field | Value |
| --- | --- |
| Model folder | `steps/01-SingleArea/model` |
| Run mode | `single_par` |
| Final par | `final.par` produced from `09.par` |
| Region count | `1` |

## Notes

This repo tracks the files needed to rerun the model from `00.par` plus the
fitted `09.par` checkpoint used for quick Kflow diagnostics tests. The default
Kflow run regenerates the report and fit files needed by `model_payload.rds`.
Existing fitted output folders, generated reports, Hessian files, fit files, and
intermediate `.par` files are excluded from version control.

`doitall.sh` uses `${PROGRAM_PATH:-mfclo64}` for every MFCL call. Kflow sets
`PROGRAM_PATH=/home/mfcl/mfclo64` through the runner, while local direct runs can
still fall back to `mfclo64` on `PATH`.

The final phase uses `BET_PHASE10_11_CONVERGENCE`, defaulting to `-3`, so Kflow
e-3 submissions are reflected inside the `doitall` switch block.
