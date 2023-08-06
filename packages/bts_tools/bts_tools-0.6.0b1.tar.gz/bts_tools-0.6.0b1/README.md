BitShares delegate tools
------------------------

The BTS Tools will help you build, run and monitor any Graphene-based client
(currently BitShares, Steem, Muse, PeerPlays).

There are 2 tools currently provided:

- command line utility allowing to quickly build and run any graphene-based client
- web application allowing to monitor a running instance of the client and send
  an email or push notification on failure

If you like these tools, please vote for
[witness wackou](https://steemit.com/witness-category/@wackou/wackou-witness-post)
on the Steem, BitShares and Muse networks. Thanks!


Documentation
=============

The main documentation for the tools, as well as a tutorial, can be found
on [ReadTheDocs](http://bts-tools.readthedocs.io/).


Command-line client
===================

just run the ``bts`` script with the command you want to execute:

    $ bts -h
    usage: bts [-h] [-p PIDFILE] [-f]
               {version,clean_homedir,clean,build,build_gui,run,run_cli,run_gui,list,monitor,deploy,deploy_node}
               [environment] [args [args ...]]
    
    following commands are available:
      - version                : show version of the tools
      - clean_homedir          : clean home directory. WARNING: this will delete your wallet!
      - save_blockchain_dir    : save a snapshot of the current state of the blockchain
      - restore_blockchain_dir : restore a snapshot of the current state of the blockchain
      - clean                  : clean build directory
      - build                  : update and build bts client
      - build_gui              : update and build bts gui client
      - run                    : run latest compiled bts client, or the one with the given hash or tag
      - run_cli                : run latest compiled bts cli wallet
      - run_gui                : run latest compiled bts gui client
      - list                   : list installed bts client binaries
      - monitor                : run the monitoring web app
      - deploy                 : deploy built binaries to a remote server
      - deploy_node            : full deploy of a seed or witness node on given ip address. Needs ssh root access
    
    Examples:
      $ bts build                 # build the latest bts client by default
      $ bts build v0.4.27         # build specific version
      $ bts build ppy-dev v0.1.8  # build a specific client/version
      $ bts run                   # run the latest compiled client by default
      $ bts run seed-test         # clients are defined in the config.yaml file
    
      $ bts build_gui   # FIXME: broken...
      $ bts run_gui     # FIXME: broken...
    
    
    
    positional arguments:
      {version,clean_homedir,clean,build,build_gui,run,run_cli,run_gui,list,monitor,deploy,deploy_node}
                            the command to run
      environment           the build/run environment (bts, steem, ...)
      args                  additional arguments to be passed to the given command
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PIDFILE, --pidfile PIDFILE
                            filename in which to write PID of child process
      -f, --forward-signals
                            forward unix signals to spawned witness client child process
    
    You should also look into ~/.bts_tools/config.yaml to tune it to your liking.


Monitoring web app
==================

To run the debug/development monitoring web app, just do the following:

    $ bts monitor
    
and it will launch on ``localhost:5000``.

For production deployments, it is recommended to put it behind a WSGI server, in which case the
entry point is ``bts_tools.wsgi:application``.

Do not forget to edit the ``~/.bts_tools/config.yaml`` file to configure it to suit your needs.
     

### Screenshots ###

You can see a live instance of the bts tools monitoring the state of the
seed nodes I am making available for the BitShares, Muse and Steem networks
here: http://seed.steemnodes.com
