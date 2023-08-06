#ifndef PYTHONIC_OPERATOR_IFLOORDIV_HPP
#define PYTHONIC_OPERATOR_IFLOORDIV_HPP

#include "pythonic/include/operator_/ifloordiv.hpp"

#include "pythonic/utils/functor.hpp"

PYTHONIC_NS_BEGIN

namespace operator_
{

  template <class A, class B>
  A ifloordiv(A a, B const &b)
  {
    A tmp = (a - (a % b)) / b;
    a = tmp;
    return tmp;
  }

  DEFINE_FUNCTOR(pythonic::operator_, ifloordiv);
}
PYTHONIC_NS_END

#endif
