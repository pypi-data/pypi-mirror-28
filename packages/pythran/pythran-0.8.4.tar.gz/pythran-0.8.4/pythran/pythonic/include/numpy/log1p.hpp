#ifndef PYTHONIC_INCLUDE_NUMPY_LOG1P_HPP
#define PYTHONIC_INCLUDE_NUMPY_LOG1P_HPP

#include "pythonic/include/utils/functor.hpp"
#include "pythonic/include/types/ndarray.hpp"
#include "pythonic/include/utils/numpy_traits.hpp"
#include <boost/simd/function/log1p.hpp>

PYTHONIC_NS_BEGIN

namespace numpy
{
#define NUMPY_NARY_FUNC_NAME log1p
#define NUMPY_NARY_FUNC_SYM boost::simd::log1p
#include "pythonic/include/types/numpy_nary_expr.hpp"
}
PYTHONIC_NS_END

#endif
