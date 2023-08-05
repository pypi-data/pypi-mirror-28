aws
===

The Amazon Web Services (AWS) provider manages multiple types of resources.

aws_ec2
-------

Openstack Instances can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/os-server-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/os_server_module.html>`_

aws_ec2_key
-----------

AWS SSH keys can be added using this resource.

* :docs1.5:`Topology Example <workspace/topologies/aws-ec2-key-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/ec2_key_module.html>`_

.. note:: This resource will not be torn down during a :term:`destroy`
   action. This is because other resources may depend on the now existing
   resource.

aws_s3
------

AWS Simple Storage Service buckets can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/aws-s3-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/aws_s3_module.html>`_

.. note:: This resource will not be torn down during a :term:`destroy`
   action. This is because other resources may depend on the now existing
   resource.

aws_sg
------

AWS Security Groups can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/aws-sg-new.yml>`
* `Ansible EC2 Security Group module <http://docs.ansible.com/ansible/latest/ec2_group_module.html>`_

.. note:: This resource will not be torn down during a :term:`destroy`
   action. This is because other resources may depend on the now existing
   resource.

Additional Dependencies
-----------------------

No additional dependencies are required for the Openstack Provider.

Credentials Management
----------------------

AWS provides several ways to provide credentials. LinchPin supports
some of these methods for passing credentials for use with openstack resources.

Environment Variables
`````````````````````

LinchPin honors the AWS environment variables

Provisioning
````````````

Provisioning with credentials uses the ``--creds-path`` option.

.. code-block:: bash

   $ linchpin -v --creds-path ~/.config/aws up

Alternatively, the credentials path can be set as an environment variable,

.. code-block:: bash

   $ export CREDS_PATH="~/.config/aws"
   $ linchpin -v up

