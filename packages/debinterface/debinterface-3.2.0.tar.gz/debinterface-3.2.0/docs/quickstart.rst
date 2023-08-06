Quickstart
============

.. sourcecode:: python

    import debinterface

    # Get a collection of objects representing the network adapters.
    adapters = debinterface.Interfaces().adapters

    # You get a list you can iterare over.
    # Each adapter has an 'export()' method that returns a dictionary of its options.
    # You can print the name of each adapter as follows:
    for adapter in adapters:
    	item = adapter.export()
    	print(item['name'])

    # Write your new interfaces file as follows:
    # Any changes made with setter methods will be reflected with the new write.
    interfaces = debinterface.Interfaces()
    interfaces.writeInterfaces()

    # A backup of your old interfaces file will be generated when writing over the previous interfaces file
    # By defaults these paths are used :
    # INTERFACES_PATH='/etc/network/interfaces'
    # BACKUP_PATH='/etc/network/interfaces.old'
    # Paths can be customized when instanciating the Interfaces class:
    interfaces = debinterface.Interfaces(interfaces_path='/home/interfaces', backup_path='/another/custom/path')

    # By defaults, interfaces file is read when instanciating the Interfaces class, to do it lazyly:
    interfaces = debinterface.Interfaces(update_adapters=False)
    interfaces.updateAdapters()
