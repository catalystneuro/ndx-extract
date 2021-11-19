function results = test_ndx_extract()
% TEST_NDX_EXTRACT Run ndx-extract tests.
%
%   Example:
%
%     % Run tests and return results
%     results = test_ndx_extract()()

import matlab.unittest.TestSuite
generateExtension('../../../spec/ndx-extract.namespace.yaml');
suiteClass = TestSuite.fromClass(?TestInterface);
results = run(suiteClass);
display(results)


