#!/bin/sh

set -e

MFCL=${PROGRAM_PATH:-mfclo64}
BET_FINAL_CONVERGENCE=${BET_FINAL_CONVERGENCE:-${BET_PHASE10_11_CONVERGENCE:--4}}

# -----------------------------------
#  PHASE 0 - create initial par file
# -----------------------------------

"${MFCL}" bet.frq bet.ini 00.par -makepar

# -----------------------
#  PHASE 1 - initial par
# -----------------------

"${MFCL}" bet.frq 00.par 01.par -file - <<PHASE1
# Use default quasi-Newton minimizer
  1 351 0
  1 192 0
# Allow all growth parameters to be fixed during control phase
  1 32 7
# Richards growth settings
  1 226 0
  1 227 0
# Catch conditioned flags
# General activation
  1 373 1  # activate CC with Baranov equation
  1 393 0  # estimate kludged_equilib_coffs and implicit_fm_level_regression_pars
  2 92 2   # specify catch-conditioned option with Baranov equation
# Catch equation bounds
  2 116 70   # value for Zmax_fish in catch equations
  2 189 80   # fraction of Zmax_fish above which penalty is calculated
  1 382 300  # weight for Zmax_fish penalty - set to 300 to avoid triggering Zmax_flag=1
# Deactivate any catch errors flags
  -999 1 0
  -999 4 0
  -999 10 0
  -999 15 0
  -999 13 0
# Survey fisheries defined
# fish flag 92 = round(mean index CV * 100), fish flag 94 = allow unequal sigma, fish flag 66 = 0
  -29 94 1       -29 92 25   -29 66 0
# Grouping flags for survey CPUE
   -1 99 1
   -2 99 2
   -3 99 3
   -4 99 4
   -5 99 5
   -6 99 6
   -7 99 7
   -8 99 8
   -9 99 9
  -10 99 10
  -11 99 11
  -12 99 12
  -13 99 13
  -14 99 14
  -15 99 15
  -16 99 16
  -17 99 17
  -18 99 18
  -19 99 19
  -20 99 20
  -21 99 21
  -22 99 22
  -23 99 23
  -24 99 24
  -25 99 25
  -26 99 26
  -27 99 27
  -28 99 28
  -29 99 29
# Recruitment and initial population settings
  1 149 100        # recruitment deviation penalty
  1 400 6          # final six recruitment deviates set to zero
# Fixed terminal recruitments are arithmetic mean of remaining period (not default geometric mean)
  1 398 1
  2 177 1          # use old totpop scaling method
  2 32 1           # and estimate totpop parameter
  2 93 4           # set no. of recruitments per year to 4
  2 57 4           # set no. of recruitments per year to 4
  2 94 1 2 128 100  # initial Z = 1.0*M, i.e. initial F = 0
# Likelihood component settings
  1 141 3     # set likelihood function for LF data to normal
  1 139 3     # set likelihood function for WF data to normal
  -999 49 20  # divide LF sample sizes by 20
  -999 50 20  # divide WF sample sizes by 20
# For longline ALL and Index fisheries reduce sample size in half
# so we aren't double counting sample sizes
# Tag dynamics settings
# Selectivity settings
  -999 3 37  # all selectivities equal for age class 37 and older
  -999 26 2  # set length-dependent selectivity option
  -999 57 3  # uses cubic spline selectivity
  -999 61 5  # with 5 nodes for cubic spline
  -12 61 8   # this selectivity complexit for F12 and F13 is necessary to model the modal characteristics of the LF.
  -13 61 8   # This in reality due to seasonal recruitment in the north, which a single region model cannot capture.
# Grouping of fisheries with common selectivity
   -1 24 1   # LL WEST 1
   -2 24 2   # LL EAST 1
   -3 24 3   # LL US 1
   -4 24 4   # LL ALL 2
   -5 24 5   # LL OS 2
   -6 24 6   # LL ARCH 3
   -7 24 7   # LL WEST 3
   -8 24 8   # LL EAST 4
   -9 24 9   # LL OS 3
  -10 24 10  # LL ALL 5
  -11 24 11  # LL AU 5
  -12 24 12  # PS JP 1
  -13 24 13  # PL JP 1
  -14 24 14  # HL ID 2
  -15 24 15  # HL PH 2
  -16 24 16  # PL ALL 2
  -17 24 17  # PS ID 2
  -18 24 18  # PS PH 2
  -19 24 19  # PS ASS 2
  -20 24 20  # PS UNA 2
  -21 24 21  # MISC ID 2
  -22 24 22  # MISC PH 2
  -23 24 23  # MISC VN 2
  -24 24 24  # PL ALL WEST 3
  -25 24 25  # PS ASS WEST 3
  -26 24 26  # PS ASS EAST 4
  -27 24 27  # PS UNA WEST 3
  -28 24 28  # PS UNA EAST 4
  -29 24 29  # INDEX
# Non-decreasing selectivity for at least one index/longline fishery in each region
   -9 16 1
# Make other longline selectivites 0 for first two age classes
   -1 75 2
   -2 75 2
   -3 75 2
   -4 75 2
   -5 75 2
   -6 75 2
   -7 75 2
   -8 75 2
   -9 75 2
  -10 75 2
  -11 75 2
  -12 75 2
  -13 75 1
  -29 75 2
# Make HL.PHID.7 selectivites 0 for first 5 age classes
  -15 75 5
  -17 16 2  -17 3 25  # FAD fisheries age-based with splines and set to zero above 25 quarters
  -18 16 2  -18 3 25
  -19 16 2  -19 3 25
  -25 16 2  -25 3 25
  -26 16 2  -26 3 25
  -20 16 2  -20 3 30  # free school fisheries
  -27 16 2  -27 3 30
  -28 16 2  -28 3 30
  -16 16 2  -16 3 25  # also for PL fisheries
  -24 16 2  -24 3 25
# Forcing selectivity to zero for large fish in small MISC fisheries
  -21 16 2  -21 3 10
  -22 16 2  -22 3 7
  -23 16 2  -23 3 6
# Turn on weighted spline for calculating maturity at age
  2 188 2
# Set Lorenzen M
  2 109 3  # select Lorenzen curve
  1 121 0  # do not estimate Lorenzen scaling parameter yet
# Filter out comps with input samples less than 50
  1 311 1   # set tail compression for LF data
  1 301 1   # set tail compression for WF data
  1 313 0   # proportions in compressed tails for LF data
  1 303 0   # proportions in compressed tails for WF data
  1 312 50  # set minimum obs sample size for LF data
  1 302 50  # set minimum obs sample size for WF data
# MFCL 2.2.2.0 growth variance fix
  1 34 0    # set to 1 34 1 for backwards compatibility
PHASE1

# ---------
#  PHASE 2
# ---------

"${MFCL}" bet.frq 01.par 02.par -file - <<PHASE2
  1 1 100  # set max. number of function evaluations per phase to 100
  1 50 0   # set convergence criterion to 1
  2 113 0  # scaling init pop - turned off
  1 190 1  # write plot-xxx.par.rep
PHASE2

# ---------
#  PHASE 3 - OPR
# ---------

"${MFCL}" bet.frq 02.par 03.par -file - <<PHASE3
  1 155 72 1 221 72  # Sets degree for year effect
  1 217 1            # Sets degree for season effect
  1 216 1            # Sets degree for region effect
  1 218 0            # Sets degree for region-season interaction effect
  1 202 2            # Do estimate year effect for last year
  1 210 0            # Likewise region effect
  1 212 0            # Likewise season effect
  1 214 0            # Likewise region-season interaction effect
# Disable devs parameters (for neatness)
  1 149 0
  1 398 0
  1 400 0
  2 30 1
  2 32 0
  2 70 0
  2 71 0
  2 177 0
  2 178 0
  2 113 0
PHASE3

# ---------
#  PHASE 4
# ---------

"${MFCL}" bet.frq 03.par 04.par -file - <<PHASE4
  1 240 1  # fit to age-length data
  1 14 1   # estimate von Bertalanffy K
  1 12 1   # estimate mean length of age 1
  1 13 1   # estimate length of age n
  1 1 300  # function evaluations
PHASE4

# ---------
#  PHASE 5
# ---------

"${MFCL}" bet.frq 04.par 05.par -file - <<PHASE5
  1 15 1   # estimate overall SD of length-at-age
  1 16 1   # estimate length dependent SD
  1 173 0  # activate independent mean lengths for first 0 age classes
  1 182 0  # penalty weight
  1 184 0  # estimate parameters
  1 1 500  # function evaluations
PHASE5

# ---------
#  PHASE 6
# ---------

"${MFCL}" bet.frq 05.par 06.par -file - <<PHASE6
  2 145 1    # use SRR parameters - low penalty for deviation
  2 146 1    # estimate SRR parameters
  2 182 1    # make SRR annual rather than quarterly
  2 161 1    # lognormal bias correction
  2 163 0    # use steepness parameterization of B&H SRR
  1 149 0    # penalty for recruitment devs
  2 147 1    # time period between spawning and recruitment
  2 148 20   # period for MSY calc - last 20 quarters
  2 155 4    # but not including last year
  2 199 212  # start period for SRR estimation/yield is start 1965?
  2 200 6    # end period for SRR estimation is mid 2017
  -999 55 1  # do impact analysis
  2 171 1    # include SRR-based equilibrium recruitment to compute unfished biomass
  1 186 1    # write fishmort and plotq0.rep
  1 187 1    # write temporary_tag_report
  1 188 1    # write ests.rep
  1 189 1    # write .fit files
  1 1 500    # function evaluations
  1 50 -2    # convergence criteria
  2 116 100  # increase F bound for NR to 1.0
PHASE6

# ---------
#  PHASE 7
# ---------
"${MFCL}" bet.frq 06.par 07.par -file - <<PHASE7
  2 145 -1   # use SRR parameters - low penalty for deviation
  1 1 5000    # function evaluations
  1 50 ${BET_FINAL_CONVERGENCE}  # convergence criterion (default -4)
  2 116 300  # increase F bound for NR to 3.0
  1 246 1   # indepvar.rpt
PHASE7

## ---------
## PHASE 8
## ---------
##
## Estimate seasonal selectivity for subtropical fisheries - proxy for seasonal recruitment effects.
# mfclo64 bet.frq 07.par 08.par -file - <<PHASE8
#   -1 74 4
#   -2 74 4
#   -3 74 4
#  -10 74 4
#  -11 74 4
#  -13 74 4
#PHASE8
