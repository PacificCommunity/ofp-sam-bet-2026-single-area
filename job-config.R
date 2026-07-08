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
  change_axis = "single-area BET model from curated input set",
  model_label = "Single-area",
  job_title = "01 Single-area",
  job_key = "01-single-area",
  run_mode = "doitall",
  region_count = 1L,
  kflow_memory = "8GB",
  mfcl_program_path = "",
  input_par = "",
  frq = "bet.frq",
  output_par = "",
  expected_final_par = "09.par",
  stringsAsFactors = FALSE
)
