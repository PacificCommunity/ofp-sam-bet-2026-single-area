# YFT 2026 single-area model

The base Kflow job runs yft.frq from the supplied fitted final.par to 08.par once.

The model directory contains only reusable inputs and label metadata. Generated MFCL outputs are not versioned.

Jitter and retrospective diagnostics regenerate `00.par` from `yft.frq` and the 2026 single-region `yft.ini`, then run the full doitall phase sequence. A fitted active-parameter report is generated from the fitted PAR when it is not present in the parent artifact.
