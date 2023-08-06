Release History
===============

**1.0.0 2018-01-22**

*   now properly handling CTL-D equal to quit and bye, CTL-C now interrupts
    running commands

**0.2.3 2017-11-24**

*   added ``url -u``, used to generate a pre-signed URL for upload

**0.2.2 2017-11-03**

*   created a build procedure for pyinstaller that works on macOS and Linux,
    as well.
*   edited installation page of the documentation.

**0.2.1 2017-03-08**

*   re-factored the hs3sh package to be able to use pyinstaller for packaging

**0.2.0 2017-01-16**

*   Changes:

    *   Added a section to the documentation describing how to patch *boto3*
        in case MultiPartUpload fails with some compatible S3 stores

**0.1.19 2016-11-30**

*   Changes:

    *   Now making sure that *ls* won't fail on missing *size*
        attribute

**0.1.18 2016-11-28**

*   Changes:

    *   Now making sure that *ls* won't fail on missing *last_modified*
        attribute

**0.1.17 2016-07-24**

*   Changes:

    *   Configuration for Vagrant
    *   fixed a bug regarding multipart upload
    *   re-build to be able to use pyinstaller

**0.1.16 2016-06-14**

*   Changes:

    *   for *put*, added ContentLength header to the request

**0.1.15 2016-05-03**

*   Changes:

    *   profiles now require https (bool), port (int), region (str)
        to allow for S3 storage targets not using the default ports
    *   Lots of small compatibility fixes
    *   Multipart PUT now allows to attach metadata key-/value-pairs
    *   new *run* command, allowing to use batch command files
    *   added missing error handling for *bucket -v*
    *   added upload progess meter for *put -m*
    *   fixed a bug that caused *time* to fail if no cmd has been given


**0.1.14 2016-04-01**

*   Changes:

    *   Command *acl* now implemented for buckets (object ACLs still not
        implemented)

**0.1.13 2016-03-25**

*   Fixed:

    *   A situation where *url* came up with a false URL when working on a
        compatible storage service

**0.1.12 2016-03-25**

*   Changes:

    *   Command *put* now supports multipart upload (``-m``)
    *   New command *url* generates a pre-signed URL for object access

**0.1.11 2016-03-23**

*   Changes:

    *   Now most commands output can be re-directed (\|, \>, \>\>)

**0.1.10 2016-03-19**

*   Changes:

    *   Now showing versioning status in *lsb*

**0.1.9 2016-03-16**

*   Changes:

    *   Replaced mkbucket/rmbucket with bucket
    *   Added the *acl* command

**0.1.8 2016-03-08**

*   Changes:

    *   Added command *lsp* to show the loaded profiles
    *   Fixed a bug that caused just one metapair being stored

**0.1.7 2016-03-08**

*   Fixed:

    *   A bug that caused *mkbucket* to crash
    *   Error message formatting

**0.1.6 2016-03-07**

*   Changed:

    *   Output of errors with length > 79 chars
    *   Added bucketacl and objectacl commands

**0.1.5 2016-03-06**

*   Changes:

    *   Introduces profiles and the .hs3sh.conf configuration file
    *   Added the *time* command to measure the processing time of commands

