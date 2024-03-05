import pytest


@pytest.fixture
def sample_asreml_result_string_1():
    return """<?xml version="1.0" encoding="utf-8" ?>
 <ASReport>
  <Version>  ASReml 4.1 [28 Dec 2014] </Version>
  <Build> my [03 Apr 2019]   64 bit  Windows x64 </Build>
  <Title> 68ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ab_SA_1001 </Title>
  <StartTime> 17 Jun 2021 16:07:26.026 </StartTime>
  <Cycle>
   <CycleNumber> 1 </CycleNumber>
   <DataSummary>
    <Variable>
     <Vnumber> 1 </Vnumber>
     <Vname> loc </Vname>
     <Vlevel> 1 </Vlevel>
   </Variable> <Variable>
     <Vnumber> 2 </Vnumber>
     <Vname> expt </Vname>
     <Vlevel> 1 </Vlevel>
   </Variable> <Variable>
     <Vnumber> 3 </Vnumber>
     <Vname> entry </Vname>
     <Vlevel> 180 </Vlevel>
   </Variable> <Variable>
     <Vnumber> 4 </Vnumber>
     <Vname> plot </Vname>
     <Vlevel> 420 </Vlevel>
   </Variable> <Variable>
     <Vnumber> 5 </Vnumber>
     <Vname> col </Vname>
     <Vlevel> 15 </Vlevel>
   </Variable> <Variable>
     <Vnumber> 6 </Vnumber>
     <Vname> row </Vname>
     <Vlevel> 28 </Vlevel>
   </Variable> <Variable>
     <Vnumber> 7 </Vnumber>
     <Vname> rep </Vname>
     <Vlevel> 2 </Vlevel>
   </Variable> <Variable>
     <Vnumber> 8 </Vnumber>
     <Vname> yield </Vname>
     <NumberMissing> 2 </NumberMissing>
     <NumberZero> 0 </NumberZero>
     <Minimum>       2.4411 </Minimum>
     <Mean>       6.6178 </Mean>
     <Maximum>      12.3619 </Maximum>
     <StndDevn>       1.5416 </StndDevn>
   </Variable> <Variable>
     <Vnumber> 9 </Vnumber>
     <Vname> mu </Vname>
     <Vlevel> 1 </Vlevel>
   </Variable> <Variable>
     <Vnumber> 10 </Vnumber>
     <Vname> mv_estimates </Vname>
     <Vlevel> 2 </Vlevel>
    </Variable >
   </DataSummary >
   <Predict_01> prediction entry !PRESENT entry !SED !TDIFF </Predict_01>
   <Iteration>
    <ItrtnNumber> 1 </ItrtnNumber>
    <REML_LogL>    -392.3842 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 2 </ItrtnNumber>
    <REML_LogL>    -391.5417 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 3 </ItrtnNumber>
    <REML_LogL>    -390.6516 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 4 </ItrtnNumber>
    <REML_LogL>    -390.5962 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 5 </ItrtnNumber>
    <REML_LogL>    -390.5929 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 6 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 7 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 8 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 9 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 10 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 11 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 12 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 13 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 14 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 15 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <Iteration>
    <ItrtnNumber> 16 </ItrtnNumber>
    <REML_LogL>    -390.5927 </REML_LogL>
    <NEDF> 416 </NEDF>
   </Iteration >
   <InformationCriteria>
    <Akaike>     787.1855 </Akaike>
    <Bayesian>     799.2775 </Bayesian>
    <ParameterCount> 3 </ParameterCount>
   </InformationCriteria >
   <PredictTable>
    <Table> 1 </Table>
    <Preamble>
     <TraitName> yield </TraitName>
     <SimpleAveraging>   	rep </SimpleAveraging>
    </Preamble >
    <ClassifySet>
     <Variable_1> entry </Variable_1>
    </ClassifySet >
    <Prow>
     <Cell> 1 </Cell>
     <Identifier> 1 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 2 </Cell>
     <Identifier> 10 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 3 </Cell>
     <Identifier> 100 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 4 </Cell>
     <Identifier> 101 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 5 </Cell>
     <Identifier> 102 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 6 </Cell>
     <Identifier> 103 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 7 </Cell>
     <Identifier> 104 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 8 </Cell>
     <Identifier> 105 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 9 </Cell>
     <Identifier> 106 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 10 </Cell>
     <Identifier> 107 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 11 </Cell>
     <Identifier> 108 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 12 </Cell>
     <Identifier> 109 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 13 </Cell>
     <Identifier> 11 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 14 </Cell>
     <Identifier> 110 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 15 </Cell>
     <Identifier> 111 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 16 </Cell>
     <Identifier> 112 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 17 </Cell>
     <Identifier> 113 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 18 </Cell>
     <Identifier> 114 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 19 </Cell>
     <Identifier> 115 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 20 </Cell>
     <Identifier> 116 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 21 </Cell>
     <Identifier> 117 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 22 </Cell>
     <Identifier> 118 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 23 </Cell>
     <Identifier> 119 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 24 </Cell>
     <Identifier> 12 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 25 </Cell>
     <Identifier> 120 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 26 </Cell>
     <Identifier> 121 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 27 </Cell>
     <Identifier> 122 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 28 </Cell>
     <Identifier> 123 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 29 </Cell>
     <Identifier> 124 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 30 </Cell>
     <Identifier> 125 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 31 </Cell>
     <Identifier> 126 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 32 </Cell>
     <Identifier> 127 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 33 </Cell>
     <Identifier> 128 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 34 </Cell>
     <Identifier> 129 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 35 </Cell>
     <Identifier> 13 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 36 </Cell>
     <Identifier> 130 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 37 </Cell>
     <Identifier> 131 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 38 </Cell>
     <Identifier> 132 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 39 </Cell>
     <Identifier> 133 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 40 </Cell>
     <Identifier> 134 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 41 </Cell>
     <Identifier> 135 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 42 </Cell>
     <Identifier> 136 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 43 </Cell>
     <Identifier> 137 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 44 </Cell>
     <Identifier> 138 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 45 </Cell>
     <Identifier> 139 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 46 </Cell>
     <Identifier> 14 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 47 </Cell>
     <Identifier> 140 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 48 </Cell>
     <Identifier> 141 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 49 </Cell>
     <Identifier> 142 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 50 </Cell>
     <Identifier> 143 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 51 </Cell>
     <Identifier> 144 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 52 </Cell>
     <Identifier> 145 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 53 </Cell>
     <Identifier> 146 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 54 </Cell>
     <Identifier> 147 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 55 </Cell>
     <Identifier> 148 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 56 </Cell>
     <Identifier> 149 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 57 </Cell>
     <Identifier> 15 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 58 </Cell>
     <Identifier> 150 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 59 </Cell>
     <Identifier> 151 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 60 </Cell>
     <Identifier> 152 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 61 </Cell>
     <Identifier> 153 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 62 </Cell>
     <Identifier> 154 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 63 </Cell>
     <Identifier> 155 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 64 </Cell>
     <Identifier> 156 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 65 </Cell>
     <Identifier> 157 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 66 </Cell>
     <Identifier> 158 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 67 </Cell>
     <Identifier> 159 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 68 </Cell>
     <Identifier> 16 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 69 </Cell>
     <Identifier> 160 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 70 </Cell>
     <Identifier> 161 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 71 </Cell>
     <Identifier> 162 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 72 </Cell>
     <Identifier> 163 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 73 </Cell>
     <Identifier> 164 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 74 </Cell>
     <Identifier> 165 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 75 </Cell>
     <Identifier> 166 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 76 </Cell>
     <Identifier> 167 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 77 </Cell>
     <Identifier> 168 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 78 </Cell>
     <Identifier> 169 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 79 </Cell>
     <Identifier> 17 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 80 </Cell>
     <Identifier> 170 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 81 </Cell>
     <Identifier> 171 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 82 </Cell>
     <Identifier> 172 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 83 </Cell>
     <Identifier> 173 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 84 </Cell>
     <Identifier> 174 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 85 </Cell>
     <Identifier> 175 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 86 </Cell>
     <Identifier> 176 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 87 </Cell>
     <Identifier> 177 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 88 </Cell>
     <Identifier> 178 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 89 </Cell>
     <Identifier> 179 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 90 </Cell>
     <Identifier> 18 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 91 </Cell>
     <Identifier> 180 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 92 </Cell>
     <Identifier> 19 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 93 </Cell>
     <Identifier> 2 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 94 </Cell>
     <Identifier> 20 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 95 </Cell>
     <Identifier> 21 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 96 </Cell>
     <Identifier> 22 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 97 </Cell>
     <Identifier> 23 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 98 </Cell>
     <Identifier> 24 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 99 </Cell>
     <Identifier> 25 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 100 </Cell>
     <Identifier> 26 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 101 </Cell>
     <Identifier> 27 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 102 </Cell>
     <Identifier> 28 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 103 </Cell>
     <Identifier> 29 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 104 </Cell>
     <Identifier> 3 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 105 </Cell>
     <Identifier> 30 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 106 </Cell>
     <Identifier> 31 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 107 </Cell>
     <Identifier> 32 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 108 </Cell>
     <Identifier> 33 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 109 </Cell>
     <Identifier> 34 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 110 </Cell>
     <Identifier> 35 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 111 </Cell>
     <Identifier> 36 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 112 </Cell>
     <Identifier> 37 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 113 </Cell>
     <Identifier> 38 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 114 </Cell>
     <Identifier> 39 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 115 </Cell>
     <Identifier> 4 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 116 </Cell>
     <Identifier> 40 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 117 </Cell>
     <Identifier> 41 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 118 </Cell>
     <Identifier> 42 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 119 </Cell>
     <Identifier> 43 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 120 </Cell>
     <Identifier> 44 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 121 </Cell>
     <Identifier> 45 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 122 </Cell>
     <Identifier> 46 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 123 </Cell>
     <Identifier> 47 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 124 </Cell>
     <Identifier> 48 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 125 </Cell>
     <Identifier> 49 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 126 </Cell>
     <Identifier> 5 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 127 </Cell>
     <Identifier> 50 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 128 </Cell>
     <Identifier> 51 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 129 </Cell>
     <Identifier> 52 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 130 </Cell>
     <Identifier> 53 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 131 </Cell>
     <Identifier> 54 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 132 </Cell>
     <Identifier> 55 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 133 </Cell>
     <Identifier> 56 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 134 </Cell>
     <Identifier> 57 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 135 </Cell>
     <Identifier> 58 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 136 </Cell>
     <Identifier> 59 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 137 </Cell>
     <Identifier> 6 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 138 </Cell>
     <Identifier> 60 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 139 </Cell>
     <Identifier> 61 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 140 </Cell>
     <Identifier> 62 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 141 </Cell>
     <Identifier> 63 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 142 </Cell>
     <Identifier> 64 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 143 </Cell>
     <Identifier> 65 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 144 </Cell>
     <Identifier> 66 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 145 </Cell>
     <Identifier> 67 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 146 </Cell>
     <Identifier> 68 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 147 </Cell>
     <Identifier> 69 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 148 </Cell>
     <Identifier> 7 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 149 </Cell>
     <Identifier> 70 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 150 </Cell>
     <Identifier> 71 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 151 </Cell>
     <Identifier> 72 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 152 </Cell>
     <Identifier> 73 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 153 </Cell>
     <Identifier> 74 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 154 </Cell>
     <Identifier> 75 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 155 </Cell>
     <Identifier> 76 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 156 </Cell>
     <Identifier> 77 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 157 </Cell>
     <Identifier> 78 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 158 </Cell>
     <Identifier> 79 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 159 </Cell>
     <Identifier> 8 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 160 </Cell>
     <Identifier> 80 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 161 </Cell>
     <Identifier> 81 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 162 </Cell>
     <Identifier> 82 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 163 </Cell>
     <Identifier> 83 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 164 </Cell>
     <Identifier> 84 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 165 </Cell>
     <Identifier> 85 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 166 </Cell>
     <Identifier> 86 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 167 </Cell>
     <Identifier> 87 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 168 </Cell>
     <Identifier> 88 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 169 </Cell>
     <Identifier> 89 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 170 </Cell>
     <Identifier> 9 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 171 </Cell>
     <Identifier> 90 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 172 </Cell>
     <Identifier> 91 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 173 </Cell>
     <Identifier> 92 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 174 </Cell>
     <Identifier> 93 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 175 </Cell>
     <Identifier> 94 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 176 </Cell>
     <Identifier> 95 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 177 </Cell>
     <Identifier> 96 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 178 </Cell>
     <Identifier> 97 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 179 </Cell>
     <Identifier> 98 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
   </Prow> <Prow>
     <Cell> 180 </Cell>
     <Identifier> 99 </Identifier>
     <PredValue>       6.6159 </PredValue>
     <StndErr>    0.0846111 </StndErr>
     <EPcode>  E </EPcode>
    </Prow >
   </PredictTable >
   <VarianceComponents>
    <VParameter>
     <ParameterIndex> 4 </ParameterIndex>
     <SourceModel> entry                   IDV_V  180 </SourceModel>
     <Source> entry </Source>
     <VCStructure> IDV_V </VCStructure>
     <ParameterType> Gamma </ParameterType>
     <Levels> 180 </Levels>
     <Gamma>   0.57920334E-07 </Gamma>
     <VComponent>   0.13792020E-06 </VComponent>
     <ZRatio>    0.0000000 </ZRatio>
     <PCchange> 0 </PCchange>
     <ConstraintCode> B </ConstraintCode>
    </VParameter >
    <VParameter>
     <RSection> 1 </RSection>
     <SourceModel> Residual                SCA_V  420 </SourceModel>
     <Source> Residual </Source>
     <VCStructure> Residual </VCStructure>
     <ParameterType> Variance </ParameterType>
     <Levels> 420 </Levels>
     <Gamma>    1.0000000 </Gamma>
     <VComponent>       2.3812 </VComponent>
     <ZRatio>      14.2072 </ZRatio>
     <PCchange> 0 </PCchange>
     <ConstraintCode> P </ConstraintCode>
    </VParameter >
    <VParameter>
     <RSection> 1 </RSection>
     <ParameterIndex> 6 </ParameterIndex>
     <SourceModel> col                      AR_R    1 </SourceModel>
     <Source> Residual [1] </Source>
     <VCStructure> AR_R </VCStructure>
     <ParameterType> Correln </ParameterType>
     <Levels> 1 </Levels>
     <Gamma>    0.1235281 </Gamma>
     <VComponent>    0.1235281 </VComponent>
     <ZRatio>       2.4783 </ZRatio>
     <PCchange> 0 </PCchange>
     <ConstraintCode> P </ConstraintCode>
    </VParameter >
   </VarianceComponents >
   <Solutions>
    <Equation>
     <Model_Term> rep </Model_Term>
     <Level> 1 </Level>
     <Effect>    0.0000000 </Effect>
     <seEffect>    0.0000000 </seEffect>
     <GiEffect>    0.0000000 </GiEffect>
     <AOMstat>    0.0000000 </AOMstat>
   </Equation> <Equation>
     <Model_Term> rep </Model_Term>
     <Level> 2 </Level>
     <Effect>   -0.1870020 </Effect>
     <seEffect>    0.1692207 </seEffect>
     <GiEffect>    0.0000000 </GiEffect>
     <AOMstat>    0.0000000 </AOMstat>
   </Equation> <Equation>
     <Model_Term> mu </Model_Term>
     <Level>          1 </Level>
     <Effect>       6.7094 </Effect>
     <seEffect>    0.1196571 </seEffect>
     <GiEffect>    0.0000000 </GiEffect>
     <AOMstat>    0.0000000 </AOMstat>
   </Equation> <Equation>
     <Model_Term> mv_estimates </Model_Term>
     <Level>          1 </Level>
     <Effect>       6.1994 </Effect>
     <seEffect>       1.5224 </seEffect>
     <GiEffect>    0.0000000 </GiEffect>
     <AOMstat>    0.0000000 </AOMstat>
   </Equation> <Equation>
     <Model_Term> mv_estimates </Model_Term>
     <Level>          2 </Level>
     <Effect>       6.0515 </Effect>
     <seEffect>       1.5224 </seEffect>
     <GiEffect>    0.0000000 </GiEffect>
     <AOMstat>    0.0000000 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 1 </Level>
     <Effect>   0.71486509E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.5183179 </GiEffect>
     <AOMstat>    0.5579872 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 10 </Level>
     <Effect>  -0.16400554E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.1891 </GiEffect>
     <AOMstat>      -1.2801 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 100 </Level>
     <Effect>   0.54884241E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.3979420 </GiEffect>
     <AOMstat>    0.4283984 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 101 </Level>
     <Effect>  -0.50577342E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3667145 </GiEffect>
     <AOMstat>   -0.3947809 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 102 </Level>
     <Effect>  -0.15628802E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.1332 </GiEffect>
     <AOMstat>      -1.2199 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 103 </Level>
     <Effect>  -0.10430029E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.7562365 </GiEffect>
     <AOMstat>   -0.8141148 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 104 </Level>
     <Effect>  -0.13181953E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.9557667 </GiEffect>
     <AOMstat>      -1.0331 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 105 </Level>
     <Effect>   0.12359094E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.8961048 </GiEffect>
     <AOMstat>    0.9646878 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 106 </Level>
     <Effect>  -0.13655230E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.9900820 </GiEffect>
     <AOMstat>      -1.0659 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 107 </Level>
     <Effect>   0.18500197E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.3414 </GiEffect>
     <AOMstat>       1.4440 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 108 </Level>
     <Effect>   0.32476924E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2354762 </GiEffect>
     <AOMstat>    0.2545285 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 109 </Level>
     <Effect>   0.75767479E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.5493574 </GiEffect>
     <AOMstat>    0.5914023 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 11 </Level>
     <Effect>  -0.10425842E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.7559329 </GiEffect>
     <AOMstat>   -0.8170954 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 110 </Level>
     <Effect>  -0.39135827E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.2837570 </GiEffect>
     <AOMstat>   -0.3054743 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 111 </Level>
     <Effect>  -0.13191067E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.9564275 </GiEffect>
     <AOMstat>      -1.0296 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 112 </Level>
     <Effect>   0.11458860E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.8308326 </GiEffect>
     <AOMstat>    0.8944201 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 113 </Level>
     <Effect>   0.13899175E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.0078 </GiEffect>
     <AOMstat>       1.0893 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 114 </Level>
     <Effect>   0.46672442E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.3384018 </GiEffect>
     <AOMstat>    0.3643012 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 115 </Level>
     <Effect>  -0.70217455E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.5091166 </GiEffect>
     <AOMstat>   -0.5480816 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 116 </Level>
     <Effect>   0.24884843E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1804293 </GiEffect>
     <AOMstat>    0.1942384 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 117 </Level>
     <Effect>  -0.99840010E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.7238970 </GiEffect>
     <AOMstat>   -0.7793001 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 118 </Level>
     <Effect>  -0.85819757E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.6222421 </GiEffect>
     <AOMstat>   -0.6725877 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 119 </Level>
     <Effect>  -0.12448041E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0902554 </GiEffect>
     <AOMstat>   -0.0971631 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 12 </Level>
     <Effect>  -0.45178133E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3275672 </GiEffect>
     <AOMstat>   -0.3526374 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 120 </Level>
     <Effect>  -0.18719356E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.3573 </GiEffect>
     <AOMstat>      -1.4611 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 121 </Level>
     <Effect>   0.12762815E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.9253768 </GiEffect>
     <AOMstat>       1.0002 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 122 </Level>
     <Effect>  -0.52242939E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3787911 </GiEffect>
     <AOMstat>   -0.4077817 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 123 </Level>
     <Effect>   0.39179317E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       2.8407 </GiEffect>
     <AOMstat>       3.0706 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 124 </Level>
     <Effect>   0.29572235E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       2.1442 </GiEffect>
     <AOMstat>       2.3176 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 125 </Level>
     <Effect>   0.10258866E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.7438262 </GiEffect>
     <AOMstat>    0.8040091 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 126 </Level>
     <Effect>  -0.19402047E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.4068 </GiEffect>
     <AOMstat>      -1.5206 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 127 </Level>
     <Effect>  -0.11235886E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.8146658 </GiEffect>
     <AOMstat>   -0.8805803 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 128 </Level>
     <Effect>   0.73981576E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.0536409 </GiEffect>
     <AOMstat>    0.0577462 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 129 </Level>
     <Effect>  -0.66009533E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.4786067 </GiEffect>
     <AOMstat>   -0.5152367 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 13 </Level>
     <Effect>  -0.73673936E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.5341780 </GiEffect>
     <AOMstat>   -0.5750611 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 130 </Level>
     <Effect>  -0.14782410E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.0718 </GiEffect>
     <AOMstat>      -1.1538 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 131 </Level>
     <Effect>   0.16644853E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.2068 </GiEffect>
     <AOMstat>       1.2992 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 132 </Level>
     <Effect>   0.11905089E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.8631868 </GiEffect>
     <AOMstat>    0.9292505 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 133 </Level>
     <Effect>   0.28023630E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       2.0319 </GiEffect>
     <AOMstat>       2.1874 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 134 </Level>
     <Effect>   0.18537091E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.3440 </GiEffect>
     <AOMstat>       1.4469 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 135 </Level>
     <Effect>  -0.17665901E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.2809 </GiEffect>
     <AOMstat>      -1.3845 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 136 </Level>
     <Effect>   0.36396313E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2638940 </GiEffect>
     <AOMstat>    0.2852456 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 137 </Level>
     <Effect>  -0.43938760E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0318581 </GiEffect>
     <AOMstat>   -0.0342964 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 138 </Level>
     <Effect>  -0.10389193E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.7532757 </GiEffect>
     <AOMstat>   -0.8109274 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 139 </Level>
     <Effect>  -0.19962282E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.4474 </GiEffect>
     <AOMstat>      -1.5645 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 14 </Level>
     <Effect>  -0.12235059E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.8871115 </GiEffect>
     <AOMstat>   -0.9550062 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 140 </Level>
     <Effect>  -0.15698884E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.1383 </GiEffect>
     <AOMstat>      -1.2254 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 141 </Level>
     <Effect>   0.23331417E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.6917 </GiEffect>
     <AOMstat>       1.8211 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 142 </Level>
     <Effect>   0.44633388E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.3236175 </GiEffect>
     <AOMstat>    0.3483854 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 143 </Level>
     <Effect>  -0.15660173E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.1355 </GiEffect>
     <AOMstat>      -1.2224 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 144 </Level>
     <Effect>   0.41123889E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2981716 </GiEffect>
     <AOMstat>    0.3222967 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 145 </Level>
     <Effect>  -0.27391825E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.9861 </GiEffect>
     <AOMstat>      -2.1381 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 146 </Level>
     <Effect>   0.34988935E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2536897 </GiEffect>
     <AOMstat>    0.2731058 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 147 </Level>
     <Effect>   0.45087741E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.3269118 </GiEffect>
     <AOMstat>    0.3533622 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 148 </Level>
     <Effect>   0.34715540E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2517074 </GiEffect>
     <AOMstat>    0.2720731 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 149 </Level>
     <Effect>  -0.40368322E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.2926933 </GiEffect>
     <AOMstat>   -0.3163751 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 15 </Level>
     <Effect>   0.70224334E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.5091664 </GiEffect>
     <AOMstat>    0.5481353 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 150 </Level>
     <Effect>   0.47851815E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.3469529 </GiEffect>
     <AOMstat>    0.3735068 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 151 </Level>
     <Effect>   0.17398726E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.2615 </GiEffect>
     <AOMstat>       1.3636 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 152 </Level>
     <Effect>   0.73907830E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.5358739 </GiEffect>
     <AOMstat>    0.5768868 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 153 </Level>
     <Effect>   0.11842701E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.8586633 </GiEffect>
     <AOMstat>    0.9281376 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 154 </Level>
     <Effect>   0.18154383E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.3163 </GiEffect>
     <AOMstat>       1.4170 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 155 </Level>
     <Effect>   0.21683963E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.5722 </GiEffect>
     <AOMstat>       1.6925 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 156 </Level>
     <Effect>   0.91433666E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.0662946 </GiEffect>
     <AOMstat>    0.0713685 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 157 </Level>
     <Effect>   0.16546842E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1199740 </GiEffect>
     <AOMstat>    0.1291562 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 158 </Level>
     <Effect>  -0.15365519E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.1114088 </GiEffect>
     <AOMstat>   -0.1199354 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 159 </Level>
     <Effect>  -0.44739032E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0324383 </GiEffect>
     <AOMstat>   -0.0349210 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 16 </Level>
     <Effect>  -0.49614707E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3597349 </GiEffect>
     <AOMstat>   -0.3888410 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 160 </Level>
     <Effect>  -0.35292883E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.2558935 </GiEffect>
     <AOMstat>   -0.2754782 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 161 </Level>
     <Effect>   0.31115287E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2256036 </GiEffect>
     <AOMstat>    0.2428700 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 162 </Level>
     <Effect>   0.80120309E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.0580918 </GiEffect>
     <AOMstat>    0.0627920 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 163 </Level>
     <Effect>  -0.41652530E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3020046 </GiEffect>
     <AOMstat>   -0.3264397 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 164 </Level>
     <Effect>  -0.37367195E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.2709335 </GiEffect>
     <AOMstat>   -0.2916692 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 165 </Level>
     <Effect>  -0.74836586E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.5426079 </GiEffect>
     <AOMstat>   -0.5841362 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 166 </Level>
     <Effect>  -0.10628919E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.7706571 </GiEffect>
     <AOMstat>   -0.8296391 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 167 </Level>
     <Effect>  -0.33010836E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -2.3935 </GiEffect>
     <AOMstat>      -2.5767 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 168 </Level>
     <Effect>  -0.40401604E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.2929346 </GiEffect>
     <AOMstat>   -0.3153543 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 169 </Level>
     <Effect>   0.17775417E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1288819 </GiEffect>
     <AOMstat>    0.1387458 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 17 </Level>
     <Effect>  -0.20579832E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.4922 </GiEffect>
     <AOMstat>      -1.6127 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 170 </Level>
     <Effect>   0.14322347E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.0385 </GiEffect>
     <AOMstat>       1.1179 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 171 </Level>
     <Effect>   0.87151042E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.6318947 </GiEffect>
     <AOMstat>    0.6830212 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 172 </Level>
     <Effect>  -0.23207754E-06 </Effect>
     <seEffect>   0.37137607E-03 </seEffect>
     <GiEffect>      -1.6827 </GiEffect>
     <AOMstat>      -2.5828 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 173 </Level>
     <Effect>   0.56777031E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.4116658 </GiEffect>
     <AOMstat>    0.4431725 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 174 </Level>
     <Effect>  -0.14017400E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0101634 </GiEffect>
     <AOMstat>   -0.0109413 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 175 </Level>
     <Effect>  -0.17577099E-06 </Effect>
     <seEffect>   0.37137604E-03 </seEffect>
     <GiEffect>      -1.2744 </GiEffect>
     <AOMstat>   -0.9718678 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 176 </Level>
     <Effect>   0.13012459E-06 </Effect>
     <seEffect>   0.37137604E-03 </seEffect>
     <GiEffect>    0.9434774 </GiEffect>
     <AOMstat>    0.7194811 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 177 </Level>
     <Effect>   0.27820837E-06 </Effect>
     <seEffect>   0.37137604E-03 </seEffect>
     <GiEffect>       2.0172 </GiEffect>
     <AOMstat>       1.5383 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 178 </Level>
     <Effect>   0.32355615E-06 </Effect>
     <seEffect>   0.37137587E-03 </seEffect>
     <GiEffect>       2.3460 </GiEffect>
     <AOMstat>    0.8135190 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 179 </Level>
     <Effect>   0.24273848E-06 </Effect>
     <seEffect>   0.37137585E-03 </seEffect>
     <GiEffect>       1.7600 </GiEffect>
     <AOMstat>    0.5835372 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 18 </Level>
     <Effect>   0.17743727E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1286521 </GiEffect>
     <AOMstat>    0.1384985 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 180 </Level>
     <Effect>   0.12571265E-07 </Effect>
     <seEffect>   0.37137590E-03 </seEffect>
     <GiEffect>    0.0911488 </GiEffect>
     <AOMstat>    0.0342105 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 19 </Level>
     <Effect>   0.15385385E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1115528 </GiEffect>
     <AOMstat>    0.1200905 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 2 </Level>
     <Effect>   0.56100118E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.4067578 </GiEffect>
     <AOMstat>    0.4396685 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 20 </Level>
     <Effect>   0.20028207E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.4522 </GiEffect>
     <AOMstat>       1.5633 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 21 </Level>
     <Effect>   0.34096898E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2472219 </GiEffect>
     <AOMstat>    0.2661430 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 22 </Level>
     <Effect>   0.14878238E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.0788 </GiEffect>
     <AOMstat>       1.1613 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 23 </Level>
     <Effect>  -0.10465670E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.7588207 </GiEffect>
     <AOMstat>   -0.8168968 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 24 </Level>
     <Effect>  -0.71458663E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.5181160 </GiEffect>
     <AOMstat>   -0.5577698 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 25 </Level>
     <Effect>  -0.11055540E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.8015896 </GiEffect>
     <AOMstat>   -0.8629390 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 26 </Level>
     <Effect>   0.41231398E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2989511 </GiEffect>
     <AOMstat>    0.3231392 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 27 </Level>
     <Effect>  -0.46079673E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0334104 </GiEffect>
     <AOMstat>   -0.0359674 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 28 </Level>
     <Effect>   0.39913331E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2893944 </GiEffect>
     <AOMstat>    0.3128092 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 29 </Level>
     <Effect>  -0.58543361E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.4244727 </GiEffect>
     <AOMstat>   -0.4569596 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 3 </Level>
     <Effect>   0.27670936E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       2.0063 </GiEffect>
     <AOMstat>       2.1599 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 30 </Level>
     <Effect>   0.20103740E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1457636 </GiEffect>
     <AOMstat>    0.1569195 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 31 </Level>
     <Effect>  -0.17916546E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.2991 </GiEffect>
     <AOMstat>      -1.4042 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 32 </Level>
     <Effect>   0.82168607E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.5957692 </GiEffect>
     <AOMstat>    0.6413662 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 33 </Level>
     <Effect>  -0.26841423E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.1946156 </GiEffect>
     <AOMstat>   -0.2103619 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 34 </Level>
     <Effect>  -0.13499121E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.9787632 </GiEffect>
     <AOMstat>      -1.0579 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 35 </Level>
     <Effect>   0.62601471E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.4538963 </GiEffect>
     <AOMstat>    0.4886351 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 36 </Level>
     <Effect>   0.12864394E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.9327419 </GiEffect>
     <AOMstat>       1.0041 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 37 </Level>
     <Effect>  -0.54051834E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3919066 </GiEffect>
     <AOMstat>   -0.4219010 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 38 </Level>
     <Effect>  -0.17519774E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.2703 </GiEffect>
     <AOMstat>      -1.3675 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 39 </Level>
     <Effect>  -0.71269899E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.5167474 </GiEffect>
     <AOMstat>   -0.5562964 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 4 </Level>
     <Effect>  -0.40598693E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.2943637 </GiEffect>
     <AOMstat>   -0.3181806 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 40 </Level>
     <Effect>  -0.23904662E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.7332 </GiEffect>
     <AOMstat>      -1.8659 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 41 </Level>
     <Effect>   0.18324226E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.3286 </GiEffect>
     <AOMstat>       1.4303 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 42 </Level>
     <Effect>   0.15819716E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.1470 </GiEffect>
     <AOMstat>       1.2348 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 43 </Level>
     <Effect>   0.64171017E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.4652764 </GiEffect>
     <AOMstat>    0.5008862 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 44 </Level>
     <Effect>  -0.24095422E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0174706 </GiEffect>
     <AOMstat>   -0.0188841 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 45 </Level>
     <Effect>   0.21467714E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.5565 </GiEffect>
     <AOMstat>       1.6757 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 46 </Level>
     <Effect>   0.13038280E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.9453496 </GiEffect>
     <AOMstat>       1.0177 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 47 </Level>
     <Effect>   0.26568574E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1926373 </GiEffect>
     <AOMstat>    0.2073807 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 48 </Level>
     <Effect>   0.95953635E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.6957185 </GiEffect>
     <AOMstat>    0.7489651 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 49 </Level>
     <Effect>  -0.27269296E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.9772 </GiEffect>
     <AOMstat>      -2.1285 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 5 </Level>
     <Effect>   0.71747625E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.5202112 </GiEffect>
     <AOMstat>    0.5623014 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 50 </Level>
     <Effect>  -0.22205795E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.6100 </GiEffect>
     <AOMstat>      -1.7403 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 51 </Level>
     <Effect>  -0.40671090E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.2948886 </GiEffect>
     <AOMstat>   -0.3187480 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 52 </Level>
     <Effect>  -0.33984333E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.2464058 </GiEffect>
     <AOMstat>   -0.2652644 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 53 </Level>
     <Effect>   0.13577875E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.0984473 </GiEffect>
     <AOMstat>    0.1064127 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 54 </Level>
     <Effect>   0.26756727E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1940015 </GiEffect>
     <AOMstat>    0.2088494 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 55 </Level>
     <Effect>  -0.26183118E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.8984 </GiEffect>
     <AOMstat>      -2.0520 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 56 </Level>
     <Effect>   0.17471377E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.2668 </GiEffect>
     <AOMstat>       1.3637 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 57 </Level>
     <Effect>  -0.66329401E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.4809259 </GiEffect>
     <AOMstat>   -0.5198376 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 58 </Level>
     <Effect>  -0.60385156E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.4378268 </GiEffect>
     <AOMstat>   -0.4713357 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 59 </Level>
     <Effect>   0.29119815E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       2.1114 </GiEffect>
     <AOMstat>       2.2729 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 6 </Level>
     <Effect>  -0.85248916E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0618103 </GiEffect>
     <AOMstat>   -0.0665410 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 60 </Level>
     <Effect>  -0.11229786E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.8142234 </GiEffect>
     <AOMstat>   -0.8765397 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 61 </Level>
     <Effect>   0.90749960E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.6579889 </GiEffect>
     <AOMstat>    0.7112267 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 62 </Level>
     <Effect>  -0.53095464E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3849724 </GiEffect>
     <AOMstat>   -0.4144361 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 63 </Level>
     <Effect>  -0.81318747E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.5896072 </GiEffect>
     <AOMstat>   -0.6347326 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 64 </Level>
     <Effect>  -0.23949481E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.1736474 </GiEffect>
     <AOMstat>   -0.1869374 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 65 </Level>
     <Effect>  -0.12079126E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.8758055 </GiEffect>
     <AOMstat>   -0.9428349 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 66 </Level>
     <Effect>   0.22949232E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1663950 </GiEffect>
     <AOMstat>    0.1791300 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 67 </Level>
     <Effect>  -0.43831334E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3178021 </GiEffect>
     <AOMstat>   -0.3434824 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 68 </Level>
     <Effect>  -0.46972338E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3405762 </GiEffect>
     <AOMstat>   -0.3681322 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 69 </Level>
     <Effect>   0.22378396E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.6226 </GiEffect>
     <AOMstat>       1.7467 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 7 </Level>
     <Effect>   0.12585073E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.0912489 </GiEffect>
     <AOMstat>    0.0982327 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 70 </Level>
     <Effect>   0.10097179E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.7321030 </GiEffect>
     <AOMstat>    0.7881342 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 71 </Level>
     <Effect>   0.15677303E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.1367 </GiEffect>
     <AOMstat>       1.2237 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 72 </Level>
     <Effect>   0.34414441E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.2495243 </GiEffect>
     <AOMstat>    0.2686216 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 73 </Level>
     <Effect>   0.26570117E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1926485 </GiEffect>
     <AOMstat>    0.2082356 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 74 </Level>
     <Effect>  -0.63394021E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.4596428 </GiEffect>
     <AOMstat>   -0.4948214 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 75 </Level>
     <Effect>  -0.80252219E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.5818743 </GiEffect>
     <AOMstat>   -0.6264079 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 76 </Level>
     <Effect>   0.25377542E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.1840016 </GiEffect>
     <AOMstat>    0.1980841 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 77 </Level>
     <Effect>   0.16139802E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.1702 </GiEffect>
     <AOMstat>       1.2598 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 78 </Level>
     <Effect>  -0.12542604E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0909410 </GiEffect>
     <AOMstat>   -0.0979012 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 79 </Level>
     <Effect>   0.11883194E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.8615993 </GiEffect>
     <AOMstat>    0.9275415 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 8 </Level>
     <Effect>  -0.12557945E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.9105226 </GiEffect>
     <AOMstat>   -0.9802091 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 80 </Level>
     <Effect>   0.13779487E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.0999091 </GiEffect>
     <AOMstat>    0.1075556 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 81 </Level>
     <Effect>  -0.90933971E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.6593231 </GiEffect>
     <AOMstat>   -0.7097841 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 82 </Level>
     <Effect>   0.17716263E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.2845 </GiEffect>
     <AOMstat>       1.3828 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 83 </Level>
     <Effect>   0.65198575E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.4727268 </GiEffect>
     <AOMstat>    0.5109751 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 84 </Level>
     <Effect>  -0.33753750E-08 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0244734 </GiEffect>
     <AOMstat>   -0.0263465 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 85 </Level>
     <Effect>  -0.30553411E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.2215296 </GiEffect>
     <AOMstat>   -0.2384843 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 86 </Level>
     <Effect>  -0.10040192E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.0727971 </GiEffect>
     <AOMstat>   -0.0783686 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 87 </Level>
     <Effect>   0.61871744E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.4486054 </GiEffect>
     <AOMstat>    0.4849020 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 88 </Level>
     <Effect>  -0.25849931E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.8743 </GiEffect>
     <AOMstat>      -2.0177 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 89 </Level>
     <Effect>  -0.16396737E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.1889 </GiEffect>
     <AOMstat>      -1.2798 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 9 </Level>
     <Effect>   0.79358465E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.5753941 </GiEffect>
     <AOMstat>    0.6194317 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 90 </Level>
     <Effect>  -0.26465816E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.9189 </GiEffect>
     <AOMstat>      -2.0658 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 91 </Level>
     <Effect>  -0.12457853E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.9032653 </GiEffect>
     <AOMstat>   -0.9723964 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 92 </Level>
     <Effect>   0.73843488E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>    0.5354074 </GiEffect>
     <AOMstat>    0.5763846 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 93 </Level>
     <Effect>  -0.20346209E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.4752 </GiEffect>
     <AOMstat>      -1.6011 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 94 </Level>
     <Effect>  -0.73758392E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.5347904 </GiEffect>
     <AOMstat>   -0.5757203 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 95 </Level>
     <Effect>  -0.47249595E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.3425865 </GiEffect>
     <AOMstat>   -0.3703051 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 96 </Level>
     <Effect>  -0.21838594E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.5834 </GiEffect>
     <AOMstat>      -1.7046 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 97 </Level>
     <Effect>  -0.14636338E-07 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>   -0.1061218 </GiEffect>
     <AOMstat>   -0.1147081 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 98 </Level>
     <Effect>  -0.15749508E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>      -1.1419 </GiEffect>
     <AOMstat>      -1.2343 </AOMstat>
   </Equation> <Equation>
     <Model_Term> entry </Model_Term>
     <Level> 99 </Level>
     <Effect>   0.14127467E-06 </Effect>
     <seEffect>   0.37137606E-03 </seEffect>
     <GiEffect>       1.0243 </GiEffect>
     <AOMstat>       1.1027 </AOMstat>
    </Equation >
   </Solutions >
   <WaldFstats>
    <WaldFtest>
     <FactorNumber> 9 </FactorNumber>
     <ModelTerm> mu </ModelTerm>
     <NumDF> 1 </NumDF>
     <DenDF>      127.4 </DenDF>
     <F-inc>   6114.17 </F-inc>
     <F-con>   6114.17 </F-con>
     <MarginFlag> . </MarginFlag>
     <Probability> &lt;.001 </Probability>
    </WaldFtest >
    <WaldFtest>
     <FactorNumber> 7 </FactorNumber>
     <ModelTerm> rep </ModelTerm>
     <NumDF> 1 </NumDF>
     <DenDF>      127.4 </DenDF>
     <F-inc>      1.22 </F-inc>
     <F-con>      1.22 </F-con>
     <MarginFlag> A </MarginFlag>
     <Probability>  0.271 </Probability>
    </WaldFtest >
   </WaldFstats >
   <FinishAt> 17 Jun 2021 16:07:29.183 </FinishAt>
   <Conclusion> LogL Converged </Conclusion>
  </Cycle >
 </ASReport >
"""