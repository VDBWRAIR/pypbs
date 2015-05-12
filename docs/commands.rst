===================
Additional Commands
===================

pbsstatus
=========

pbsstatus is a quick view of your cluster's utilization

.. code-block:: bash

    $> pbsstatus

    NP Utilization	Cluster Load	Avail CPU	Used CPU	Total CPU	Running Jobs
            28.12%	      20.20%	       23	       9	       32	           9

qpeek
=====

qpeek is a a bit of a rewrite for the qpeek perl script that is a little more 
robust

Qsub a simple job

.. code-block:: bash

    $> cat <<EOF | qsub -l nodes=1,walltime=00:01:00
    while sleep 2
    do
        echo "HI"
    done
    EOF
    1.host.example.com

Cat the output of the job

.. code-block:: bash

    $> qpeek 1.host.example.com
    HI
    HI
    HI

Tail the output of the job in real-time

.. code-block:: bash

    $> qpeek --operation follow 1.host.example.com
    HI
    HI
    HI
