args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) {
  stop("Usage: Rscript scripts/build_fishery_map.R <labels.tmp> <fishery_map.R> <species>")
}

labels_file <- args[[1L]]
output_file <- args[[2L]]
species <- toupper(args[[3L]])

lines <- trimws(readLines(labels_file, warn = FALSE))
matches <- regexec("^([0-9]+)[.]?[[:space:]]+(.+)$", lines)
parts <- regmatches(lines, matches)
parts <- parts[lengths(parts) == 3L]

fishery <- as.integer(vapply(parts, function(x) x[[2L]], character(1)))
fishery_name <- trimws(vapply(parts, function(x) x[[3L]], character(1)))
keep <- is.finite(fishery) & nzchar(fishery_name) &
  !grepl("^summary$", fishery_name, ignore.case = TRUE)
fishery <- fishery[keep]
fishery_name <- fishery_name[keep]

if (!length(fishery) || !identical(fishery, seq_along(fishery))) {
  stop("Fishery labels must be consecutive and start at 1: ", labels_file)
}

group <- vapply(toupper(fishery_name), function(label) {
  if (grepl("^INDEX([ .]|$)", label)) return("Index")
  for (candidate in c("LL", "PS", "PL", "HL", "MISC")) {
    if (grepl(paste0("^", candidate, "([ .]|$)"), label)) return(candidate)
  }
  "Other"
}, character(1))

quoted <- function(x) paste(encodeString(x, quote = "\""), collapse = ",\n    ")
output <- c(
  paste0("# Generated from ", basename(labels_file), " for the ", species, " single-area model."),
  "# Historical area suffixes in display labels are retained; MFCL region is 1 for every fishery.",
  "",
  "fishery_map <- data.frame(",
  "  fishery_name = c(",
  paste0("    ", quoted(fishery_name)),
  "  ),",
  paste0("  fishery = 1:", length(fishery), ","),
  paste0("  region = rep(1L, ", length(fishery), "),"),
  "  group = c(",
  paste0("    ", quoted(group)),
  "  ),",
  "  stringsAsFactors = FALSE",
  ")",
  ""
)
writeLines(output, output_file, useBytes = TRUE)
