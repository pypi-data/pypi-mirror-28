
include(${CMAKE_CURRENT_LIST_DIR}/TiMemoryConfigVersion.cmake)


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was TiMemoryConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

set_and_check(TiMemory_INCLUDE_DIR "${PACKAGE_PREFIX_DIR}/include")
set_and_check(TiMemory_LIB_DIR "${PACKAGE_PREFIX_DIR}/lib")
set_and_check(TiMemory_PYTHON_DIR "${PACKAGE_PREFIX_DIR}")

foreach(_TYPE LIB INCLUDE PYTHON)
    set(TiMemory_${_TYPE}_DIRS ${TiMemory_${_TYPE}_DIR})
endforeach(_TYPE LIB INCLUDE PYTHON)

set(TiMemory_EXTERNAL_INCLUDE_DIRS /opt/local/include/mpich-mp)
foreach(_DIR ${TiMemory_EXTERNAL_INCLUDE_DIRS})
    list(APPEND TiMemory_INCLUDE_DIRS SYSTEM ${_DIR})
endforeach(_DIR ${TiMemory_EXTERNAL_INCLUDE_DIRS})

include(${CMAKE_CURRENT_LIST_DIR}/TiMemoryLibraryDepends.cmake)

if(DEFINED CMAKE_CXX_STANDARD)
    if("${CMAKE_CXX_STANDARD}" VERSION_LESS 11 OR
        "${CMAKE_CXX_STANDARD}" VERSION_GREATER 17)
        set(CMAKE_CXX_STANDARD 11)
        set(CMAKE_CXX_STANDARD_REQUIRED ON)
    endif("${CMAKE_CXX_STANDARD}" VERSION_LESS 11 OR
        "${CMAKE_CXX_STANDARD}" VERSION_GREATER 17)
endif(DEFINED CMAKE_CXX_STANDARD)

check_required_components(TiMemory)

get_target_property(_STATIC_LOCATION timemory-static IMPORTED_LOCATION_RELEASE)

# try to get imported location
foreach(_LIBTYPE SHARED STATIC)

    string(TOUPPER "${CMAKE_BUILD_TYPE}" _BUILD_TYPE)
    if("${CMAKE_BUILD_TYPE}" MATCHES "${CMAKE_CONFIGURATION_TYPES}")
        set(IMPORTED_LOCATION_BUILD IMPORTED_LOCATION_${_BUILD_TYPE})
    else("${CMAKE_BUILD_TYPE}" MATCHES "${CMAKE_CONFIGURATION_TYPES}")
        set(IMPORTED_LOCATION_BUILD )
    endif("${CMAKE_BUILD_TYPE}" MATCHES "${CMAKE_CONFIGURATION_TYPES}")

    foreach(_LOC
            IMPORTED_LOCATION
            ${IMPORTED_LOCATION_BUILD}
            IMPORTED_LOCATION_RELEASE
            IMPORTED_LOCATION_RELWITHDEBINFO
            IMPORTED_LOCATION_DEBUG
            IMPORTED_LOCATION_MINSIZEREL)
        if(NOT _${_LIBTYPE}_LOCATION)
            get_target_property(_SHARED_LOCATION timemory-shared ${_LOC})
        endif(NOT _${_LIBTYPE}_LOCATION)
    endforeach(_LOC
            IMPORTED_LOCATION
            ${IMPORTED_LOCATION_BUILD}
            IMPORTED_LOCATION_RELEASE
            IMPORTED_LOCATION_RELWITHDEBINFO
            IMPORTED_LOCATION_DEBUG
            IMPORTED_LOCATION_MINSIZEREL)

    STRING(TOLOWER "${_LIBTYPE}" _LIBTAG)
    if(_${_LIBTYPE}_LOCATION)
        set(TiMemory_${_LIBTYPE}_LIBRARY ${_${_LIBTYPE}_LOCATION}
            CACHE INTERNAL "TiMemory ${_LIBTAG} library")
    else(_${_LIBTYPE}_LOCATION)
        set(TiMemory_${_LIBTYPE}_LIBRARY timemory-${_LIBTAG}
            CACHE INTERNAL "TiMemory ${_LIBTAG} library")
    endif(_${_LIBTYPE}_LOCATION)

    unset(_${_LIBTYPE}_LOCATION)

endforeach(_LIBTYPE SHARED STATIC)

if(BUILD_SHARED_LIBRARIES)
    set(TiMemory_LIBRARIES timemory-shared)
elseif(BUILD_STATIC_LIBRARIES)
    set(TiMemory_LIBRARIES timemory-static)
else()
    set(TiMemory_LIBRARIES timemory-shared)
endif(BUILD_SHARED_LIBRARIES)

add_definitions(-DNAME_TIM=tim)
if(OFF)
    add_definitions(-DTIMEMORY_EXCEPTIONS)
endif(OFF)

set(TiMemory_C_FLAGS "")
set(TiMemory_CXX_FLAGS "-W -Wall -Wextra -Wno-unknown-warning-option -Wno-implicit-fallthrough -Wno-unused-parameter -Wno-shadow-field-in-constructor-modified -Wno-unused-private-field -Wno-exceptions -Wunused-but-set-parameter -Wno-unused-variable -pthread -std=c++${CMAKE_CXX_STANDARD}")
set(TIMEMORY_USE_MPI TRUE)

if(TIMEMORY_USE_MPI)
    add_definitions(-DTIMEMORY_USE_MPI)
endif(TIMEMORY_USE_MPI)

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set UnitTest++_FOUND to TRUE
# if all listed variables are TRUE
find_package_handle_standard_args(TiMemory DEFAULT_MSG
    TiMemory_LIBRARIES
    TiMemory_INCLUDE_DIR
    TiMemory_PYTHON_DIR)
