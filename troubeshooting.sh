#!/bin/bash
#More details at: https://asia.ensembl.org/info/docs/tools/vep/script/vep_download.html

#export current working directory
export cwd=$(pwd)
#export lof paths
export LOF="$cwd/loftee"
export VEP_PATH=$LOF/vep
export VEP_DATA=$LOF/vep_data
export VER=106
export PERL5LIB=$VEP_PATH:$PERL5LIB
export PATH=$VEP_PATH/htslib:$PATH
export PERL5LIB=$VEP_PATH
export PATH="$VEP_PATH/htslib:$PATH"
#export PATH=$HOME/vep/samtools/bin:$PATH
export PERL_BASE="$LOF/perl"
export PERL5LIB="$PERL_BASE/perl-5.24.1/lib/perl5:$PERL_BASE/perl-5.24.1/lib/perl5/x86_64-linux:$PERL5LIB"
export PATH="$PERL_BASE/perl-5.24.1/bin:$PATH"
export PATH="$VEP_PATH:$PATH"
export KENT_SRC=$LOF/kent-335_base/src
export MACHTYPE=$(uname -m)
export CFLAGS="-fPIC"
export MYSQLINC='mysql_config --include | sed -e 's/^-I//g''
export MYSQLLIBS='mysql_config --libs'
export PERL5LIB=$PERL5LIB:$PERL_BASE/cpanm/lib/perl5

#troubleshooting
export KENT_SRC=$LOF/kent-335_base/src
export MACHTYPE=$(uname -m)
export CFLAGS="-fPIC"
export MYSQLINC='mysql_config --include | sed -e 's/^-I//g''
export MYSQLLIBS='mysql_config --libs'
cd $KENT_SRC/lib
echo 'CFLAGS="-fPIC"' > ../inc/localEnvironment.mk
make clean && make
cd ../jkOwnLib
make clean && make

mkdir $PERL_BASE/cpanm/
cpanm -l $PERL_BASE/cpanm Bio::DB::BigFile
cpanm -l $PERL_BASE/cpanm List::MoreUtils
cpanm -l $PERL_BASE/cpanm DBD::SQLite
export PERL5LIB=$PERL5LIB:$PERL_BASE/cpanm/lib/perl5

cd $cwd
