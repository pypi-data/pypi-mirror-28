Items and Hardware and Profiles, oh my!
=======================================

Let's talk about the complexities inherent in handling OVF hardware definition
and configuration profiles, why I initially implemented the OVFHardware and
OVFItem classes the way I did, and whether there's a more elegant way out.

Background
----------

The most relevant section of the `OVF standard`_ is section 9.8, which
describes the *optional* ``DeploymentOptionSection`` of the OVF descriptor.
Some key excerpts from this section:

..

    Only one ``DeploymentOptionSection`` section shall be present.

..

    ``Configuration`` elements (...) shall have identifiers specified by the
    ``ovf:id`` attribute that are unique in the OVF package.

..

    A default ``Configuration`` element may be specified with the optional
    ``ovf:default`` attribute. Only one default ``Configuration`` element
    shall be specified. If no default is specified, the first element in the
    list is the default.

..

    Each ``Item`` (...) has an optional ``ovf:configuration`` attribute,
    containing a list of configurations separated by a single space character.
    If not specified, the item shall be selected for any configuration.
    If specified, the item shall be selected only if the chosen configuration
    ID is in the list. A configuration attribute shall not contain a
    configuration ID that is not specified in the ``DeploymentOptionSection``.

..

    (...) [M]ultiple ``Item`` (...) elements are allowed to refer to the same
    InstanceID. A single combined ``Item`` (...) for the given InstanceID
    shall be constructed by picking up the child elements of each ``Item``
    (...) with child elements of a former ``Item`` (...) not being picked up
    if there is a like-named child element in a latter ``Item`` (...)
    Any attributes specified on child elements (...) that are not picked up
    that way, are not part of the combined ``Item``

..

    All ``Item`` (...) elements shall specify ``ResourceType``, and (...)
    elements with the same InstanceID shall agree on ``ResourceType``.

Observations
------------

DeploymentOptionSection (and hence, Configurations) are optional
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Several general possibilities COT may encounter in an OVF:

1. No DeploymentOptionSection means no Configurations are defined.
   In this case, there is a single implied default configuration, and all
   Items implicitly belong to this configuration.
2. DeploymentOptionSection exists and defines one or more Configurations.
   In this case, any Item that does not declare any Configuration references
   implicitly applies to all configurations, while any Item that declares
   Configurations belongs only to those.

We can simplify things by recognizing that as far as Item handling goes,
case #1 is just a subset of case #2 -- all Items belong to all Configurations,
there just happens to only be a single (implicit) Configuration.

Note also that either we have a single implicit Configuration or we have
one or more explicitly declared Configurations -- never a mixture of
implicit and explicit.

ResourceType/InstanceID linkage
'''''''''''''''''''''''''''''''

The constraint that InstanceID and ResourceType must always agree greatly
simplifies what could otherwise be a very complex scenario. In essence,
for any given InstanceID, there is exactly one valid ResourceType,
and so for any given Configuration, either:

1. An item exists with this InstanceID and has the agreed-upon ResourceType
2. No item exists with this InstanceID in this Configuration

Now, other than InstanceID and ResourceType, every other Item attribute may
vary widely between configurations, but even this simple constraint makes
our life a lot easier.

Item combining/layering
'''''''''''''''''''''''

The fact that an Item can in essence be declared and subsequently redefined an
arbitrary number of times adds complexity, but we only really need to handle
it in two cases:

1. When initially loading the OVF descriptor XML into COT
2. When writing back out to XML

Ideally we want to not change the XML of Items that COT is not modifying,
but when updating an Item, COT can and should be free to configure the
XML of that Item however it wishes so long as it's still a valid OVF.

We can probably manage this by tracking modifications by InstanceID - an
InstanceID that is untouched should remain unchanged by COT, while modifying
any part of any Item for a given InstanceID gives COT permission to regenerate
its XML.

The OVFHardware/OVFItem implementation
--------------------------------------

The existing implementation, with classes OVFHardware and OVFItem, was built
around the idea that Items will typically only vary slightly between config
profiles.

The OVFHardware class is essentially a dict mapping InstanceID to OVFItem;
hence, at most one OVFItem exists for any given InstanceID.

An OVFItem instance represents all Item variants for given InstanceID across
all configurations. It is structured as a dict of dict of sets; in essence
OVFItem[property-name][value] = set([profile1, profile2])

Pros
''''

- Relatively straightforward to associate/dissociate an Item from a given
  configuration profile (iterate over all properties in the Item, add/remove
  the given configuration to the set of profiles for each property).
- Easy to get a view of how or if a given Item (InstanceID) differs among
  profiles.
- Easy to set/update a given property across all profiles simultaneously.
- Relatively easy to export a fairly minimal set of Item XML elements after
  modifying an OVFItem.

Cons
''''

- Changing property values for an individual profile(s) involves some complex
  logic and validation checks.
- Getting values for a given property involves different code flow and
  assumptions depending on whether one is trying to get "all values across
  profiles", "single value, identical across all profiles", or "single value
  for single profile", but the current OVFItem API doesn't always make
  this obvious.

New Design
----------

Whereas the existing design is structured as::

    OVF.hardware = OVFHardware
    OVFHardware[InstanceID] = OVFItem
    OVFItem[property][value] = set(profiles)

the new proposed design is::

    OVF.configurations = OVFConfigManager
    OVFConfigManager[config] = OVFConfiguration
    OVFConfiguration[InstanceID] = OVFHardwareItem
    OVFHardwareItem[property] = value

Pros
''''

- Much easier to get an overview of a configuration profile as a whole
- Easier to edit properties of an individual existing configuration

Cons
''''

- Adding an entirely new configuration is more difficult
- More work needed when updating a property across multiple profiles
- More work needed when creating a new Item across multiple profiles
- Need to refactor code that looks up a single Item across multiple
  profiles
- More memory intensive when dealing with lots of profiles (?)

.. _`OVF standard`: https://www.dmtf.org/sites/default/files/standards/documents/DSP0243_2.1.1.pdf
