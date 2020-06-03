#!/usr/bin/perl -w
use strict;

# genSLURMconf.pl -- script to generate slurm.conf from
#                    slurm.tmpl
# Reads hostname and cpu information from shell utilities:
# hostname and lscpu. Note: This only for single node
# (master and slave in one machine) configuration only.
#
# 2019.03.01
# Victor Jun M. Ulat, CIMMYT
# v.ulat@cgiar.org

my $tmpl='slurm.tmpl';
my $conf='slurm.conf';
my $hostname=$ARGV[0] // `hostname`;
chomp $hostname;

my $content='';

open TMPL, $tmpl or die "Cannot open $tmpl: $!";
while (my $line=readline *TMPL){
  $content.=$line;
}

close TMPL;

my $socketN=0;
my $coresPerSocket=0;
my $threadsPerCore=0;

my @cpuInfo=`lscpu`;

foreach my $c (@cpuInfo) {
  chomp $c;
  if ($c=~/^Core/) {
    ($coresPerSocket=$c)=~s/Core.+?\s{2,}//g;
  }
  if ($c=~/^Socket/){
    ($socketN=$c)=~s/Socket.+?\s{2,}//g;
  }
  if ($c=~/^Thread/){
    ($threadsPerCore=$c)=~s/Thread.+?\s{2,}//g;
  }
}

$content=~s/\[HOSTNAME\]/$hostname/g;
$content=~s/\[SOCKET\]/$socketN/g;
$content=~s/\[CORESPERSOCKET\]/$coresPerSocket/g;
$content=~s/\[THREADSPERCORE\]/$threadsPerCore/g;

open CONF, ">$conf" or die "Cannot open $conf: $!";

print CONF $content;

close CONF;

exit();

