# YFT 2026 single-area model

The base Kflow job runs `yft.frq` once from the supplied fitted `final.par` to `08.par`.

Jitter and retrospective diagnostics start independently from `yft.ini`, generate a fresh `00.par`, and run the complete model-specific phase sequence.

Only reusable model inputs and label metadata are versioned. Generated MFCL outputs are produced by Kflow.
