# Default Kflow runs for the fitted BET and YFT 2026 single-area models.

stepwise_run <- list(
  default_step_select = "all",
  flow_group = "bet-yft-2026-single-area",
  trigger_next = FALSE
)

stepwise_models <- data.frame(
  step_id = c("BET", "YFT"),
  enabled = c(TRUE, TRUE),
  major_step = c("BET", "YFT"),
  substep = c("BET", "YFT"),
  change_axis = c(
    "BET fitted single-area snapshot",
    "YFT fitted single-area snapshot"
  ),
  model_label = c(
    "BET 2026 single-area fitted model",
    "YFT 2026 single-area fitted model"
  ),
  job_title = c(
    "BET 2026 single-area fitted final-PAR run",
    "YFT 2026 single-area fitted final-PAR run"
  ),
  job_key = c(
    "bet-2026-single-area-final-par",
    "yft-2026-single-area-final-par"
  ),
  run_mode = c("single_par", "single_par"),
  region_count = c(1L, 1L),
  kflow_memory = c("8GB", "8GB"),
  mfcl_program_path = c("", ""),
  input_par = c("final.par", "final.par"),
  frq = c("bet.frq", "yft.frq"),
  output_par = c("08.par", "08.par"),
  expected_final_par = c("", ""),
  stringsAsFactors = FALSE
)
