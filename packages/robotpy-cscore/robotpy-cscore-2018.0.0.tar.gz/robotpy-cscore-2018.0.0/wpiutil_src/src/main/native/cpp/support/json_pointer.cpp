/*----------------------------------------------------------------------------*/
/* Modifications Copyright (c) FIRST 2017. All Rights Reserved.               */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/
/*
    __ _____ _____ _____
 __|  |   __|     |   | |  JSON for Modern C++
|  |  |__   |  |  | | | |  version 2.1.1
|_____|_____|_____|_|___|  https://github.com/nlohmann/json

Licensed under the MIT License <http://opensource.org/licenses/MIT>.
Copyright (c) 2013-2017 Niels Lohmann <http://nlohmann.me>.

Permission is hereby  granted, free of charge, to any  person obtaining a copy
of this software and associated  documentation files (the "Software"), to deal
in the Software  without restriction, including without  limitation the rights
to  use, copy,  modify, merge,  publish, distribute,  sublicense, and/or  sell
copies  of  the Software,  and  to  permit persons  to  whom  the Software  is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE  IS PROVIDED "AS  IS", WITHOUT WARRANTY  OF ANY KIND,  EXPRESS OR
IMPLIED,  INCLUDING BUT  NOT  LIMITED TO  THE  WARRANTIES OF  MERCHANTABILITY,
FITNESS FOR  A PARTICULAR PURPOSE AND  NONINFRINGEMENT. IN NO EVENT  SHALL THE
AUTHORS  OR COPYRIGHT  HOLDERS  BE  LIABLE FOR  ANY  CLAIM,  DAMAGES OR  OTHER
LIABILITY, WHETHER IN AN ACTION OF  CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE  OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
#define WPI_JSON_IMPLEMENTATION
#include "support/json.h"

#include <algorithm>
#include <numeric> // accumulate

using namespace wpi;

std::string json::json_pointer::to_string() const noexcept
{
    return std::accumulate(reference_tokens.begin(),
                           reference_tokens.end(), std::string{},
                           [](const std::string & a, const std::string & b)
    {
        return a + "/" + escape(b);
    });
}

json::reference json::json_pointer::get_and_create(reference j) const
{
    pointer result = &j;

    // in case no reference tokens exist, return a reference to the
    // JSON value j which will be overwritten by a primitive value
    for (const auto& reference_token : reference_tokens)
    {
        switch (result->m_type)
        {
            case value_t::null:
            {
                if (reference_token == "0")
                {
                    // start a new array if reference token is 0
                    result = &result->operator[](0);
                }
                else
                {
                    // start a new object otherwise
                    result = &result->operator[](reference_token);
                }
                break;
            }

            case value_t::object:
            {
                // create an entry in the object
                result = &result->operator[](reference_token);
                break;
            }

            case value_t::array:
            {
                // create an entry in the array
                JSON_TRY
                {
                    result = &result->operator[](static_cast<size_type>(std::stoi(reference_token)));
                }
                JSON_CATCH (std::invalid_argument&)
                {
                    JSON_THROW(parse_error::create(109, 0, "array index '" + reference_token + "' is not a number"));
                }
                break;
            }

            /*
            The following code is only reached if there exists a
            reference token _and_ the current value is primitive. In
            this case, we have an error situation, because primitive
            values may only occur as single value; that is, with an
            empty list of reference tokens.
            */
            default:
            {
                JSON_THROW(type_error::create(313, "invalid value to unflatten"));
            }
        }
    }

    return *result;
}

json::reference json::json_pointer::get_unchecked(pointer ptr) const
{
    for (const auto& reference_token : reference_tokens)
    {
        // convert null values to arrays or objects before continuing
        if (ptr->m_type == value_t::null)
        {
            // check if reference token is a number
            const bool nums = std::all_of(reference_token.begin(),
                                          reference_token.end(),
                                          [](const char x)
            {
                return (x >= '0' && x <= '9');
            });

            // change value to array for numbers or "-" or to object
            // otherwise
            if (nums || reference_token == "-")
            {
                *ptr = value_t::array;
            }
            else
            {
                *ptr = value_t::object;
            }
        }

        switch (ptr->m_type)
        {
            case value_t::object:
            {
                // use unchecked object access
                ptr = &ptr->operator[](reference_token);
                break;
            }

            case value_t::array:
            {
                // error condition (cf. RFC 6901, Sect. 4)
                if (reference_token.size() > 1 && reference_token[0] == '0')
                {
                    JSON_THROW(parse_error::create(106, 0, "array index '" + reference_token + "' must not begin with '0'"));
                }

                if (reference_token == "-")
                {
                    // explicitly treat "-" as index beyond the end
                    ptr = &ptr->operator[](ptr->m_value.array->size());
                }
                else
                {
                    // convert array index to number; unchecked access
                    JSON_TRY
                    {
                        ptr = &ptr->operator[](static_cast<size_type>(std::stoi(reference_token)));
                    }
                    JSON_CATCH (std::invalid_argument&)
                    {
                        JSON_THROW(parse_error::create(109, 0, "array index '" + reference_token + "' is not a number"));
                    }
                }
                break;
            }

            default:
            {
                JSON_THROW(out_of_range::create(404, "unresolved reference token '" + reference_token + "'"));
            }
        }
    }

    return *ptr;
}

json::reference json::json_pointer::get_checked(pointer ptr) const
{
    for (const auto& reference_token : reference_tokens)
    {
        switch (ptr->m_type)
        {
            case value_t::object:
            {
                // note: at performs range check
                ptr = &ptr->at(reference_token);
                break;
            }

            case value_t::array:
            {
                if (reference_token == "-")
                {
                    // "-" always fails the range check
                    JSON_THROW(out_of_range::create(402, "array index '-' (" +
                                                    std::to_string(ptr->m_value.array->size()) +
                                                    ") is out of range"));
                }

                // error condition (cf. RFC 6901, Sect. 4)
                if (reference_token.size() > 1 && reference_token[0] == '0')
                {
                    JSON_THROW(parse_error::create(106, 0, "array index '" + reference_token + "' must not begin with '0'"));
                }

                // note: at performs range check
                JSON_TRY
                {
                    ptr = &ptr->at(static_cast<size_type>(std::stoi(reference_token)));
                }
                JSON_CATCH (std::invalid_argument&)
                {
                    JSON_THROW(parse_error::create(109, 0, "array index '" + reference_token + "' is not a number"));
                }
                break;
            }

            default:
            {
                JSON_THROW(out_of_range::create(404, "unresolved reference token '" + reference_token + "'"));
            }
        }
    }

    return *ptr;
}

json::const_reference json::json_pointer::get_unchecked(const_pointer ptr) const
{
    for (const auto& reference_token : reference_tokens)
    {
        switch (ptr->m_type)
        {
            case value_t::object:
            {
                // use unchecked object access
                ptr = &ptr->operator[](reference_token);
                break;
            }

            case value_t::array:
            {
                if (reference_token == "-")
                {
                    // "-" cannot be used for const access
                    JSON_THROW(out_of_range::create(402, "array index '-' (" +
                                                    std::to_string(ptr->m_value.array->size()) +
                                                    ") is out of range"));
                }

                // error condition (cf. RFC 6901, Sect. 4)
                if (reference_token.size() > 1 && reference_token[0] == '0')
                {
                    JSON_THROW(parse_error::create(106, 0, "array index '" + reference_token + "' must not begin with '0'"));
                }

                // use unchecked array access
                JSON_TRY
                {
                    ptr = &ptr->operator[](static_cast<size_type>(std::stoi(reference_token)));
                }
                JSON_CATCH (std::invalid_argument&)
                {
                    JSON_THROW(parse_error::create(109, 0, "array index '" + reference_token + "' is not a number"));
                }
                break;
            }

            default:
            {
                JSON_THROW(out_of_range::create(404, "unresolved reference token '" + reference_token + "'"));
            }
        }
    }

    return *ptr;
}

json::const_reference json::json_pointer::get_checked(const_pointer ptr) const
{
    for (const auto& reference_token : reference_tokens)
    {
        switch (ptr->m_type)
        {
            case value_t::object:
            {
                // note: at performs range check
                ptr = &ptr->at(reference_token);
                break;
            }

            case value_t::array:
            {
                if (reference_token == "-")
                {
                    // "-" always fails the range check
                    JSON_THROW(out_of_range::create(402, "array index '-' (" +
                                                    std::to_string(ptr->m_value.array->size()) +
                                                    ") is out of range"));
                }

                // error condition (cf. RFC 6901, Sect. 4)
                if (reference_token.size() > 1 && reference_token[0] == '0')
                {
                    JSON_THROW(parse_error::create(106, 0, "array index '" + reference_token + "' must not begin with '0'"));
                }

                // note: at performs range check
                JSON_TRY
                {
                    ptr = &ptr->at(static_cast<size_type>(std::stoi(reference_token)));
                }
                JSON_CATCH (std::invalid_argument&)
                {
                    JSON_THROW(parse_error::create(109, 0, "array index '" + reference_token + "' is not a number"));
                }
                break;
            }

            default:
            {
                JSON_THROW(out_of_range::create(404, "unresolved reference token '" + reference_token + "'"));
            }
        }
    }

    return *ptr;
}

std::vector<std::string> json::json_pointer::split(const std::string& reference_string)
{
    std::vector<std::string> result;

    // special case: empty reference string -> no reference tokens
    if (reference_string.empty())
    {
        return result;
    }

    // check if nonempty reference string begins with slash
    if (reference_string[0] != '/')
    {
        JSON_THROW(parse_error::create(107, 1, "JSON pointer must be empty or begin with '/' - was: '" + reference_string + "'"));
    }

    // extract the reference tokens:
    // - slash: position of the last read slash (or end of string)
    // - start: position after the previous slash
    for (
        // search for the first slash after the first character
        size_t slash = reference_string.find_first_of('/', 1),
        // set the beginning of the first reference token
        start = 1;
        // we can stop if start == string::npos+1 = 0
        start != 0;
        // set the beginning of the next reference token
        // (will eventually be 0 if slash == std::string::npos)
        start = slash + 1,
        // find next slash
        slash = reference_string.find_first_of('/', start))
    {
        // use the text between the beginning of the reference token
        // (start) and the last slash (slash).
        auto reference_token = reference_string.substr(start, slash - start);

        // check reference tokens are properly escaped
        for (size_t pos = reference_token.find_first_of('~');
                pos != std::string::npos;
                pos = reference_token.find_first_of('~', pos + 1))
        {
            assert(reference_token[pos] == '~');

            // ~ must be followed by 0 or 1
            if (pos == reference_token.size() - 1 ||
                    (reference_token[pos + 1] != '0' &&
                     reference_token[pos + 1] != '1'))
            {
                JSON_THROW(parse_error::create(108, 0, "escape character '~' must be followed with '0' or '1'"));
            }
        }

        // finally, store the reference token
        unescape(reference_token);
        result.push_back(reference_token);
    }

    return result;
}

/*!
@brief replace all occurrences of a substring by another string

@param[in,out] s  the string to manipulate; changed so that all
                  occurrences of @a f are replaced with @a t
@param[in]     f  the substring to replace with @a t
@param[in]     t  the string to replace @a f

@pre The search string @a f must not be empty. **This precondition is
     enforced with an assertion.**

@since version 2.0.0
*/
void json::json_pointer::replace_substring(std::string& s,
                              const std::string& f,
                              const std::string& t)
{
    assert(!f.empty());

    for (
        size_t pos = s.find(f);         // find first occurrence of f
        pos != std::string::npos;       // make sure f was found
        s.replace(pos, f.size(), t),    // replace with t
        pos = s.find(f, pos + t.size()) // find next occurrence of f
    );
}

/// escape tilde and slash
std::string json::json_pointer::escape(std::string s)
{
    // escape "~"" to "~0" and "/" to "~1"
    replace_substring(s, "~", "~0");
    replace_substring(s, "/", "~1");
    return s;
}

/// unescape tilde and slash
void json::json_pointer::unescape(std::string& s)
{
    // first transform any occurrence of the sequence '~1' to '/'
    replace_substring(s, "~1", "/");
    // then transform any occurrence of the sequence '~0' to '~'
    replace_substring(s, "~0", "~");
}

void json::json_pointer::flatten(const std::string& reference_string,
                    const json& value,
                    json& result)
{
    switch (value.m_type)
    {
        case value_t::array:
        {
            if (value.m_value.array->empty())
            {
                // flatten empty array as null
                result[reference_string] = nullptr;
            }
            else
            {
                // iterate array and use index as reference string
                for (size_t i = 0; i < value.m_value.array->size(); ++i)
                {
                    flatten(reference_string + "/" + std::to_string(i),
                            value.m_value.array->operator[](i), result);
                }
            }
            break;
        }

        case value_t::object:
        {
            if (value.m_value.object->empty())
            {
                // flatten empty object as null
                result[reference_string] = nullptr;
            }
            else
            {
                // iterate object and use keys as reference string
                for (const auto& element : *value.m_value.object)
                {
                    flatten(reference_string + "/" + escape(element.first()),
                            element.second, result);
                }
            }
            break;
        }

        default:
        {
            // add primitive value with its reference string
            result[reference_string] = value;
            break;
        }
    }
}

json json::json_pointer::unflatten(const json& value)
{
    if (!value.is_object())
    {
        JSON_THROW(type_error::create(314, "only objects can be unflattened"));
    }

    // we need to iterate over the object values in sorted key order
    llvm::SmallVector<llvm::StringMapConstIterator<json>, 64> sorted;
    for (auto i = value.m_value.object->begin(),
         end = value.m_value.object->end(); i != end; ++i)
    {
        if (!i->second.is_primitive())
        {
            JSON_THROW(type_error::create(315, "values in object must be primitive"));
        }
        sorted.push_back(i);
    }
    std::sort(sorted.begin(), sorted.end(),
              [](const llvm::StringMapConstIterator<json>& a,
                 const llvm::StringMapConstIterator<json>& b) {
                return a->getKey() < b->getKey();
              });

    json result;

    // iterate the sorted JSON object values
    for (const auto& element : sorted)
    {

        // assign value to reference pointed to by JSON pointer; Note
        // that if the JSON pointer is "" (i.e., points to the whole
        // value), function get_and_create returns a reference to
        // result itself. An assignment will then create a primitive
        // value.
        json_pointer(element->first()).get_and_create(result) = element->second;
    }

    return result;
}

