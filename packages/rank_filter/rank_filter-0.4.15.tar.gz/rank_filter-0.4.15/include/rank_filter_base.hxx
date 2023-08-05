#ifndef __RANK_FILTER_BASE__
#define __RANK_FILTER_BASE__


#include <deque>
#include <cassert>
#include <functional>
#include <iostream>
#include <iterator>

#include <boost/array.hpp>
#include <boost/container/set.hpp>
#include <boost/container/node_allocator.hpp>
#include <boost/math/special_functions/round.hpp>
#include <boost/static_assert.hpp>
#include <boost/type_traits.hpp>


namespace rank_filter
{

template<class I1,
         class I2>
inline void lineRankOrderFilter1D(const I1& src_begin, const I1& src_end,
        I2& dest_begin, I2& dest_end,
        size_t half_length, double rank)
{
    // Types in use.
    typedef typename std::iterator_traits<I1>::value_type T1;
    typedef typename std::iterator_traits<I2>::value_type T2;
    typedef typename std::iterator_traits<I1>::difference_type I1_diff_t;
    typedef typename std::iterator_traits<I2>::difference_type I2_diff_t;

    // Establish common types to work with source and destination values.
    BOOST_STATIC_ASSERT((boost::is_same<T1, T2>::value));
    typedef T1 T;
    typedef typename boost::common_type<I1_diff_t, I2_diff_t>::type I_diff_t;

    // Rank must be in the range 0 to 1
    assert((0 <= rank) && (rank <= 1));

    const I_diff_t rank_pos = static_cast<I_diff_t>(boost::math::round(rank * (2 * half_length)));

    // The position of the window.
    I_diff_t window_begin = 0;

    // Lengths.
    const I_diff_t src_size = std::distance(src_begin, src_end);
    const I_diff_t dest_size = std::distance(dest_begin, dest_end);

    typedef boost::container::multiset< T,
            std::less<T>,
            boost::container::node_allocator<T>,
            boost::container::tree_assoc_options< boost::container::tree_type<boost::container::scapegoat_tree> >::type> multiset;

    typedef std::deque< typename multiset::iterator > deque;

    multiset sorted_window;
    deque window_iters(2 * half_length + 1);

    // Get the initial sorted window.
    // Include the reflection.
    for (I_diff_t j = 0; j < half_length; j++)
    {
        window_iters[j] = sorted_window.insert(src_begin[window_begin + half_length - j]);
    }
    for (I_diff_t j = half_length; j < (2 * half_length + 1); j++)
    {
        window_iters[j] = sorted_window.insert(src_begin[window_begin + j - half_length]);
    }

    typename multiset::iterator rank_point = sorted_window.begin();

    for (I_diff_t i = 0; i < rank_pos; i++)
    {
        rank_point++;
    }

    typename multiset::iterator prev_iter;
    T prev_value;
    T next_value;
    while ( window_begin < src_size )
    {
        dest_begin[window_begin] = *rank_point;

        prev_iter = window_iters.front();
        prev_value = *prev_iter;
        window_iters.pop_front();

        window_begin++;

        if ( window_begin == src_size )
        {
            next_value = prev_value;
        }
        else if ( window_begin < (src_size - half_length) )
        {
            next_value = src_begin[window_begin + half_length];
        }
        else
        {
            next_value = *(window_iters[(2 * (src_size - (window_begin + 1)))]);
        }

        if ( ( *rank_point < prev_value ) && ( *rank_point <= next_value ) )
        {
            sorted_window.erase(prev_iter);
            window_iters.push_back(sorted_window.insert(next_value));
        }
        else if ( ( *rank_point >= prev_value ) && ( *rank_point > next_value ) )
        {
            if ( rank_point == prev_iter )
            {
                window_iters.push_back(sorted_window.insert(next_value));
                rank_point--;

                sorted_window.erase(prev_iter);
            }
            else
            {
                sorted_window.erase(prev_iter);
                window_iters.push_back(sorted_window.insert(next_value));
            }
        }
        else if ( ( *rank_point < prev_value ) && ( *rank_point > next_value ) )
        {
            sorted_window.erase(prev_iter);
            window_iters.push_back(sorted_window.insert(next_value));

            rank_point--;
        }
        else if ( ( *rank_point >= prev_value ) && ( *rank_point <= next_value ) )
        {
            if (rank_point == prev_iter)
            {
                window_iters.push_back(sorted_window.insert(next_value));
                rank_point++;

                sorted_window.erase(prev_iter);
            }
            else
            {
                sorted_window.erase(prev_iter);
                window_iters.push_back(sorted_window.insert(next_value));

                rank_point++;
            }
        }
    }
}

}


namespace std
{
    template <class T, size_t N>
    ostream& operator<<(ostream& out, const boost::array<T, N>& that)
    {
        out << "{ ";
        for (unsigned int i = 0; i < (N - 1); i++)
        {
            out << that[i] << ", ";
        }
        out << that[N - 1] << " }";

        return(out);
    }
}


#endif //__RANK_FILTER_BASE__
