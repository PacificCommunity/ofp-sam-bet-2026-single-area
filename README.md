# BET 2026 Single-Area

<p align="right">
  <a href="kflow.yaml"><img src="kflow-ready.svg" alt="Kflow ready task"></a>
</p>

BET 2026 single-area MFCL model runner for Kflow. The repository keeps one
runnable model folder under `steps/01-SingleArea/model/` and uses the same
compact-output pattern as the BET 2026 stepwise workflow. The default Kflow run
runs briefly from the fitted `09.par` checkpoint, then builds the compact
payload from the generated MFCL reports and fit files. The full `doitall.sh` fit
remains available as an override.

## Model

| Model | What it is | Source |
| --- | --- | --- |
| `01-SingleArea` | Single-area BET short run from fitted `09.par`; full `doitall.sh` can rerun from `00.par`. | Curated single-area BET input set. |

## Included Inputs

| File | Use |
| --- | --- |
| `00.par` | Starting par for the single-area `doitall.sh` run. |
| `09.par` | Fitted checkpoint used by the default fast Kflow run. |
| `bet.frq` | MFCL frequency input. |
| `bet.ini` | Source ini retained for provenance; the current script starts from `00.par`. |
| `bet.age_length` | Age-length input used by the model. |
| `doitall.sh` | Native MFCL run script ending at `09.par`; MFCL calls use `PROGRAM_PATH` and final convergence uses `BET_PHASE10_11_CONVERGENCE`, default `-3`. |
| `mfcl.cfg`, `labels.tmp`, `index.txt` | Supporting model files for the single-area run. |

Large fitted outputs, including `69-01-01-00/`, reports, Hessian files, fit
files, and intermediate `.par` chains between `00.par` and `09.par`, are
intentionally not tracked here. Kflow's compact runtime artifact retains the
small generated `indepvar.rpt`/`xinit.rpt` reports when present because native
Jitter needs the active-parameter map; other bulky fit outputs remain omitted.

## Kflow

The Kflow task is `ofp-sam-bet-2026-single-area`.

Default launch settings:

| Setting | Value |
| --- | --- |
| `STEP_SELECT` | `all` |
| `RUN_MODE` | `single_par` |
| `INPUT_PAR` | `09.par` |
| `OUTPUT_PAR` | `final.par` |
| `BET_PHASE10_11_CONVERGENCE` | `-3` |
| `PROGRAM_PATH` | `/home/mfcl/mfclo64` |
| Runtime diagnostics | `mfclkit 0.0.0.9016` and `mfclshiny 0.0.0.9015` |
| CPUs | `2` |
| Memory | `8GB` |
| Final par | `final.par` |

The pinned diagnostic packages are installed in the short-lived runtime library;
Kflow forwards GitHub access only for that source-install step.

The default `single_par` mode runs MFCL from `09.par` to `final.par` with one
function-evaluation pass and report output enabled, then uses the generated
files to build `model_payload.rds` for Shiny and downstream diagnostic tasks. To
rerun the model from `00.par`, override `RUN_MODE=doitall`, clear `INPUT_PAR`
and `OUTPUT_PAR`, and keep `BET_PHASE10_11_CONVERGENCE=-3` for the quick
convergence setting.

Useful commands:

```sh
make list
make kflow TRIGGER_NEXT=false
```

After a successful run, compact model outputs are written under
`outputs/models/01-SingleArea/` and can be opened with the MFCL Shiny local app
registered in `kflow.yaml`.

Diagnostic unit jobs are merged independently by diagnostic type. Each
diagnostic merge publishes its delta directly onto the original single-area
fit, so no separate common merge or attach job is created and concurrent
Hessian, profile, jitter, retrospective, ASPM, and self-test updates do not
replace one another.
