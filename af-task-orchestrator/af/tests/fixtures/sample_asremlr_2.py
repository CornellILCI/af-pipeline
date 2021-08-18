import pytest


@pytest.fixture
def sample_asreml_not_converged_result_string():
    return """<?xml version="1.0" encoding="utf-8" ?>
<ASReport>
<Version> ASReml 4.2 [01 Jan 2016]</Version>
<Build>ne [21 Jun 2021]   64 bit  Windows x64</Build>
<Title>67ac5d6f-5cdc-45fd-a2fa-2bc17a2c58bg_SA_1001</Title>
<StartTime>05 Aug 2021 12:56:51.130</StartTime>
<Cycle>
<CycleNumber>1</CycleNumber>
<DataSummary>
<Variable>
    <Vnumber>1</Vnumber>
    <Vname>loc</Vname>
    <Vlevel>1</Vlevel>
</Variable> <Variable>
    <Vnumber>2</Vnumber>
    <Vname>expt</Vname>
    <Vlevel>1</Vlevel>
</Variable> <Variable>
    <Vnumber>3</Vnumber>
    <Vname>entry</Vname>
    <Vlevel>180</Vlevel>
</Variable> <Variable>
    <Vnumber>4</Vnumber>
    <Vname>plot</Vname>
    <Vlevel>420</Vlevel>
</Variable> <Variable>
    <Vnumber>5</Vnumber>
    <Vname>col</Vname>
    <Vlevel>19</Vlevel>
</Variable> <Variable>
    <Vnumber>6</Vnumber>
    <Vname>row</Vname>
    <Vlevel>32</Vlevel>
</Variable> <Variable>
    <Vnumber>7</Vnumber>
    <Vname>rep</Vname>
    <Vlevel>2</Vlevel>
</Variable> <Variable>
    <Vnumber>8</Vnumber>
    <Vname>yield</Vname>
    <Variate>
    <Position>8</Position>
    <NumberMissing>58</NumberMissing>
    <NumberZero>0</NumberZero>
    <Minimum>       2.4411 </Minimum>
    <Mean>       6.6178 </Mean>
    <Maximum>      12.3619 </Maximum>
    <StndDevn>       1.5416 </StndDevn>
    </Variate >
</Variable> <Variable>
    <Vnumber>9</Vnumber>
    <Vname>mu</Vname>
    <Vlevel>1</Vlevel>
</Variable> <Variable>
    <Vnumber>10</Vnumber>
    <Vname>mv_estimates</Vname>
    <Vlevel>58</Vlevel>
</Variable >
</DataSummary >
<Predict_01>prediction entry</Predict_01>
<Convergence>
<Iteration>
    <ItrtnNumber>1</ItrtnNumber>
    <REML_LogL>        -379.368 </REML_LogL>
    <NEDF>416</NEDF>
</Iteration >
<Iteration>
    <ItrtnNumber>2</ItrtnNumber>
    <REML_LogL>        -367.794 </REML_LogL>
    <NEDF>416</NEDF>
</Iteration >
<Iteration>
    <ItrtnNumber>3</ItrtnNumber>
    <REML_LogL>        -358.960 </REML_LogL>
    <NEDF>416</NEDF>
</Iteration >
<Iteration>
    <ItrtnNumber>4</ItrtnNumber>
    <REML_LogL>        -356.446 </REML_LogL>
    <NEDF>416</NEDF>
</Iteration >
</Convergence >
<InformationCriteria>
<Akaike>         720.891 </Akaike>
<Bayesian>         737.014 </Bayesian>
<ParameterCount>4</ParameterCount>
</InformationCriteria >
<PredictTable>
<Table>1</Table>
<Preamble>
    <TraitName>yield</TraitName>
    <SimpleAveraging>  	rep</SimpleAveraging>
</Preamble >
<ClassifySet>
    <Variable_1>entry</Variable_1>
</ClassifySet >
<Prow>
    <Cell>1</Cell>
    <Identifier>           1</Identifier>
    <PredValue>       6.6212 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>2</Cell>
    <Identifier>           2</Identifier>
    <PredValue>       6.6235 </PredValue>
    <StndErr>    0.1269795 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>3</Cell>
    <Identifier>           3</Identifier>
    <PredValue>       6.6258 </PredValue>
    <StndErr>    0.1269855 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>4</Cell>
    <Identifier>           4</Identifier>
    <PredValue>       6.6208 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>5</Cell>
    <Identifier>           5</Identifier>
    <PredValue>       6.6233 </PredValue>
    <StndErr>    0.1269797 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>6</Cell>
    <Identifier>           6</Identifier>
    <PredValue>       6.6200 </PredValue>
    <StndErr>    0.1269848 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>7</Cell>
    <Identifier>           7</Identifier>
    <PredValue>       6.6203 </PredValue>
    <StndErr>    0.1269856 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>8</Cell>
    <Identifier>           8</Identifier>
    <PredValue>       6.6167 </PredValue>
    <StndErr>    0.1269590 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>9</Cell>
    <Identifier>           9</Identifier>
    <PredValue>       6.6240 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>10</Cell>
    <Identifier>          10</Identifier>
    <PredValue>       6.6193 </PredValue>
    <StndErr>    0.1269591 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>11</Cell>
    <Identifier>          11</Identifier>
    <PredValue>       6.6177 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>12</Cell>
    <Identifier>          12</Identifier>
    <PredValue>       6.6219 </PredValue>
    <StndErr>    0.1269857 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>13</Cell>
    <Identifier>          13</Identifier>
    <PredValue>       6.6199 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>14</Cell>
    <Identifier>          14</Identifier>
    <PredValue>       6.6167 </PredValue>
    <StndErr>    0.1269804 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>15</Cell>
    <Identifier>          15</Identifier>
    <PredValue>       6.6241 </PredValue>
    <StndErr>    0.1269858 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>16</Cell>
    <Identifier>          16</Identifier>
    <PredValue>       6.6210 </PredValue>
    <StndErr>    0.1269799 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>17</Cell>
    <Identifier>          17</Identifier>
    <PredValue>       6.6147 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>18</Cell>
    <Identifier>          18</Identifier>
    <PredValue>       6.6233 </PredValue>
    <StndErr>    0.1269851 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>19</Cell>
    <Identifier>          19</Identifier>
    <PredValue>       6.6214 </PredValue>
    <StndErr>    0.1269590 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>20</Cell>
    <Identifier>          20</Identifier>
    <PredValue>       6.6236 </PredValue>
    <StndErr>    0.1269856 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>21</Cell>
    <Identifier>          21</Identifier>
    <PredValue>       6.6206 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>22</Cell>
    <Identifier>          22</Identifier>
    <PredValue>       6.6261 </PredValue>
    <StndErr>    0.1269855 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>23</Cell>
    <Identifier>          23</Identifier>
    <PredValue>       6.6215 </PredValue>
    <StndErr>    0.1269872 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>24</Cell>
    <Identifier>          24</Identifier>
    <PredValue>       6.6195 </PredValue>
    <StndErr>    0.1269851 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>25</Cell>
    <Identifier>          25</Identifier>
    <PredValue>       6.6166 </PredValue>
    <StndErr>    0.1269806 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>26</Cell>
    <Identifier>          26</Identifier>
    <PredValue>       6.6223 </PredValue>
    <StndErr>    0.1269750 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>27</Cell>
    <Identifier>          27</Identifier>
    <PredValue>       6.6222 </PredValue>
    <StndErr>    0.1269851 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>28</Cell>
    <Identifier>          28</Identifier>
    <PredValue>       6.6237 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>29</Cell>
    <Identifier>          29</Identifier>
    <PredValue>       6.6206 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>30</Cell>
    <Identifier>          30</Identifier>
    <PredValue>       6.6207 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>31</Cell>
    <Identifier>          31</Identifier>
    <PredValue>       6.6211 </PredValue>
    <StndErr>    0.1269750 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>32</Cell>
    <Identifier>          32</Identifier>
    <PredValue>       6.6210 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>33</Cell>
    <Identifier>          33</Identifier>
    <PredValue>       6.6198 </PredValue>
    <StndErr>    0.1269458 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>34</Cell>
    <Identifier>          34</Identifier>
    <PredValue>       6.6146 </PredValue>
    <StndErr>    0.1269796 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>35</Cell>
    <Identifier>          35</Identifier>
    <PredValue>       6.6247 </PredValue>
    <StndErr>    0.1269806 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>36</Cell>
    <Identifier>          36</Identifier>
    <PredValue>       6.6216 </PredValue>
    <StndErr>    0.1269851 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>37</Cell>
    <Identifier>          37</Identifier>
    <PredValue>       6.6215 </PredValue>
    <StndErr>    0.1269857 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>38</Cell>
    <Identifier>          38</Identifier>
    <PredValue>       6.6159 </PredValue>
    <StndErr>    0.1269858 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>39</Cell>
    <Identifier>          39</Identifier>
    <PredValue>       6.6199 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>40</Cell>
    <Identifier>          40</Identifier>
    <PredValue>       6.6157 </PredValue>
    <StndErr>    0.1269594 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>41</Cell>
    <Identifier>          41</Identifier>
    <PredValue>       6.6259 </PredValue>
    <StndErr>    0.1269597 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>42</Cell>
    <Identifier>          42</Identifier>
    <PredValue>       6.6265 </PredValue>
    <StndErr>    0.1269857 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>43</Cell>
    <Identifier>          43</Identifier>
    <PredValue>       6.6214 </PredValue>
    <StndErr>    0.1269591 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>44</Cell>
    <Identifier>          44</Identifier>
    <PredValue>       6.6233 </PredValue>
    <StndErr>    0.1269802 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>45</Cell>
    <Identifier>          45</Identifier>
    <PredValue>       6.6263 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>46</Cell>
    <Identifier>          46</Identifier>
    <PredValue>       6.6235 </PredValue>
    <StndErr>    0.1269329 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>47</Cell>
    <Identifier>          47</Identifier>
    <PredValue>       6.6206 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>48</Cell>
    <Identifier>          48</Identifier>
    <PredValue>       6.6200 </PredValue>
    <StndErr>    0.1269855 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>49</Cell>
    <Identifier>          49</Identifier>
    <PredValue>       6.6133 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>50</Cell>
    <Identifier>          50</Identifier>
    <PredValue>       6.6162 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>51</Cell>
    <Identifier>          51</Identifier>
    <PredValue>       6.6173 </PredValue>
    <StndErr>    0.1269806 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>52</Cell>
    <Identifier>          52</Identifier>
    <PredValue>       6.6226 </PredValue>
    <StndErr>    0.1269856 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>53</Cell>
    <Identifier>          53</Identifier>
    <PredValue>       6.6216 </PredValue>
    <StndErr>    0.1269807 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>54</Cell>
    <Identifier>          54</Identifier>
    <PredValue>       6.6214 </PredValue>
    <StndErr>    0.1269806 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>55</Cell>
    <Identifier>          55</Identifier>
    <PredValue>       6.6144 </PredValue>
    <StndErr>    0.1269803 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>56</Cell>
    <Identifier>          56</Identifier>
    <PredValue>       6.6255 </PredValue>
    <StndErr>    0.1269597 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>57</Cell>
    <Identifier>          57</Identifier>
    <PredValue>       6.6179 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>58</Cell>
    <Identifier>          58</Identifier>
    <PredValue>       6.6213 </PredValue>
    <StndErr>    0.1269747 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>59</Cell>
    <Identifier>          59</Identifier>
    <PredValue>       6.6255 </PredValue>
    <StndErr>    0.1269802 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>60</Cell>
    <Identifier>          60</Identifier>
    <PredValue>       6.6182 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>61</Cell>
    <Identifier>          61</Identifier>
    <PredValue>       6.6229 </PredValue>
    <StndErr>    0.1269749 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>62</Cell>
    <Identifier>          62</Identifier>
    <PredValue>       6.6198 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>63</Cell>
    <Identifier>          63</Identifier>
    <PredValue>       6.6197 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>64</Cell>
    <Identifier>          64</Identifier>
    <PredValue>       6.6195 </PredValue>
    <StndErr>    0.1269847 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>65</Cell>
    <Identifier>          65</Identifier>
    <PredValue>       6.6187 </PredValue>
    <StndErr>    0.1269587 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>66</Cell>
    <Identifier>          66</Identifier>
    <PredValue>       6.6224 </PredValue>
    <StndErr>    0.1269596 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>67</Cell>
    <Identifier>          67</Identifier>
    <PredValue>       6.6210 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>68</Cell>
    <Identifier>          68</Identifier>
    <PredValue>       6.6208 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>69</Cell>
    <Identifier>          69</Identifier>
    <PredValue>       6.6269 </PredValue>
    <StndErr>    0.1269856 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>70</Cell>
    <Identifier>          70</Identifier>
    <PredValue>       6.6235 </PredValue>
    <StndErr>    0.1269514 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>71</Cell>
    <Identifier>          71</Identifier>
    <PredValue>       6.6256 </PredValue>
    <StndErr>    0.1269847 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>72</Cell>
    <Identifier>          72</Identifier>
    <PredValue>       6.6228 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>73</Cell>
    <Identifier>          73</Identifier>
    <PredValue>       6.6215 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>74</Cell>
    <Identifier>          74</Identifier>
    <PredValue>       6.6219 </PredValue>
    <StndErr>    0.1269806 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>75</Cell>
    <Identifier>          75</Identifier>
    <PredValue>       6.6196 </PredValue>
    <StndErr>    0.1269645 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>76</Cell>
    <Identifier>          76</Identifier>
    <PredValue>       6.6197 </PredValue>
    <StndErr>    0.1269596 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>77</Cell>
    <Identifier>          77</Identifier>
    <PredValue>       6.6249 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>78</Cell>
    <Identifier>          78</Identifier>
    <PredValue>       6.6208 </PredValue>
    <StndErr>    0.1269590 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>79</Cell>
    <Identifier>          79</Identifier>
    <PredValue>       6.6241 </PredValue>
    <StndErr>    0.1269807 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>80</Cell>
    <Identifier>          80</Identifier>
    <PredValue>       6.6202 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>81</Cell>
    <Identifier>          81</Identifier>
    <PredValue>       6.6195 </PredValue>
    <StndErr>    0.1269806 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>82</Cell>
    <Identifier>          82</Identifier>
    <PredValue>       6.6250 </PredValue>
    <StndErr>    0.1269855 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>83</Cell>
    <Identifier>          83</Identifier>
    <PredValue>       6.6218 </PredValue>
    <StndErr>    0.1269799 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>84</Cell>
    <Identifier>          84</Identifier>
    <PredValue>       6.6227 </PredValue>
    <StndErr>    0.1269803 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>85</Cell>
    <Identifier>          85</Identifier>
    <PredValue>       6.6214 </PredValue>
    <StndErr>    0.1269856 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>86</Cell>
    <Identifier>          86</Identifier>
    <PredValue>       6.6189 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>87</Cell>
    <Identifier>          87</Identifier>
    <PredValue>       6.6224 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>88</Cell>
    <Identifier>          88</Identifier>
    <PredValue>       6.6176 </PredValue>
    <StndErr>    0.1269848 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>89</Cell>
    <Identifier>          89</Identifier>
    <PredValue>       6.6177 </PredValue>
    <StndErr>    0.1269850 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>90</Cell>
    <Identifier>          90</Identifier>
    <PredValue>       6.6148 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>91</Cell>
    <Identifier>          91</Identifier>
    <PredValue>       6.6190 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>92</Cell>
    <Identifier>          92</Identifier>
    <PredValue>       6.6232 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>93</Cell>
    <Identifier>          93</Identifier>
    <PredValue>       6.6169 </PredValue>
    <StndErr>    0.1269750 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>94</Cell>
    <Identifier>          94</Identifier>
    <PredValue>       6.6198 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>95</Cell>
    <Identifier>          95</Identifier>
    <PredValue>       6.6199 </PredValue>
    <StndErr>    0.1269544 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>96</Cell>
    <Identifier>          96</Identifier>
    <PredValue>       6.6165 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>97</Cell>
    <Identifier>          97</Identifier>
    <PredValue>       6.6224 </PredValue>
    <StndErr>    0.1269802 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>98</Cell>
    <Identifier>          98</Identifier>
    <PredValue>       6.6200 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>99</Cell>
    <Identifier>          99</Identifier>
    <PredValue>       6.6218 </PredValue>
    <StndErr>    0.1269851 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>100</Cell>
    <Identifier>         100</Identifier>
    <PredValue>       6.6214 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>101</Cell>
    <Identifier>         101</Identifier>
    <PredValue>       6.6183 </PredValue>
    <StndErr>    0.1269855 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>102</Cell>
    <Identifier>         102</Identifier>
    <PredValue>       6.6186 </PredValue>
    <StndErr>    0.1269874 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>103</Cell>
    <Identifier>         103</Identifier>
    <PredValue>       6.6197 </PredValue>
    <StndErr>    0.1269590 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>104</Cell>
    <Identifier>         104</Identifier>
    <PredValue>       6.6188 </PredValue>
    <StndErr>    0.1269800 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>105</Cell>
    <Identifier>         105</Identifier>
    <PredValue>       6.6223 </PredValue>
    <StndErr>    0.1269848 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>106</Cell>
    <Identifier>         106</Identifier>
    <PredValue>       6.6151 </PredValue>
    <StndErr>    0.1269856 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>107</Cell>
    <Identifier>         107</Identifier>
    <PredValue>       6.6268 </PredValue>
    <StndErr>    0.1269595 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>108</Cell>
    <Identifier>         108</Identifier>
    <PredValue>       6.6221 </PredValue>
    <StndErr>    0.1269745 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>109</Cell>
    <Identifier>         109</Identifier>
    <PredValue>       6.6233 </PredValue>
    <StndErr>    0.1269850 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>110</Cell>
    <Identifier>         110</Identifier>
    <PredValue>       6.6191 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>111</Cell>
    <Identifier>         111</Identifier>
    <PredValue>       6.6159 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>112</Cell>
    <Identifier>         112</Identifier>
    <PredValue>       6.6227 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>113</Cell>
    <Identifier>         113</Identifier>
    <PredValue>       6.6230 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>114</Cell>
    <Identifier>         114</Identifier>
    <PredValue>       6.6211 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>115</Cell>
    <Identifier>         115</Identifier>
    <PredValue>       6.6187 </PredValue>
    <StndErr>    0.1269807 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>116</Cell>
    <Identifier>         116</Identifier>
    <PredValue>       6.6201 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>117</Cell>
    <Identifier>         117</Identifier>
    <PredValue>       6.6196 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>118</Cell>
    <Identifier>         118</Identifier>
    <PredValue>       6.6194 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>119</Cell>
    <Identifier>         119</Identifier>
    <PredValue>       6.6211 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>120</Cell>
    <Identifier>         120</Identifier>
    <PredValue>       6.6153 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>121</Cell>
    <Identifier>         121</Identifier>
    <PredValue>       6.6246 </PredValue>
    <StndErr>    0.1269750 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>122</Cell>
    <Identifier>         122</Identifier>
    <PredValue>       6.6176 </PredValue>
    <StndErr>    0.1269851 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>123</Cell>
    <Identifier>         123</Identifier>
    <PredValue>       6.6282 </PredValue>
    <StndErr>    0.1269458 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>124</Cell>
    <Identifier>         124</Identifier>
    <PredValue>       6.6232 </PredValue>
    <StndErr>    0.1269800 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>125</Cell>
    <Identifier>         125</Identifier>
    <PredValue>       6.6212 </PredValue>
    <StndErr>    0.1269803 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>126</Cell>
    <Identifier>         126</Identifier>
    <PredValue>       6.6175 </PredValue>
    <StndErr>    0.1269800 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>127</Cell>
    <Identifier>         127</Identifier>
    <PredValue>       6.6190 </PredValue>
    <StndErr>    0.1269807 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>128</Cell>
    <Identifier>         128</Identifier>
    <PredValue>       6.6198 </PredValue>
    <StndErr>    0.1269857 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>129</Cell>
    <Identifier>         129</Identifier>
    <PredValue>       6.6192 </PredValue>
    <StndErr>    0.1269847 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>130</Cell>
    <Identifier>         130</Identifier>
    <PredValue>       6.6173 </PredValue>
    <StndErr>    0.1269850 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>131</Cell>
    <Identifier>         131</Identifier>
    <PredValue>       6.6249 </PredValue>
    <StndErr>    0.1269649 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>132</Cell>
    <Identifier>         132</Identifier>
    <PredValue>       6.6249 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>133</Cell>
    <Identifier>         133</Identifier>
    <PredValue>       6.6284 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>134</Cell>
    <Identifier>         134</Identifier>
    <PredValue>       6.6232 </PredValue>
    <StndErr>    0.1269851 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>135</Cell>
    <Identifier>         135</Identifier>
    <PredValue>       6.6190 </PredValue>
    <StndErr>    0.1269800 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>136</Cell>
    <Identifier>         136</Identifier>
    <PredValue>       6.6219 </PredValue>
    <StndErr>    0.1269807 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>137</Cell>
    <Identifier>         137</Identifier>
    <PredValue>       6.6218 </PredValue>
    <StndErr>    0.1269514 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>138</Cell>
    <Identifier>         138</Identifier>
    <PredValue>       6.6201 </PredValue>
    <StndErr>    0.1269807 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>139</Cell>
    <Identifier>         139</Identifier>
    <PredValue>       6.6177 </PredValue>
    <StndErr>    0.1269757 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>140</Cell>
    <Identifier>         140</Identifier>
    <PredValue>       6.6190 </PredValue>
    <StndErr>    0.1269801 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>141</Cell>
    <Identifier>         141</Identifier>
    <PredValue>       6.6246 </PredValue>
    <StndErr>    0.1269849 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>142</Cell>
    <Identifier>         142</Identifier>
    <PredValue>       6.6209 </PredValue>
    <StndErr>    0.1269855 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>143</Cell>
    <Identifier>         143</Identifier>
    <PredValue>       6.6186 </PredValue>
    <StndErr>    0.1269855 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>144</Cell>
    <Identifier>         144</Identifier>
    <PredValue>       6.6225 </PredValue>
    <StndErr>    0.1269544 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>145</Cell>
    <Identifier>         145</Identifier>
    <PredValue>       6.6162 </PredValue>
    <StndErr>    0.1269857 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>146</Cell>
    <Identifier>         146</Identifier>
    <PredValue>       6.6222 </PredValue>
    <StndErr>    0.1269853 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>147</Cell>
    <Identifier>         147</Identifier>
    <PredValue>       6.6207 </PredValue>
    <StndErr>    0.1269803 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>148</Cell>
    <Identifier>         148</Identifier>
    <PredValue>       6.6217 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>149</Cell>
    <Identifier>         149</Identifier>
    <PredValue>       6.6184 </PredValue>
    <StndErr>    0.1269807 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>150</Cell>
    <Identifier>         150</Identifier>
    <PredValue>       6.6227 </PredValue>
    <StndErr>    0.1269800 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>151</Cell>
    <Identifier>         151</Identifier>
    <PredValue>       6.6219 </PredValue>
    <StndErr>    0.1269802 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>152</Cell>
    <Identifier>         152</Identifier>
    <PredValue>       6.6248 </PredValue>
    <StndErr>    0.1269802 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>153</Cell>
    <Identifier>         153</Identifier>
    <PredValue>       6.6240 </PredValue>
    <StndErr>    0.1269459 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>154</Cell>
    <Identifier>         154</Identifier>
    <PredValue>       6.6212 </PredValue>
    <StndErr>    0.1269596 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>155</Cell>
    <Identifier>         155</Identifier>
    <PredValue>       6.6275 </PredValue>
    <StndErr>    0.1269852 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>156</Cell>
    <Identifier>         156</Identifier>
    <PredValue>       6.6192 </PredValue>
    <StndErr>    0.1269857 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>157</Cell>
    <Identifier>         157</Identifier>
    <PredValue>       6.6184 </PredValue>
    <StndErr>    0.1269851 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>158</Cell>
    <Identifier>         158</Identifier>
    <PredValue>       6.6238 </PredValue>
    <StndErr>    0.1269874 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>159</Cell>
    <Identifier>         159</Identifier>
    <PredValue>       6.6216 </PredValue>
    <StndErr>    0.1269593 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>160</Cell>
    <Identifier>         160</Identifier>
    <PredValue>       6.6203 </PredValue>
    <StndErr>    0.1269858 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>161</Cell>
    <Identifier>         161</Identifier>
    <PredValue>       6.6196 </PredValue>
    <StndErr>    0.1269858 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>162</Cell>
    <Identifier>         162</Identifier>
    <PredValue>       6.6189 </PredValue>
    <StndErr>    0.1269541 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>163</Cell>
    <Identifier>         163</Identifier>
    <PredValue>       6.6214 </PredValue>
    <StndErr>    0.1269802 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>164</Cell>
    <Identifier>         164</Identifier>
    <PredValue>       6.6200 </PredValue>
    <StndErr>    0.1269541 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>165</Cell>
    <Identifier>         165</Identifier>
    <PredValue>       6.6208 </PredValue>
    <StndErr>    0.1269800 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>166</Cell>
    <Identifier>         166</Identifier>
    <PredValue>       6.6180 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>167</Cell>
    <Identifier>         167</Identifier>
    <PredValue>       6.6113 </PredValue>
    <StndErr>    0.1269850 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>168</Cell>
    <Identifier>         168</Identifier>
    <PredValue>       6.6189 </PredValue>
    <StndErr>    0.1269855 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>169</Cell>
    <Identifier>         169</Identifier>
    <PredValue>       6.6187 </PredValue>
    <StndErr>    0.1269650 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>170</Cell>
    <Identifier>         170</Identifier>
    <PredValue>       6.6253 </PredValue>
    <StndErr>    0.1269855 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>171</Cell>
    <Identifier>         171</Identifier>
    <PredValue>       6.6218 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>172</Cell>
    <Identifier>         172</Identifier>
    <PredValue>       6.6180 </PredValue>
    <StndErr>    0.1270486 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>173</Cell>
    <Identifier>         173</Identifier>
    <PredValue>       6.6210 </PredValue>
    <StndErr>    0.1269858 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>174</Cell>
    <Identifier>         174</Identifier>
    <PredValue>       6.6211 </PredValue>
    <StndErr>    0.1269805 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>175</Cell>
    <Identifier>         175</Identifier>
    <PredValue>       6.6151 </PredValue>
    <StndErr>    0.1268445 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>176</Cell>
    <Identifier>         176</Identifier>
    <PredValue>       6.6282 </PredValue>
    <StndErr>    0.1268454 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>177</Cell>
    <Identifier>         177</Identifier>
    <PredValue>       6.6301 </PredValue>
    <StndErr>    0.1268404 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>178</Cell>
    <Identifier>         178</Identifier>
    <PredValue>       6.6254 </PredValue>
    <StndErr>    0.1257182 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>179</Cell>
    <Identifier>         179</Identifier>
    <PredValue>       6.6286 </PredValue>
    <StndErr>    0.1256124 </StndErr>
    <EPcode> E</EPcode>
</Prow> <Prow>
    <Cell>180</Cell>
    <Identifier>         180</Identifier>
    <PredValue>       6.6247 </PredValue>
    <StndErr>    0.1259166 </StndErr>
    <EPcode> E</EPcode>
</Prow >
<SED>    0.0752131 </SED>
</PredictTable >
<VarianceComponents>
<VParameter>
    <ParameterIndex>4</ParameterIndex>
    <SourceModel>entry                   IDV_V  180</SourceModel>
    <Source>entry</Source>
    <VCStructure>IDV_V</VCStructure>
    <ParameterType>Gamma</ParameterType>
    <Levels>180</Levels>
    <Gamma>   0.11697715E-03 </Gamma>
    <VComponent>   0.26934085E-03 </VComponent>
    <ZRatio>    0.0031786 </ZRatio>
    <PCchange>-3</PCchange>
    <ConstraintCode>?</ConstraintCode>
</VParameter >
<VParameter>
    <RSection>1</RSection>
    <SourceModel>Residual                SCA_V  476</SourceModel>
    <Source>Residual</Source>
    <VCStructure>Residual</VCStructure>
    <ParameterType>Variance</ParameterType>
    <Levels>476</Levels>
    <Gamma>       1.0000 </Gamma>
    <VComponent>       2.3025 </VComponent>
    <ZRatio>      11.8326 </ZRatio>
    <PCchange>0</PCchange>
    <ConstraintCode>P</ConstraintCode>
</VParameter >
<VParameter>
    <RSection>1</RSection>
    <ParameterIndex>6</ParameterIndex>
    <SourceModel>row                      AR_R    1</SourceModel>
    <Source>Residual [1]</Source>
    <VCStructure>AR_R</VCStructure>
    <ParameterType>Correln</ParameterType>
    <Levels>1</Levels>
    <Gamma>    0.3945776 </Gamma>
    <VComponent>    0.3945776 </VComponent>
    <ZRatio>       9.2413 </ZRatio>
    <PCchange>76</PCchange>
    <ConstraintCode>P</ConstraintCode>
</VParameter >
<VParameter>
    <RSection>1</RSection>
    <ParameterIndex>7</ParameterIndex>
    <SourceModel>col                      AR_R    1</SourceModel>
    <Source>Residual [1]</Source>
    <VCStructure>AR_R</VCStructure>
    <ParameterType>Correln</ParameterType>
    <Levels>1</Levels>
    <Gamma>    0.0966912 </Gamma>
    <VComponent>    0.0966912 </VComponent>
    <ZRatio>       1.9035 </ZRatio>
    <PCchange>1</PCchange>
    <ConstraintCode>P</ConstraintCode>
</VParameter >
</VarianceComponents >
<Solutions>
<Equation>
    <Model_Term>rep</Model_Term>
    <Level>1</Level>
    <Effect>    0.0000000 </Effect>
    <seEffect>    0.0000000 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>rep</Model_Term>
    <Level>2</Level>
    <Effect>   -0.2818564 </Effect>
    <seEffect>    0.2176415 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mu</Model_Term>
    <Level>         1</Level>
    <Effect>       6.7619 </Effect>
    <seEffect>    0.1586282 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>         1</Level>
    <Effect>       5.9258 </Effect>
    <seEffect>       1.3260 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>         2</Level>
    <Effect>       5.7925 </Effect>
    <seEffect>       1.3260 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>         3</Level>
    <Effect>       6.8137 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>         4</Level>
    <Effect>       6.7090 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>         5</Level>
    <Effect>       6.7863 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>         6</Level>
    <Effect>       6.6761 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>         7</Level>
    <Effect>       6.6372 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>         8</Level>
    <Effect>       6.4410 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>         9</Level>
    <Effect>       6.7798 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        10</Level>
    <Effect>       6.4907 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        11</Level>
    <Effect>       6.6510 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        12</Level>
    <Effect>       6.5736 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        13</Level>
    <Effect>       6.6040 </Effect>
    <seEffect>       1.5179 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        14</Level>
    <Effect>       6.5899 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        15</Level>
    <Effect>       6.6992 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        16</Level>
    <Effect>       6.6187 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        17</Level>
    <Effect>       6.4940 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        18</Level>
    <Effect>       6.5602 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        19</Level>
    <Effect>       6.6322 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        20</Level>
    <Effect>       6.6502 </Effect>
    <seEffect>       1.5193 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        21</Level>
    <Effect>       6.7821 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        22</Level>
    <Effect>       6.8465 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        23</Level>
    <Effect>       6.4785 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        24</Level>
    <Effect>       6.6260 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        25</Level>
    <Effect>       6.8032 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        26</Level>
    <Effect>       6.5841 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        27</Level>
    <Effect>       6.6856 </Effect>
    <seEffect>       1.5248 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        28</Level>
    <Effect>       6.7923 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        29</Level>
    <Effect>       6.8647 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        30</Level>
    <Effect>       6.9174 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        31</Level>
    <Effect>       6.7735 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        32</Level>
    <Effect>       6.7041 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        33</Level>
    <Effect>       6.8829 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        34</Level>
    <Effect>       6.7520 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        35</Level>
    <Effect>       6.6472 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        36</Level>
    <Effect>       6.7799 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        37</Level>
    <Effect>       6.8682 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        38</Level>
    <Effect>       6.6679 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        39</Level>
    <Effect>       6.7806 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        40</Level>
    <Effect>       6.6711 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        41</Level>
    <Effect>       6.6709 </Effect>
    <seEffect>       1.5236 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        42</Level>
    <Effect>       6.6588 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        43</Level>
    <Effect>       6.7812 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        44</Level>
    <Effect>       6.8827 </Effect>
    <seEffect>       1.5178 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        45</Level>
    <Effect>       6.5701 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        46</Level>
    <Effect>       6.6534 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        47</Level>
    <Effect>       6.6294 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        48</Level>
    <Effect>       6.6634 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        49</Level>
    <Effect>       6.7672 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        50</Level>
    <Effect>       6.6896 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        51</Level>
    <Effect>       6.5314 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        52</Level>
    <Effect>       6.6604 </Effect>
    <seEffect>       1.5193 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        53</Level>
    <Effect>       6.8360 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        54</Level>
    <Effect>       6.7043 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        55</Level>
    <Effect>       6.6172 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        56</Level>
    <Effect>       6.6278 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        57</Level>
    <Effect>       6.7341 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>mv_estimates</Model_Term>
    <Level>        58</Level>
    <Effect>       6.8598 </Effect>
    <seEffect>       1.5195 </seEffect>
    <GiEffect>    0.0000000 </GiEffect>
    <AOMstat>    0.0000000 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>         1</Level>
    <Effect>   0.21510731E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.0757660 </GiEffect>
    <AOMstat>    0.0708005 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>         2</Level>
    <Effect>    0.0024995 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.8803957 </GiEffect>
    <AOMstat>    0.8242744 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>         3</Level>
    <Effect>    0.0048262 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.6999 </GiEffect>
    <AOMstat>       1.5878 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>         4</Level>
    <Effect>  -0.22634447E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.0797240 </GiEffect>
    <AOMstat>   -0.0746409 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>         5</Level>
    <Effect>    0.0022646 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.7976559 </GiEffect>
    <AOMstat>    0.7468079 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>         6</Level>
    <Effect>  -0.97575095E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.3436830 </GiEffect>
    <AOMstat>   -0.3210165 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>         7</Level>
    <Effect>  -0.71922558E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.2533286 </GiEffect>
    <AOMstat>   -0.2366185 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>         8</Level>
    <Effect>   -0.0042555 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>      -1.4989 </GiEffect>
    <AOMstat>      -1.4431 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>         9</Level>
    <Effect>    0.0030519 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>       1.0750 </GiEffect>
    <AOMstat>       1.0064 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        10</Level>
    <Effect>   -0.0016500 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>   -0.5811787 </GiEffect>
    <AOMstat>   -0.5595278 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        11</Level>
    <Effect>   -0.0032408 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -1.1415 </GiEffect>
    <AOMstat>      -1.0687 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        12</Level>
    <Effect>   0.95134966E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.3350883 </GiEffect>
    <AOMstat>    0.3129856 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        13</Level>
    <Effect>   -0.0011010 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.3877857 </GiEffect>
    <AOMstat>   -0.3622082 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        14</Level>
    <Effect>   -0.0043188 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -1.5212 </GiEffect>
    <AOMstat>      -1.4242 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        15</Level>
    <Effect>    0.0031115 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.0959 </GiEffect>
    <AOMstat>       1.0241 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        16</Level>
    <Effect>   0.24626482E-04 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.0086740 </GiEffect>
    <AOMstat>    0.0081213 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        17</Level>
    <Effect>   -0.0063225 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -2.2269 </GiEffect>
    <AOMstat>      -2.0850 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        18</Level>
    <Effect>    0.0023097 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.8135297 </GiEffect>
    <AOMstat>    0.7598780 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        19</Level>
    <Effect>   0.36672634E-03 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>    0.1291698 </GiEffect>
    <AOMstat>    0.1243576 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        20</Level>
    <Effect>    0.0026564 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.9356372 </GiEffect>
    <AOMstat>    0.8739224 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        21</Level>
    <Effect>  -0.34285129E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.1207605 </GiEffect>
    <AOMstat>   -0.1127955 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        22</Level>
    <Effect>    0.0050687 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.7853 </GiEffect>
    <AOMstat>       1.6676 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        23</Level>
    <Effect>   0.46833936E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.1649604 </GiEffect>
    <AOMstat>    0.1541131 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        24</Level>
    <Effect>   -0.0014428 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.5081918 </GiEffect>
    <AOMstat>   -0.4749022 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        25</Level>
    <Effect>   -0.0044048 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -1.5515 </GiEffect>
    <AOMstat>      -1.4531 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        26</Level>
    <Effect>    0.0013208 </Effect>
    <seEffect>    0.0531973 </seEffect>
    <GiEffect>    0.4652324 </GiEffect>
    <AOMstat>    0.4366061 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        27</Level>
    <Effect>    0.0012104 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.4263356 </GiEffect>
    <AOMstat>    0.3982224 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        28</Level>
    <Effect>    0.0027572 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.9711626 </GiEffect>
    <AOMstat>    0.9092423 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        29</Level>
    <Effect>  -0.41188059E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.1450743 </GiEffect>
    <AOMstat>   -0.1358256 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        30</Level>
    <Effect>  -0.32439527E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.1142598 </GiEffect>
    <AOMstat>   -0.1067236 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        31</Level>
    <Effect>   0.13566697E-03 </Effect>
    <seEffect>    0.0531973 </seEffect>
    <GiEffect>    0.0477852 </GiEffect>
    <AOMstat>    0.0448449 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        32</Level>
    <Effect>  -0.26423116E-04 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.0093069 </GiEffect>
    <AOMstat>   -0.0086929 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        33</Level>
    <Effect>   -0.0011908 </Effect>
    <seEffect>    0.0532023 </seEffect>
    <GiEffect>   -0.4194394 </GiEffect>
    <AOMstat>   -0.4057791 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        34</Level>
    <Effect>   -0.0064015 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -2.2548 </GiEffect>
    <AOMstat>      -2.1110 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        35</Level>
    <Effect>    0.0037616 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>       1.3249 </GiEffect>
    <AOMstat>       1.2405 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        36</Level>
    <Effect>   0.56257226E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.1981515 </GiEffect>
    <AOMstat>    0.1850826 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        37</Level>
    <Effect>   0.51787979E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.1824097 </GiEffect>
    <AOMstat>    0.1703775 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        38</Level>
    <Effect>   -0.0050380 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -1.7745 </GiEffect>
    <AOMstat>      -1.6574 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        39</Level>
    <Effect>   -0.0010916 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.3844857 </GiEffect>
    <AOMstat>   -0.3591323 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        40</Level>
    <Effect>   -0.0052576 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>      -1.8518 </GiEffect>
    <AOMstat>      -1.7829 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        41</Level>
    <Effect>    0.0049159 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>       1.7315 </GiEffect>
    <AOMstat>       1.6670 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        42</Level>
    <Effect>    0.0054738 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.9280 </GiEffect>
    <AOMstat>       1.8016 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        43</Level>
    <Effect>   0.42006594E-03 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>    0.1479573 </GiEffect>
    <AOMstat>    0.1424453 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        44</Level>
    <Effect>    0.0022732 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.8006718 </GiEffect>
    <AOMstat>    0.7496269 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        45</Level>
    <Effect>    0.0053474 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.8835 </GiEffect>
    <AOMstat>       1.7592 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        46</Level>
    <Effect>    0.0025320 </Effect>
    <seEffect>    0.0532067 </seEffect>
    <GiEffect>    0.8918411 </GiEffect>
    <AOMstat>    0.8867463 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        47</Level>
    <Effect>  -0.34290820E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.1207805 </GiEffect>
    <AOMstat>   -0.1128142 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        48</Level>
    <Effect>  -0.98037023E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.3453100 </GiEffect>
    <AOMstat>   -0.3225334 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        49</Level>
    <Effect>   -0.0076564 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -2.6968 </GiEffect>
    <AOMstat>      -2.5189 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        50</Level>
    <Effect>   -0.0047936 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -1.6884 </GiEffect>
    <AOMstat>      -1.5808 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        51</Level>
    <Effect>   -0.0036658 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -1.2912 </GiEffect>
    <AOMstat>      -1.2089 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        52</Level>
    <Effect>    0.0015847 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.5581536 </GiEffect>
    <AOMstat>    0.5213419 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        53</Level>
    <Effect>   0.63655226E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.2242090 </GiEffect>
    <AOMstat>    0.2099140 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        54</Level>
    <Effect>   0.45675743E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.1608810 </GiEffect>
    <AOMstat>    0.1506238 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        55</Level>
    <Effect>   -0.0065497 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -2.3070 </GiEffect>
    <AOMstat>      -2.1599 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        56</Level>
    <Effect>    0.0045001 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>       1.5850 </GiEffect>
    <AOMstat>       1.5260 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        57</Level>
    <Effect>   -0.0030886 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -1.0879 </GiEffect>
    <AOMstat>      -1.0185 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        58</Level>
    <Effect>   0.32744998E-03 </Effect>
    <seEffect>    0.0531973 </seEffect>
    <GiEffect>    0.1153358 </GiEffect>
    <AOMstat>    0.1082394 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        59</Level>
    <Effect>    0.0045425 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>       1.6000 </GiEffect>
    <AOMstat>       1.4980 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        60</Level>
    <Effect>   -0.0027509 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.9689359 </GiEffect>
    <AOMstat>   -0.9050489 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        61</Level>
    <Effect>    0.0018648 </Effect>
    <seEffect>    0.0531974 </seEffect>
    <GiEffect>    0.6568407 </GiEffect>
    <AOMstat>    0.6167734 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        62</Level>
    <Effect>   -0.0012202 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.4297992 </GiEffect>
    <AOMstat>   -0.4014508 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        63</Level>
    <Effect>   -0.0012712 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.4477535 </GiEffect>
    <AOMstat>   -0.4182180 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        64</Level>
    <Effect>   -0.0015281 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.5382500 </GiEffect>
    <AOMstat>   -0.5027521 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        65</Level>
    <Effect>   -0.0022967 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>   -0.8089466 </GiEffect>
    <AOMstat>   -0.7789530 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        66</Level>
    <Effect>    0.0013669 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>    0.4814552 </GiEffect>
    <AOMstat>    0.4635152 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        67</Level>
    <Effect>   0.35351887E-04 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.0124518 </GiEffect>
    <AOMstat>    0.0116579 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        68</Level>
    <Effect>  -0.15506316E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.0546170 </GiEffect>
    <AOMstat>   -0.0511349 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        69</Level>
    <Effect>    0.0059536 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       2.0970 </GiEffect>
    <AOMstat>       1.9587 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        70</Level>
    <Effect>    0.0024811 </Effect>
    <seEffect>    0.0532019 </seEffect>
    <GiEffect>    0.8738932 </GiEffect>
    <AOMstat>    0.8432948 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        71</Level>
    <Effect>    0.0046044 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.6218 </GiEffect>
    <AOMstat>       1.5148 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        72</Level>
    <Effect>    0.0017936 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.6317573 </GiEffect>
    <AOMstat>    0.5900799 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        73</Level>
    <Effect>   0.56146324E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.1977609 </GiEffect>
    <AOMstat>    0.1851534 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        74</Level>
    <Effect>   0.91499319E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.3222826 </GiEffect>
    <AOMstat>    0.3017349 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        75</Level>
    <Effect>   -0.0014369 </Effect>
    <seEffect>    0.0532013 </seEffect>
    <GiEffect>   -0.5061103 </GiEffect>
    <AOMstat>   -0.4865263 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        76</Level>
    <Effect>   -0.0013077 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>   -0.4606006 </GiEffect>
    <AOMstat>   -0.4434340 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        77</Level>
    <Effect>    0.0039573 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.3939 </GiEffect>
    <AOMstat>       1.3019 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        78</Level>
    <Effect>  -0.21079680E-03 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>   -0.0742477 </GiEffect>
    <AOMstat>   -0.0714816 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        79</Level>
    <Effect>    0.0031439 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>       1.1074 </GiEffect>
    <AOMstat>       1.0368 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        80</Level>
    <Effect>  -0.81339268E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.2864965 </GiEffect>
    <AOMstat>   -0.2677225 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        81</Level>
    <Effect>   -0.0014642 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.5157221 </GiEffect>
    <AOMstat>   -0.4828417 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        82</Level>
    <Effect>    0.0040081 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.4117 </GiEffect>
    <AOMstat>       1.3186 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        83</Level>
    <Effect>   0.81746765E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.2879318 </GiEffect>
    <AOMstat>    0.2695766 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        84</Level>
    <Effect>    0.0016885 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.5947319 </GiEffect>
    <AOMstat>    0.5568256 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        85</Level>
    <Effect>   0.37734709E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.1329107 </GiEffect>
    <AOMstat>    0.1241460 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        86</Level>
    <Effect>   -0.0021258 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.7487538 </GiEffect>
    <AOMstat>   -0.6993693 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        87</Level>
    <Effect>    0.0013688 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.4821320 </GiEffect>
    <AOMstat>    0.4513935 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        88</Level>
    <Effect>   -0.0033987 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -1.1971 </GiEffect>
    <AOMstat>      -1.1182 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        89</Level>
    <Effect>   -0.0032738 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -1.1531 </GiEffect>
    <AOMstat>      -1.0771 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        90</Level>
    <Effect>   -0.0061858 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -2.1788 </GiEffect>
    <AOMstat>      -2.0351 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        91</Level>
    <Effect>   -0.0019923 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.7017426 </GiEffect>
    <AOMstat>   -0.6554746 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        92</Level>
    <Effect>    0.0022330 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.7865292 </GiEffect>
    <AOMstat>    0.7346468 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        93</Level>
    <Effect>   -0.0040856 </Effect>
    <seEffect>    0.0531973 </seEffect>
    <GiEffect>      -1.4390 </GiEffect>
    <AOMstat>      -1.3505 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        94</Level>
    <Effect>   -0.0012362 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.4354314 </GiEffect>
    <AOMstat>   -0.4069076 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        95</Level>
    <Effect>   -0.0010381 </Effect>
    <seEffect>    0.0532020 </seEffect>
    <GiEffect>   -0.3656310 </GiEffect>
    <AOMstat>   -0.3528916 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        96</Level>
    <Effect>   -0.0044438 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -1.5652 </GiEffect>
    <AOMstat>      -1.4620 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        97</Level>
    <Effect>    0.0014279 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.5029351 </GiEffect>
    <AOMstat>    0.4710625 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        98</Level>
    <Effect>  -0.93872126E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.3306402 </GiEffect>
    <AOMstat>   -0.3095614 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>        99</Level>
    <Effect>   0.80809785E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.2846315 </GiEffect>
    <AOMstat>    0.2658653 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       100</Level>
    <Effect>   0.43945467E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.1547865 </GiEffect>
    <AOMstat>    0.1449179 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       101</Level>
    <Effect>   -0.0027000 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.9510066 </GiEffect>
    <AOMstat>   -0.8882864 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       102</Level>
    <Effect>   -0.0023760 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.8368888 </GiEffect>
    <AOMstat>   -0.7818499 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       103</Level>
    <Effect>   -0.0012607 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>   -0.4440484 </GiEffect>
    <AOMstat>   -0.4275066 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       104</Level>
    <Effect>   -0.0022210 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.7822833 </GiEffect>
    <AOMstat>   -0.7324046 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       105</Level>
    <Effect>    0.0012757 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.4493222 </GiEffect>
    <AOMstat>    0.4198795 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       106</Level>
    <Effect>   -0.0058701 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -2.0676 </GiEffect>
    <AOMstat>      -1.9312 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       107</Level>
    <Effect>    0.0058616 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>       2.0646 </GiEffect>
    <AOMstat>       1.9880 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       108</Level>
    <Effect>    0.0011468 </Effect>
    <seEffect>    0.0531973 </seEffect>
    <GiEffect>    0.4039148 </GiEffect>
    <AOMstat>    0.3790942 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       109</Level>
    <Effect>    0.0023011 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.8105201 </GiEffect>
    <AOMstat>    0.7570810 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       110</Level>
    <Effect>   -0.0019363 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.6819968 </GiEffect>
    <AOMstat>   -0.6370195 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       111</Level>
    <Effect>   -0.0050896 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -1.7927 </GiEffect>
    <AOMstat>      -1.6744 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       112</Level>
    <Effect>    0.0017593 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.6196614 </GiEffect>
    <AOMstat>    0.5787908 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       113</Level>
    <Effect>    0.0020466 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.7208563 </GiEffect>
    <AOMstat>    0.6749009 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       114</Level>
    <Effect>   0.12591140E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.0443490 </GiEffect>
    <AOMstat>    0.0415214 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       115</Level>
    <Effect>   -0.0023175 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.8162818 </GiEffect>
    <AOMstat>   -0.7642355 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       116</Level>
    <Effect>  -0.86338267E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.3041042 </GiEffect>
    <AOMstat>   -0.2841745 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       117</Level>
    <Effect>   -0.0014021 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.4938420 </GiEffect>
    <AOMstat>   -0.4623565 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       118</Level>
    <Effect>   -0.0016147 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.5687506 </GiEffect>
    <AOMstat>   -0.5324918 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       119</Level>
    <Effect>   0.83228534E-04 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.0293151 </GiEffect>
    <AOMstat>    0.0273815 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       120</Level>
    <Effect>   -0.0057155 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -2.0132 </GiEffect>
    <AOMstat>      -1.8812 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       121</Level>
    <Effect>    0.0036592 </Effect>
    <seEffect>    0.0531973 </seEffect>
    <GiEffect>       1.2889 </GiEffect>
    <AOMstat>       1.2095 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       122</Level>
    <Effect>   -0.0034067 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -1.1999 </GiEffect>
    <AOMstat>      -1.1208 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       123</Level>
    <Effect>    0.0071703 </Effect>
    <seEffect>    0.0532023 </seEffect>
    <GiEffect>       2.5256 </GiEffect>
    <AOMstat>       2.4433 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       124</Level>
    <Effect>    0.0022083 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.7778227 </GiEffect>
    <AOMstat>    0.7282303 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       125</Level>
    <Effect>   0.18875262E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.0664832 </GiEffect>
    <AOMstat>    0.0622451 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       126</Level>
    <Effect>   -0.0035224 </Effect>
    <seEffect>    0.0531970 </seEffect>
    <GiEffect>      -1.2407 </GiEffect>
    <AOMstat>      -1.1623 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       127</Level>
    <Effect>   -0.0020340 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.7164198 </GiEffect>
    <AOMstat>   -0.6707430 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       128</Level>
    <Effect>   -0.0012240 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.4311122 </GiEffect>
    <AOMstat>   -0.4026748 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       129</Level>
    <Effect>   -0.0017390 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.6125324 </GiEffect>
    <AOMstat>   -0.5721816 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       130</Level>
    <Effect>   -0.0036388 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -1.2817 </GiEffect>
    <AOMstat>      -1.1971 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       131</Level>
    <Effect>    0.0038743 </Effect>
    <seEffect>    0.0532013 </seEffect>
    <GiEffect>       1.3646 </GiEffect>
    <AOMstat>       1.3118 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       132</Level>
    <Effect>    0.0038787 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>       1.3662 </GiEffect>
    <AOMstat>       1.2796 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       133</Level>
    <Effect>    0.0074584 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       2.6270 </GiEffect>
    <AOMstat>       2.4538 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       134</Level>
    <Effect>    0.0021847 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.7695020 </GiEffect>
    <AOMstat>    0.7187597 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       135</Level>
    <Effect>   -0.0020144 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.7095366 </GiEffect>
    <AOMstat>   -0.6645722 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       136</Level>
    <Effect>   0.91826081E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.3234336 </GiEffect>
    <AOMstat>    0.3028122 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       137</Level>
    <Effect>   0.86225913E-03 </Effect>
    <seEffect>    0.0532019 </seEffect>
    <GiEffect>    0.3037084 </GiEffect>
    <AOMstat>    0.2930754 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       138</Level>
    <Effect>  -0.84834076E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.2988060 </GiEffect>
    <AOMstat>   -0.2797541 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       139</Level>
    <Effect>   -0.0033308 </Effect>
    <seEffect>    0.0531974 </seEffect>
    <GiEffect>      -1.1732 </GiEffect>
    <AOMstat>      -1.1016 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       140</Level>
    <Effect>   -0.0019954 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.7028418 </GiEffect>
    <AOMstat>   -0.6580296 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       141</Level>
    <Effect>    0.0035727 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.2584 </GiEffect>
    <AOMstat>       1.1755 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       142</Level>
    <Effect>  -0.43728550E-04 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.0154022 </GiEffect>
    <AOMstat>   -0.0143864 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       143</Level>
    <Effect>   -0.0023787 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.8378459 </GiEffect>
    <AOMstat>   -0.7825812 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       144</Level>
    <Effect>    0.0014682 </Effect>
    <seEffect>    0.0532020 </seEffect>
    <GiEffect>    0.5171417 </GiEffect>
    <AOMstat>    0.4991223 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       145</Level>
    <Effect>   -0.0048197 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -1.6976 </GiEffect>
    <AOMstat>      -1.5856 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       146</Level>
    <Effect>    0.0011913 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.4196089 </GiEffect>
    <AOMstat>    0.3919299 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       147</Level>
    <Effect>  -0.26892865E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.0947231 </GiEffect>
    <AOMstat>   -0.0886842 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       148</Level>
    <Effect>   0.69407489E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.2444699 </GiEffect>
    <AOMstat>    0.2288826 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       149</Level>
    <Effect>   -0.0026047 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.9174426 </GiEffect>
    <AOMstat>   -0.8589490 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       150</Level>
    <Effect>    0.0016877 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.5944373 </GiEffect>
    <AOMstat>    0.5565418 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       151</Level>
    <Effect>   0.90204457E-03 </Effect>
    <seEffect>    0.0531970 </seEffect>
    <GiEffect>    0.3177218 </GiEffect>
    <AOMstat>    0.2976500 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       152</Level>
    <Effect>    0.0038078 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>       1.3412 </GiEffect>
    <AOMstat>       1.2557 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       153</Level>
    <Effect>    0.0030099 </Effect>
    <seEffect>    0.0532023 </seEffect>
    <GiEffect>       1.0601 </GiEffect>
    <AOMstat>       1.0256 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       154</Level>
    <Effect>   0.23415202E-03 </Effect>
    <seEffect>    0.0532016 </seEffect>
    <GiEffect>    0.0824740 </GiEffect>
    <AOMstat>    0.0794008 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       155</Level>
    <Effect>    0.0064824 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       2.2832 </GiEffect>
    <AOMstat>       2.1326 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       156</Level>
    <Effect>   -0.0017421 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.6136007 </GiEffect>
    <AOMstat>   -0.5733887 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       157</Level>
    <Effect>   -0.0025992 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.9155037 </GiEffect>
    <AOMstat>   -0.8555333 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       158</Level>
    <Effect>    0.0028008 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>    0.9865082 </GiEffect>
    <AOMstat>    0.9216309 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       159</Level>
    <Effect>   0.56379662E-03 </Effect>
    <seEffect>    0.0532017 </seEffect>
    <GiEffect>    0.1985827 </GiEffect>
    <AOMstat>    0.1913770 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       160</Level>
    <Effect>  -0.72318955E-03 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.2547248 </GiEffect>
    <AOMstat>   -0.2379228 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       161</Level>
    <Effect>   -0.0013924 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.4904467 </GiEffect>
    <AOMstat>   -0.4580958 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       162</Level>
    <Effect>   -0.0020809 </Effect>
    <seEffect>    0.0532020 </seEffect>
    <GiEffect>   -0.7329348 </GiEffect>
    <AOMstat>   -0.7074011 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       163</Level>
    <Effect>   0.45777613E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.1612398 </GiEffect>
    <AOMstat>    0.1509603 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       164</Level>
    <Effect>   -0.0010232 </Effect>
    <seEffect>    0.0532020 </seEffect>
    <GiEffect>   -0.3603904 </GiEffect>
    <AOMstat>   -0.3478353 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       165</Level>
    <Effect>  -0.21427692E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>   -0.0754735 </GiEffect>
    <AOMstat>   -0.0706618 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       166</Level>
    <Effect>   -0.0029929 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>      -1.0542 </GiEffect>
    <AOMstat>   -0.9869523 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       167</Level>
    <Effect>   -0.0097106 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>      -3.4203 </GiEffect>
    <AOMstat>      -3.1947 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       168</Level>
    <Effect>   -0.0020843 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.7341434 </GiEffect>
    <AOMstat>   -0.6857179 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       169</Level>
    <Effect>   -0.0022607 </Effect>
    <seEffect>    0.0532013 </seEffect>
    <GiEffect>   -0.7962611 </GiEffect>
    <AOMstat>   -0.7654458 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       170</Level>
    <Effect>    0.0042936 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>       1.5123 </GiEffect>
    <AOMstat>       1.4126 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       171</Level>
    <Effect>   0.78158039E-03 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.2752914 </GiEffect>
    <AOMstat>    0.2577397 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       172</Level>
    <Effect>   -0.0030372 </Effect>
    <seEffect>    0.0532402 </seEffect>
    <GiEffect>      -1.0698 </GiEffect>
    <AOMstat>      -1.4186 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       173</Level>
    <Effect>  -0.29759127E-04 </Effect>
    <seEffect>    0.0531965 </seEffect>
    <GiEffect>   -0.0104819 </GiEffect>
    <AOMstat>   -0.0097905 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       174</Level>
    <Effect>   0.75631609E-04 </Effect>
    <seEffect>    0.0531969 </seEffect>
    <GiEffect>    0.0266393 </GiEffect>
    <AOMstat>    0.0249408 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       175</Level>
    <Effect>   -0.0059056 </Effect>
    <seEffect>    0.0531108 </seEffect>
    <GiEffect>      -2.0801 </GiEffect>
    <AOMstat>      -1.3786 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       176</Level>
    <Effect>    0.0072384 </Effect>
    <seEffect>    0.0531108 </seEffect>
    <GiEffect>       2.5495 </GiEffect>
    <AOMstat>       1.6898 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       177</Level>
    <Effect>    0.0091030 </Effect>
    <seEffect>    0.0531112 </seEffect>
    <GiEffect>       3.2063 </GiEffect>
    <AOMstat>       2.1276 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       178</Level>
    <Effect>    0.0043958 </Effect>
    <seEffect>    0.0524574 </seEffect>
    <GiEffect>       1.5483 </GiEffect>
    <AOMstat>    0.4703973 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       179</Level>
    <Effect>    0.0076103 </Effect>
    <seEffect>    0.0523720 </seEffect>
    <GiEffect>       2.6805 </GiEffect>
    <AOMstat>    0.7756292 </AOMstat>
</Equation> <Equation>
    <Model_Term>entry</Model_Term>
    <Level>       180</Level>
    <Effect>    0.0037151 </Effect>
    <seEffect>    0.0525789 </seEffect>
    <GiEffect>       1.3085 </GiEffect>
    <AOMstat>    0.4302530 </AOMstat>
</Equation >
</Solutions >
<WaldFstats>
<WaldFtest>
    <FactorNumber>9</FactorNumber>
    <ModelTerm>mu</ModelTerm>
    <NumDF>1</NumDF>
    <DenDF>      65.1</DenDF>
    <F-inc>  3290.89</F-inc>
    <F-con>  3290.89</F-con>
    <MarginFlag>.</MarginFlag>
    <Probability> &lt;.001 </Probability>
</WaldFtest >
<WaldFtest>
    <FactorNumber>7</FactorNumber>
    <ModelTerm>rep</ModelTerm>
    <NumDF>1</NumDF>
    <DenDF>      90.3</DenDF>
    <F-inc>     1.68</F-inc>
    <F-con>     1.68</F-con>
    <MarginFlag>A</MarginFlag>
    <Probability> 0.199</Probability>
</WaldFtest >
</WaldFstats >
<FinishAt>05 Aug 2021 12:56:52.261</FinishAt>
<Conclusion> Warning: LogL not converged</Conclusion>
</Cycle >
</ASReport >
"""