# scripts

This directory contains various scripts to perform analysis tasks.  
The general assumed structure are like the following:  

    CORE/
        .git/
        ...
        Makefile
        CMS3_CORE.so
        ...
    YOUR_CORE/
        .git/
        ...
        Makefile
        libYOUR_CORE.so
        ...
    SOME_PACKAGE/
        .git/
        ...
        Makefile
        libYourPackage.so
        ...
    ProjectMetis/ # https://github.com/aminnj/ProjectMetis
        .git/
        ...
        Makefile
        libYourPackage.so
        ...
    plottery/ # https://github.com/aminnj/plottery
        .git/
        ...
        Makefile
        libYourPackage.so
        ...
    .git
    ScanChain.C # your looper or whatever
    ...
    ScanChain.h
    ...
    bootstrap.sh
    ...
    scripts/ # <---- this package
        .git
        setup.sh
        root.sh
        run.sh
        run.C
        ...

See [this WWW analysis code](https://github.com/sgnoohc/www) as an example.
In particular note the ```bootstrap.sh``` in that package.

Once you have setup like this, you setup your ```scripts/``` like

    $ source scripts/setup.sh

The ```scripts/``` assumes ```ScanChain.C``` or whichever is your looper has EXACTLY the following format:

    void ScanChain(TChain* chain, TString output_name, TString option_string, int nevents)

Then, you can run over a root file with this ScanChain by issuing a command like:

    $ run.sh /path/to/ScanChain.C /path/to/output.root Events 1000 'OptionString' '/hadoop/cms/store/blah/cms3/NewPhysicsMCNtuple/merged_*.root,/hadoop/cms/store/blah/cms3/SuckySMBkg/merged_*.root'
             ^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^^ ^^^^^^ ^^^^ ^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             Use this ScanChain   Make your output      Tree   #   Any additional  Comma separated list of inputs or input pattern.
                                  based on what each    in     of  options         Please note that when using wildcards '*' use quotes properly.
                                  ScanChain does        input  evt ScanChain needs Also, you can only use wildcards at the base level names. (e.g. merged_*.root and not /hadoop/*/*/merged*.root)
                                                               to                                                                                                                ^ ^
                                                               run                                                                                                          These will fail. (feature request?)


