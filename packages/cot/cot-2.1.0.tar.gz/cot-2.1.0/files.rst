OVF/OVA Associated Files
------------------------

An interesting thing about OVF is that it provides several different types and
levels of file reference and validation:

- The optional manifest file, which lists files and provides their checksums
- The References section in the OVF descriptor, which lists files, and
  optionally their sizes
- The optional certificate file (not currently supported by COT)
- The Disks section in the OVF descriptor...? TODO

A minimally specified OVF/OVA might just have:

- a list of file paths in its References section

A maximally specified OVF/OVA might have:

- a list of file paths and associated sizes in its References
- a manifest, giving a checksum of the above descriptor and all other files
- a certificate, signing the manifest itself

At input time (loading an OVF/OVA into COT), we should:

- if a manifest is present, see if all given checksums are valid (including the
  descriptor itself).
- after loading the descriptor:

  - if we have a manifest, its file listing must match the References file
    listing (excluding the descriptor itself)
  - if file(s) listed in the References include sizes, make sure they are valid.

When writing out from COT, we always provide the maximal specification that
we currently support - meaning we always output file sizes in the References
and generate a manifest file. (Again, no support for certificates yet.)

So in essence the workflow is:

- Load OVF/OVA - validate manifest and references
- Make changes, update file information as needed due to changes
- Before output, re-validate existing info and populate missing info as needed
