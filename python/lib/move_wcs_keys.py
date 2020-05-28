from astropy.io import fits
from glob import glob

input = raw_input('Enter file name(s): ')
files = glob(input)

keys = ['radesys', 'pa_aper', 'va_scale',
        'wcsaxes',
        'crpix1', 'crpix2', 'crpix3',
        'crval1', 'crval2', 'crval3',
        'cdelt1', 'cdelt2', 'cdelt3',
        'cunit1', 'cunit2', 'cunit3',
        'ctype1', 'ctype2', 'ctype3',
        'pc1_1', 'pc1_2', 'pc1_3',
        'pc2_1', 'pc2_2', 'pc2_3',
        'pc3_1', 'pc3_2', 'pc3_3',
        's_region', 'wavstart', 'wavend', 'sporder',
        'v2_ref', 'v3_ref', 'vparity', 'v3i_yang',
        'ra_ref', 'dec_ref', 'roll_ref',
        'ra_v1', 'dec_v1', 'pa_v3']

for f in files:

    print('Working on file %s' % f)
    fd = fits.open(f, mode='update')

    for key in keys:
        try:
            value = fd[0].header[key]
            fd[1].header[key] = value
            fd[0].header.remove(key)
        except:
            pass

    fd.close()
