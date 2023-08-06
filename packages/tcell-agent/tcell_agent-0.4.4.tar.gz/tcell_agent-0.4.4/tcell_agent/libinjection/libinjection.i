%module libinjection

%{
  #include "libinjection.h"
  #include "libinjection_sqli.h"
  #include <stddef.h>

  int is_sqli(const char* s, size_t slen)
  {
    char fingerprint[8];
    int result = libinjection_sqli(s, slen, fingerprint);
    /*printf("Received an integer : %s\n", &fingerprint[0]);*/
    return result;
  }
%}

%include "typemaps.i"

// automatically append string length into arg array
%apply (char *STRING, size_t LENGTH) { (const char *s, size_t slen) };


// The C functions all start with 'libinjection_' as a namespace
// We don't need this since it's in the libinjection ruby module
// i.e. libinjection.libinjection_is_sqli --> libinjection.is_sqli
//
%rename(is_xss) libinjection_xss;
%rename(is_sqli_state) libinjection_is_sqli;
%rename("%(strip:[libinjection_])s") "";

%include "libinjection.h"
%include "libinjection_sqli.h"

int is_sqli(const char* s, size_t slen);
