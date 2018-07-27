#include <sndfile.h>
#include <fftw3.h>
#include <cmath>
#include <cstring>
#include <iostream>
#include <vector>
#define _USE_MATH_DEFINES


using namespace std;

void spectrogram(double *samples, int len_samples, int fft_length = 256, int sample_rate = 2, int hop_length = 128)
{
	fftw_cleanup();
	double *window = new double[fft_length];
	for (int i = 0; i < fft_length; ++i)
		window[i] = 0.5 - 0.5 * cos(2 * i * M_PI / (fft_length - 1));
	
	double window_norm = 0.0f;
	for (int i = 0; i < fft_length; ++i)
		window_norm += window[i] * window[i];
	
	double scale = window_norm * sample_rate;
	int trunc = (len_samples - fft_length) % hop_length;
	
	int len_x = len_samples - trunc;
	
	double *x = new double[len_x];
	memcpy(x, samples, (len_samples - trunc) * sizeof(double));
	
	// as_strided
	
	int shape_1 = (len_x - fft_length) / hop_length + 1;

	int shape_2 = (fft_length / 2) + 1;
	
	double *nx = (double*) fftw_malloc(sizeof(double) * (fft_length * shape_1));

	for (int i = 0; i < fft_length; ++i)
		for (int j = 0; j < shape_1; ++j)
			
			nx[i + j * fft_length] = x[i + j * hop_length] * window[i];
	
	delete []x;
	
	fftw_complex *out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * shape_2 * shape_1);

	for (int i = 0; i < shape_1; ++i)
	{
		fftw_plan plan = fftw_plan_dft_r2c_1d(fft_length, nx + fft_length * i, out + shape_2 * i, FFTW_ESTIMATE);
		fftw_execute(plan);
		fftw_destroy_plan(plan);
	}
	
	double *result = new double[shape_2 * shape_1];
	for (int i = 0; i < shape_2 * shape_1; ++i)
		result[i] = (out[i][0] * out[i][0] + out[i][1] * out[i][1])/ scale * 2;
	
	fftw_free(out);
	
	for (int i = 0; i < shape_1; ++i)
	{
		result[(i + 1) * shape_2 - 1] /= 2;
		result[i * shape_2] /= 2;
	}
	
	//for (int i = 0; i < shape_1 * shape_2; ++i)
	//	cout<<result[i]<<endl;
	
	double *freqs = new double[shape_2];
	for (int i = 0; i < shape_2; ++i)
		freqs[i] = double(sample_rate) / fft_length * i;
	
	//for(int i = 0; i < shape_2; ++i)
	//	cout<<freqs[i]<<endl;
}



int main()
{
	SF_INFO info;
	SNDFILE *f;
	f = sf_open("1.wav", SFM_READ, &info);
	if(f == NULL)
		return -1;
	int len_samples = info.frames;
	double *a = new double[len_samples];
	sf_readf_double(f, a, len_samples);
	
	int fft_length = 320;
	int sample_rate = 16000;
	int hop_length = 160;
	
	spectrogram(a, len_samples, 320, sample_rate, hop_length);
	
	delete []a;
	sf_close(f);
	return 0;
}