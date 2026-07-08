# Edit this file to choose the default run and model metadata.
# The runner still uses the stepwise config object names, but this repo has one
# single-area model folder.

stepwise_run <- list(
  default_step_select = "all",
  flow_group = "bet-2026-single-area",
  trigger_next = TRUE
)

stepwise_models <- data.frame(
  step_id = "01-SingleArea",
  enabled = TRUE,
  major_step = "01-SingleArea",
  substep = "01a",
  change_axis = "single-area BET fitted checkpoint from curated input set",
  model_label = "Single-area checkpoint",
  job_title = "01 Single-area checkpoint",
  job_key = "01-single-area-checkpoint",
  run_mode = "smoke_bundle",
  region_count = 1L,
  kflow_memory = "8GB",
  mfcl_program_path = "",
  input_par = "09.par",
  frq = "bet.frq",
  output_par = "final.par",
  expected_final_par = "final.par",
  stringsAsFactors = FALSE
)
