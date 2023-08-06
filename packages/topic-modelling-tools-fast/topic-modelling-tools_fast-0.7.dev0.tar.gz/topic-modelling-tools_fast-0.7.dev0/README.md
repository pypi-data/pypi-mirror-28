# topic-modelling-tools
Topic Modelling with Latent Dirichlet Allocation using Gibbs sampling.
This version of the package uses the GNU Scientific Library for random number
generation, providing faster performance than numpy.

by Stephen Hansen, stephen.hansen@economics.ox.ac.uk
Associate Professor of Economics, University of Oxford

Python/Cython code for cleaning text and estimating LDA via collapsed Gibbs sampling as in Griffiths and Steyvers (2004).

Tutorial scripts and notebooks making use of this library, along with some
example data, can be found in:
https://github.com/sekhansen/text-mining-tutorial


## Installation instructions

This version of the package requires the GNU Scientific Library (GSL) to be
installed.  You can download GSL from ftp://ftp.gnu.org/gnu/gsl/ or 
for Mac OSX using homebrew, you can do `brew install gsl`. If you have conda,
do `conda install gsl`.  

(For a version that doesn't require GSL (but is somewhat slower), checkout the
"master" branch of this repository, or `pip install topic-modelling-tools`.)

If you already have GSL, Python and pip installed, `pip install topic-modelling-tools_gsl`
should work.  The package depends on some other python libraries such as
numpy and nltk but this should be taken care of by pip.

The only other requirement is that a C++ compiler is needed to build the Cython
code.  For Mac OS X you can download Xcode command-line tools,
while for Windows you can download the Visual Studio C++ compiler.

