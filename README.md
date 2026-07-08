# BET 2026 Single-Area

<p align="right">
  <a href="kflow.yaml"><img src="kflow-ready.svg" alt="Kflow ready task"></a>
</p>

BET 2026 single-area MFCL model runner for Kflow. The repository keeps one
runnable model folder under `steps/01-SingleArea/model/` and uses the same
compact-output pattern as the BET 2026 stepwise workflow. The default Kflow run
packages the fitted `09.par` checkpoint so diagnostics can be smoke-tested
quickly; the full `doitall.sh` fit remains available as an override.

## Model

| Model | What it is | Source |
| --- | --- | --- |
| `01-SingleArea` | Single-area BET fitted checkpoint packaged from `09.par`; full `doitall.sh` can rerun from `00.par`. | Curated single-area BET input set. |

## Included Inputs

| File | Use |
| --- | --- |
| `00.par` | Starting par for the single-area `doitall.sh` run. |
| `09.par` | Fitted checkpoint used by the default fast Kflow smoke/payload run. |
| `bet.frq` | MFCL frequency input. |
| `bet.ini` | Source ini retained for provenance; the current script starts from `00.par`. |
| `bet.age_length` | Age-length input used by the model. |
| `doitall.sh` | Native MFCL run script ending at `09.par`; MFCL calls use `PROGRAM_PATH` and final convergence uses `BET_PHASE10_11_CONVERGENCE`, default `-3`. |
| `mfcl.cfg`, `labels.tmp`, `index.txt` | Supporting model files for the single-area run. |

Large fitted outputs, including `69-01-01-00/`, reports, Hessian files, fit
files, and intermediate `.par` chains between `00.par` and `09.par`, are
intentionally not tracked here.

## Kflow

The Kflow task is `ofp-sam-bet-2026-single-area`.

Default launch settings:

| Setting | Value |
| --- | --- |
| `STEP_SELECT` | `all` |
| `RUN_MODE` | `smoke_bundle` |
| `INPUT_PAR` | `09.par` |
| `OUTPUT_PAR` | `final.par` |
| `BET_PHASE10_11_CONVERGENCE` | `-3` |
| `PROGRAM_PATH` | `/home/mfcl/mfclo64` |
| CPUs | `2` |
| Memory | `8GB` |
| Final par | `final.par` |

The default `smoke_bundle` mode skips MFCL, copies `09.par` to `final.par`, and
writes a compact payload so downstream diagnostic tasks can validate their
attach/merge flow without running a full fit. To rerun the model from `00.par`,
override `RUN_MODE=doitall`, clear `INPUT_PAR` and `OUTPUT_PAR`, and keep
`BET_PHASE10_11_CONVERGENCE=-3` for the quick convergence setting.

Useful commands:

```sh
make list
make kflow TRIGGER_NEXT=false
```

After a successful run, compact model outputs are written under
`outputs/models/01-SingleArea/` and can be opened with the MFCL Shiny local app
registered in `kflow.yaml`.
