#!/bin/bash
#More details at: https://asia.ensembl.org/info/docs/tools/vep/script/vep_download.html

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
