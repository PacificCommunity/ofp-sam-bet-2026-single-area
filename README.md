# BET 2026 Single-Area

<p align="right">
  <a href="kflow.yaml"><img src="kflow-ready.svg" alt="Kflow ready task"></a>
</p>

BET 2026 single-area MFCL model runner for Kflow. The repository keeps one
runnable model folder under `steps/01-SingleArea/model/` and uses the same
compact-output pattern as the BET 2026 stepwise workflow.

## Model

| Model | What it is | Source |
| --- | --- | --- |
| `01-SingleArea` | Single-area BET model run from `00.par` through `09.par` using `doitall.sh`. | Curated single-area BET input set. |

## Included Inputs

| File | Use |
| --- | --- |
| `00.par` | Starting par for the single-area `doitall.sh` run. |
| `bet.frq` | MFCL frequency input. |
| `bet.ini` | Source ini retained for provenance; the current script starts from `00.par`. |
| `bet.age_length` | Age-length input used by the model. |
| `doitall.sh` | Native MFCL run script ending at `09.par`; MFCL calls use `PROGRAM_PATH` and final convergence uses `BET_PHASE10_11_CONVERGENCE`, default `-3`. |
| `mfcl.cfg`, `labels.tmp`, `index.txt` | Supporting model files for the single-area run. |

Large fitted outputs, including `69-01-01-00/`, reports, Hessian files, fit
files, and generated `.par` chains after `00.par`, are intentionally not
tracked here.

## Kflow

The Kflow task is `ofp-sam-bet-2026-single-area`.

Default launch settings:

| Setting | Value |
| --- | --- |
| `STEP_SELECT` | `all` |
| `RUN_MODE` | `doitall` |
| `BET_PHASE10_11_CONVERGENCE` | `-3` |
| `PROGRAM_PATH` | `/home/mfcl/mfclo64` |
| CPUs | `2` |
| Memory | `8GB` |
| Final par | `09.par` |

For fast structural Kflow tests, set `RUN_MODE=smoke_bundle`,
`INPUT_PAR=00.par`, and `OUTPUT_PAR=final.par`. That mode skips MFCL, copies
the input par to the output par, and writes a compact payload so downstream
diagnostic tasks can validate their attach/merge flow without running a full
fit.

Useful commands:

```sh
make list
make kflow TRIGGER_NEXT=false
```

After a successful run, compact model outputs are written under
`outputs/models/01-SingleArea/` and can be opened with the MFCL Shiny local app
registered in `kflow.yaml`.
