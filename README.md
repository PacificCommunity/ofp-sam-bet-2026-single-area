# BET 2026 Single-Area

<p align="right">
  <a href="kflow.yaml"><img src="kflow-ready.svg" alt="Kflow ready task"></a>
</p>

BET 2026 one-region MFCL model runner for Kflow and standalone use. The
`BET2026` branch rebuilds the model from the supplied 1007 INI and the complete
archived doitall sequence; no fitted checkpoint is carried forward from the
older single-area bundle.

## Model

| Model | What it is | Source |
| --- | --- | --- |
| `01-SingleArea` | 29-fishery, one-region BET model; Phase 0 creates `00.par` and the fit ends at `07.par`. | BET2026 one-region archive inputs. |

## Included Inputs

| File | Use |
| --- | --- |
| `bet.frq` | MFCL frequency input. |
| `bet.ini` | MFCL 1007 INI with `LN(R0)=17` and Richards growth input. |
| `bet.age_length` | Age-length input used by the model. |
| `bet.tag.txt` | Source tag data retained with the archive; the default FRQ has zero active tag groups. |
| `doitall.sh` | Fail-fast native MFCL sequence from `-makepar` through `07.par`; commands use `PROGRAM_PATH`. |
| `mfcl.cfg`, `labels.tmp` | Supporting model files from the same archive. |

Old PAR checkpoints and archived Hessian/report files are intentionally not
tracked. Kflow generates a fresh PAR chain and keeps the compact payload plus
the fit artifacts required by MFCL Shiny and downstream diagnostics.

## Kflow

The Kflow task is `ofp-sam-bet-2026-single-area`.

Default launch settings:

| Setting | Value |
| --- | --- |
| `STEP_SELECT` | `all` |
| `RUN_MODE` | `doitall` |
| `INPUT_PAR` | empty; generated from the 1007 INI |
| Expected final PAR | `07.par` |
| `BET_FINAL_CONVERGENCE` | `-4` |
| `PROGRAM_PATH` | `/home/mfcl/mfclo64` |
| Runtime diagnostics | `mfclkit 0.0.0.9017` and `mfclshiny 0.0.0.9015` |
| CPUs | `2` |
| Memory | `8GB` |
| Fisheries | `29` |

The pinned diagnostic packages are installed in the short-lived runtime library;
Kflow forwards GitHub access only for that source-install step.

The default run creates `00.par` from `bet.frq` and `bet.ini`, executes every
active phase in `doitall.sh`, and treats `07.par` as the final fit. The final
criterion defaults to the archive setting `-4`; override
`BET_FINAL_CONVERGENCE` only for an explicit convergence sensitivity.

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
