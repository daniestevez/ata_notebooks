#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include <rtklib.h>

#define RNX_PARAM 1
#define SP3_PARAM 2
#define ANTEX_PARAM 3
#define START_TIME_PARAM 4

int main(int argc, char **argv) {
  nav_t *nav;
  gtime_t t;
  double rs[6], dts[2], var, pos[3], e[3], rr[3];
  int svh;
  int j;
  pcvs_t pcvs = {0};
  pcv_t *pcv;

  nav = malloc(sizeof(*nav));
  if (!nav) {
    perror("malloc");
    exit(1);
  }

  memset(nav, 0, sizeof(*nav));

  if (readrnx(argv[RNX_PARAM], 0, "-SYS=E", NULL, nav, NULL) != 1) {
    fprintf(stderr, "Could not read RINEX\n");
    exit(1);
  }

  readsp3(argv[SP3_PARAM], nav, 0);
  if (!nav->peph) {
    fprintf(stderr, "Could not read SP3\n");
    exit(1);
  }

  if (!readpcv(argv[ANTEX_PARAM], &pcvs)) {
    fprintf(stderr, "Could not read ANTEX\n");
    exit(1);
  }
    
  if (str2time(argv[START_TIME_PARAM], 0, strlen(argv[START_TIME_PARAM]), &t) < 0) {
    fprintf(stderr, "Could not interpret time\n");
    exit(1);
  }

  /* assign PCVs from ANTEX */
  for (j = 0; j < MAXSAT; j++) {
    if (satsys(j + 1, NULL) != SYS_GAL) continue;
    if ((pcv = searchpcv(j + 1, "", t, &pcvs))) {
      nav->pcvs[j] = *pcv;
    }
    else {
      char id[64];
      satno2id(j + 1, id);
      fprintf(stderr, "Warning: could not find PCV for %s\n", id);
    }
  }

  /* assign carrier wavelengths */
  for (int i = 0; i < MAXSAT; i++) {
    for (j = 0; j < NFREQ; j++) {
      nav->lam[i][j] = satwavelen(i + 1, j, nav);
    }
  }

  double antennas[2][3] = {
    {40.816410, -121.471828, 1000}, // 1h
    {40.818316, -121.470420, 1000}  // 4g
  };
  double dopplers[2] = {0};

  for (int ant = 0; ant < 2; ++ant) {
    pos[0] = antennas[ant][0]/180*PI;
    pos[1] = antennas[ant][1]/180*PI;
    pos[2] = antennas[ant][2];
    pos2ecef(pos,rr);
  
    if (!satpos(t, t, satno(SYS_GAL, 31), EPHOPT_PREC, nav, rs, dts, &var, &svh)) {
      fprintf(stderr, "Could not compute satpos\n");
      exit(1);
    }
    geodist(rs, rr, e);
        
    /* range rate with earth rotation correction and satellite clock drift */
    dopplers[ant] = dot(rs + 3, e, 3) + OMGE/CLIGHT * (rs[4]*rr[0] - rs[3]*rr[1])
      - CLIGHT * dts[1];
  
    printf("Antenna %d -> Doppler = %f\n", ant, dopplers[ant]);
  }

  printf("Doppler difference = %.9f\n", dopplers[0]-dopplers[1]);
  
  free(nav);
  
  return 0;
}
