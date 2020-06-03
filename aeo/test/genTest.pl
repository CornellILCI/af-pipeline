#!/usr/bin/perl -w
use strict;
use Getopt::Std;

# genTest.pl -- script to generate JSON request files.
# 2019.02
# Victor Jun M. Ulat 
# v.ulat@cgiar.org

# -n  number of request files to generate
#     i.e. -n 10
# -c  copy to ../input
#     i.e. -c y (n for no)
# -t  request type (alpha, rowcol, rcbd, random)
#     i.e. -t alpha (generate alpha-lattice request files)

my $root="$ENV{'PYSIMBA_ROOT'}";
my %args=();
getopt("nct:", \%args);

my $argN = keys %args;

if ($argN<3){
  # print message here...
  print "\n\tError: Insufficient arguments!\n";
  print "\tUsage: $0 -n 10 -t rcbd -c y\n";
  print "\t Note: -t random does not include asreml.\n\n";
  exit();
}

my $i=1;
my @designs=();
my @temp=`ls -1 $root/test/*.tmpl`;
foreach my $e(@temp){
  if ($e!~/(ASREML)|(runSEA)/){
    push(@designs, $e);
  }
}


while ($i <= $args{n}){
  my $filename=genFN();

  # randomize between with and without layout
  my $wl=genRN('1','2');
  my $lo='';

  if ($wl==1){
    $lo='nl';
  } elsif ($wl==2){
    $lo='wl';
  }

  my $rq='';

  if ($args{'t'} eq 'rcbd'){
    $rq='RCBD';
  } elsif ($args{'t'} eq 'rowcol') {
    $rq='RWCL';
  } elsif ($args{'t'} eq 'augrcbd'){
    $rq='AUGR';
  } elsif ($args{'t'} eq 'alpha'){
    $rq='ALPH';
  } elsif ($args{'t'} eq 'random') {
    $rq=$designs[rand @designs];
    chomp $rq;
    $rq=~s/.+?\///g;
    $rq=~s/(n|w)l\.tmpl//g;
  } elsif ($args{'t'} eq 'asreml') {
    $filename=~s/\_SD\_/\_SA\_/g;
    $rq='ASREML';
    $lo='';
  } else {
    print "\n\tError: \"$args{'t'}\" ".
          "unrecognized design.\n".
          "\tDesigns: rcbd, rowcol, ".
          "augrcbd, alpha, random\n\n";
    exit();
  }

  my $tag=uc($rq.$lo);
  
  $filename.="_".$tag;
  my $dir='';
  $dir=$filename;

  if ($args{'t'} eq 'asreml') {
    `mkdir $dir`;
    $filename=$filename."/".$filename;
  }

  $filename.=".JSON";
  
  $rq.=$lo.".tmpl";
  my $cn=genCN($rq);

  if ($args{'t'} eq 'asreml'){
    my $anID=$dir.".1";
    $cn=~s/\[ANID\]/$anID/g;
    my $dt1=$anID.".1.1.dt";
    my $dt2=$anID.".1.2.dt";
    my $as1=$anID.".1.1.as";
    my $as2=$anID.".1.2.as";
    `cp ASREMLas.tmpl $dir/$as1`;
    `sed -i 's/INPUTDT/$dt1/g' $dir/$as1`;
    `cp ASREMLas.tmpl $dir/$as2`;
    `sed -i 's/INPUTDT/$dt2/g' $dir/$as2`;
    `cp ASREMLdt.tmpl $dir/$dt1`;
    `cp ASREMLdt.tmpl $dir/$dt2`;
  }

  open TEST, ">$filename" or 
       die "Cannot open $filename: $!";
  print TEST $cn;
  close TEST; 
  $i++; 
}

if ($args{'c'} eq 'y') {
  if ($args{'t'} eq 'asreml'){
    `mv $root/test/*_ASREML $root/input/`;
  } else {
    `mv $root/test/*.JSON $root/input/`;
  }
}

exit();

sub genCN {
  my ($rq)=@_;
  my $ts=genTS();
  my $id=genRI();
  my $ri=genRN('1','2000');
  my $content='';

  open TMPL, "$root/test/$rq" or 
       die "Cannot open $root/test/$rq: $!";
  
  while (my $line=readline *TMPL) {
    if ($line=~/\[\d+/){
      my $tmp=$line;
      chomp $tmp;
      $tmp=~s/.+?\[//g;
      $tmp=~s/\].+//g;
      my ($min,$max)=split(/\|/, $tmp);
      my $value=genRN($min,$max);
      $line=~s/\[.+?\]/$value/g;
    }
    $content.=$line;
  }  

  $content=~s/\[RQTS\]/$ts/g;
  $content=~s/\[RRID\]/$ri/g;
  $content=~s/\[RQID\]/$id/g; 
  
  if($args{'t'} eq 'asreml') {
    $ri=genRN('500','50000');
    $ri=$ri."ASReml";
    $content=~s/\[RMDL\]/$ri/g;
  }
    
  return ($content);
}
sub genFN {
  my @e=localtime(time);
  my @chars=("A".."Z","0".."9");
  my @nums=("0".."9");
  my $str1;
  my $str2;
  $str1.=$chars[rand @chars] for 1..7;
  $str2.=$nums[rand @nums] for 1..5;
  my $fn=$e[5]+1900;
  $fn.=$str1."_SD_".$str2;
  return($fn);
}

sub genTS {
  my @e=localtime(time);
  my $yr=$e[5]+1900;
  my $ts=$yr."-".sprintf("%02d", $e[4])."-".$e[3];
  $ts.="T".sprintf("%02d", $e[2]).":"
          .sprintf("%02d", $e[1]).":"
          .sprintf("%02d", $e[0])."+08:00";
  return($ts);
}

sub genRN {
  my ($min, $max)=@_;
  my @nums=("$min".."$max");
  my $rn;
  $rn=$nums[rand @nums];
  return ($rn);
}

sub genRI {
  my @e=localtime(time);
  my $yr=$e[5]+1900;
  my @nums=("0".."9");
  my $id;
  $id.=$nums[rand @nums] for 1..7;
  my $ri="TDSGN-";
  $ri.=$yr."-".sprintf("%02d",$e[4])."-"
       .sprintf("%02d",$e[3])."-".$id;
  return($ri);
}
