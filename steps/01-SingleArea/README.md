# 01 Single-Area

One-region BET model rebuilt from the BET2026 archive inputs. The default Kflow
path starts from the MFCL 1007 INI and runs the complete active doitall sequence.

## Snapshot

| Field | Value |
| --- | --- |
| Model folder | `steps/01-SingleArea/model` |
| Run mode | `doitall` |
| Final par | `07.par` |
| Region count | `1` |
| Fisheries | `29` |

## Notes

Phase 0 creates `00.par` from `bet.frq` and the 1007 `bet.ini`. Existing PAR
checkpoints, generated reports, Hessian files, fit files, and intermediate PAR
files are excluded from version control.

`doitall.sh` uses `${PROGRAM_PATH:-mfclo64}` for every MFCL call. Kflow sets
`PROGRAM_PATH=/home/mfcl/mfclo64` through the runner, while local direct runs can
still fall back to `mfclo64` on `PATH`.

The final phase uses `BET_FINAL_CONVERGENCE`, defaulting to the archived `-4`.
