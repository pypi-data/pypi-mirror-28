#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "timemory-shared" for configuration "Release"
set_property(TARGET timemory-shared APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(timemory-shared PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libtimemory.1.0.0.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libtimemory.1.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS timemory-shared )
list(APPEND _IMPORT_CHECK_FILES_FOR_timemory-shared "${_IMPORT_PREFIX}/lib/libtimemory.1.0.0.dylib" )

# Import target "timemory-static" for configuration "Release"
set_property(TARGET timemory-static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(timemory-static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libtimemory.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS timemory-static )
list(APPEND _IMPORT_CHECK_FILES_FOR_timemory-static "${_IMPORT_PREFIX}/lib/libtimemory.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
