#include <iostream>
#include <vector>

std::vector<int> get_frame_counts(float maxRandDelay, float startTime, float dt) {
  std::vector<int> fc((startTime + maxRandDelay) * 60 + 2);
  for (int i = 0; i < 65536; i++) {
    float rDt = (float)i / 65535;
    float time = (maxRandDelay * rDt) + startTime;
    int nframes = 0;
    while (time > 0) {
      nframes++;
      time -= dt;
    }
    fc[nframes]++;
  }
  return fc;
}

int main() {
  std::vector<int> fc_1 = get_frame_counts(5., 8., 1./60);
  std::vector<int> fc_2 = get_frame_counts(10., 15., 1./60);
  std::vector<int> fc_3 = get_frame_counts(10., 15., 1./60);
  std::vector<int> fc_4 = get_frame_counts(10., 15., 1./60);
  std::vector<unsigned long long> fct_2(fc_1.size() + fc_2.size());
  std::vector<unsigned long long> fct_3(fct_2.size() + fc_3.size());
  std::vector<unsigned long long> fct_4(fct_3.size() + fc_4.size());

  for (int i = 0; i < fc_1.size(); i++)
    for (int j = 0; j < fc_2.size(); j++)
      fct_2[i + j] += fc_1[i] * fc_2[j];
  for (int i = 0; i < fct_2.size(); i++)
    for (int j = 0; j < fc_3.size(); j++)
      fct_3[i + j] += fct_2[i] * fc_3[j];
  for (int i = 0; i < fct_3.size(); i++)
    for (int j = 0; j < fc_4.size(); j++)
      fct_4[i + j] += fct_3[i] * fc_4[j];

  unsigned __int128 total = 0;
  for (int i = 0; i < fct_4.size(); i++)
    total += fct_4[i];

  FILE* outFile;
  outFile = fopen("i_drone.txt", "w");
  fprintf(outFile, "  %6s  %7s  %17s  %21s  %21s  %21s  %17s  %22s\n", "Frames", "Seconds", "Occurrences", "PDF", "CDF", "1-CDF", "1/CDF", "1/(1-CDF)");
  unsigned __int128 cval = 0;
  for (int i = 0; i < fct_4.size(); i++) {
    unsigned long long val = fct_4[i];
    if (val == 0) continue;
    double cprob2 = (double)(total - cval) / total;
    double icprob2 = (double)total / (total - cval);
    cval += val;
    double seconds = (double)i / 60;
    double prob = (double)val / total;
    double cprob1 = (double)cval / total;
    double icprob1 = (double)total / cval;
    fprintf(outFile, "  %6d  %7.4f  %17llu  %21.15e  %21.15e  %21.15e  %17.2f  %22.2f\n", i, seconds, val, prob, cprob1, cprob2, icprob1, icprob2);
  }

  return 0;
}
