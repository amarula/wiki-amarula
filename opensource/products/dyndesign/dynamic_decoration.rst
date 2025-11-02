Dynamic Decoration of Methods in Python
#######################################

.. figure:: /images/dyndesign-dynamic_decoration-intro.png
   :alt: Original image created with DALL·E

   Original image created with DALL·E

Decorators are an extraordinary tool to modify or enhance the behavior
of functions and methods without having to modify their source code
directly.

Nevertheless, the main constraint of decorators is that they need to be
defined statically within the same scope where they are applied,
otherwise a “NameError” or “AttributeError” exception is raised. For
example, a method of a parent class cannot be directly utilized as a
decorator for a child class, just as a method of a component class
cannot be employed to decorate the methods of the class that uses that
component.

Motivation
**********

The primary motivation behind deciding to support Dynamic Decoration was
to facilitate method decoration across classes that are merged with
``mergeclasses`` , which is a key aspect of the DynDesign project
discussed in detail in the previous article of this series.

At a later time, I realized can the Dynamic Decorators have applications
beyond the merged classes, allowing developers to use as decorators -
methods from **ancestor classes**

::

   class Parent:
       def method_from_parent:
           ...

   class Child(Parent):
       @method_from_parent
       #^^^^^^^^^^^^^^^^^^ NameError: name 'method_from_parent' is not defined
       @decoratewith("method_from_parent")
       # Works!!
       def decorated_method(...):
           ...

-  methods from **component classes**

::

   class Component:
       def method_from_component:
           ...

   class Composite:
       def __init__(self):
           self.component = Component()

       @component.method_from_component
       #^^^^^^^^^ NameError: name 'component' is not defined
       @decoratewith("component.method_from_component")
       # Works!!
       def decorated_method(...):
           ...

-  functions **built at runtime**

::

   class RuntimeDecorated:
       @decoratewith("runtime_built")
       def decorated_method(...):
           ...

   runtime_decorated = RuntimeDecorated()
   runtime_decorated.runtime_built = build_decorator()

More information about the above use cases can be found here.

Dynamic Decorators in action
****************************

The current article picks up where the previous one left off, which
involved the utilization of a Python script to show the behavior of
Collatz functions. The script has a number of optional arguments, and is
implemented by associating to each option an optional class, which is
merged depending on whether the corresponding option is set or not (the
complete code for the examples presented in the articles of this series
is available here).

::

   #collatz_output_graph.py

   import argparse
   from dyndesign import mergeclasses
   import matplotlib.pyplot as plt

   class CollatzGraph:
       def __init__(self):
           self.sequence = []

       def output_number(self, n):
           self.sequence.append(n)

       def output_graph(self):
           plt.plot(self.sequence)
           plt.xlabel("Step")
           plt.ylabel("Value")
           plt.title(f"{self.FUNCTION_NAME} Function")
           plt.show()
   ...

   class CollatzOutput:
       def output_number(self, n):
           print(f"{n}; ", end='')

       def output_sequence(self):
           print(f"{self.FUNCTION_NAME} sequence starting from {self.n} is:")
           self.output_number(self.n)
           for n in self.get_collatz_sequence(self.n):
               self.output_number(n)
           print()


   if __name__ == "__main__":
       parser = argparse.ArgumentParser(description='Calculate Collatz sequence.')
       parser.add_argument('n', help='an integer to calculate the Collatz sequence')
       parser.add_argument('-c', action='store_true', dest='custom_collatz')
       parser.add_argument('-g', action='store_true', dest='collatz_graph')
       args = parser.parse_args()

       CollatzMerged = mergeclasses(CollatzSequence, CollatzOutput)
       if args.custom_collatz:
           CollatzMerged = mergeclasses(CollatzMerged, CollatzCustom)
       if args.collatz_graph:
           CollatzMerged = mergeclasses(
               CollatzMerged,
               CollatzGraph,
               invoke_all=['output_number']
           )

       collatz = CollatzMerged(args.n)
       collatz.output_sequence()
       if args.collatz_graph:
           collatz.output_graph()

The first problem that I want to address is the code duplication of
statement ``if args.collatz_graph`` at the bottom of the script, to call
“output_graph” in case option “-g” is selected: that statement also
appears 4 lines above, in clear violation of the **DRY** principle.

To avoid this repetition, the ``**decoratewith**`` meta decorator
provided by DynDesign package can be used to **dynamically decorate the
method** “output_sequence” by passing “output_graph” as decorator name,
instead of calling method “output_graph” at the end of the script, so
that the script code becomes

::

   #collatz_graph_decorator.py

   from dyndesign import mergeclasses, decoratewith
   ...

   class CollatzGraph:
       def output_number(self, n):
           self.sequence.append(n)

       def output_graph(self, func):
           self.sequence = []
           func(self)
           plt.plot(self.sequence)
           ...

   class CollatzOutput:
       ...

       @decoratewith("output_graph")
       def output_sequence(self):
           ...

   ...
   collatz = CollatzMerged(args.n)
   collatz.output_sequence()

where method “output_graph” is converted into a decorator by adding
argument “func” after “self” and by including the ``func(self)`` call in
decorator’s body. Also, constructor ``__init__`` of “CollatzGraph” can
now be removed as “self.sequence” is initialized in “output_graph” just
before calling “func”.

This highlights another advantage of ``decoratewith`` : the syntax of
the dynamic decorators is simpler if compared to the syntax of built-in
decorators in Python, which involves defining wrapper functions:

::

   def builtin_decorator(func):
       def wrapper():
           ...
           func()
           ...
       return wrapper

As expected, the code presented in this section is a refactored version
that yields identical results to its previous implementation:

::

   $ python collatz_decorators.py -g 79
   Collatz sequence starting from 79 is:
   79; 238; 119; 358; 179; 538; 269; 808; 404; 202; 101; 304; 152; 76; 38; 19;
   58; 29; 88; 44; 22; 11; 34; 17; 52; 26; 13; 40; 20; 10; 5; 16; 8; 4; 2; 1;

.. figure:: /images/dyndesign-dynamic_decoration-graph.png

Multiple Decorators
*******************

Multiple decorator names can be passed to ``decoratewith`` , allowing
for the corresponding decorator methods to be\ **applied in nested
chain** , as documented here.

In order to test this feature, I demonstrate an example below by adding
a new ‘-s’ option to the script, which prints out relevant statistics
about the Collatz sequences. For this purpose, a new class called
‘CollatzStatistics’ can be defined and optionally merged with the
existing classes:

::

   class CollatzStatistics:
       def output_number(self, n):
           self.max = max(self.max, n)
           self.count += 1

       def output_stats(self, func):
           self.max = 0
           self.count = 0
           func(self)
           print(f"Max value reached: {self.max}")
           print(f"Sequence length: {self.count}")

The decorator name “output_stats” can then be passed to ``decoratewith``
after “output_graph”, resulting in the nested execution of the two
decorators:

::

   @decoratewith("output_graph", "output_stats")
   def output_sequence(self):
       ...

Finally, the class can be merged to “CollatzMerged”:

::

   ...
   parser.add_argument('-s', action='store_true', dest='collatz_statistics')

   ...
   if args.collatz_statistics:
       CollatzMerged = mergeclasses(
           CollatzMerged,
           CollatzStatistics,
           invoke_all=['output_number']
       )

where the overloading of “output_number” instances in other merged
classes is prevented by passing the decorator name again in the
``invoke_all`` list, just like when merging “CollatzGraph”.

*NOTE: It could be argued that the method’s name “output_number” does
not align well with the function of updating the statistics, and the
method’s functionality in all the classes where it is implemented may be
better described by a more generic name such as “process_number”.
Anyway, to maintain clarity across different versions of the script, I
opted to retain the original name.*

The code above gives the expected results with any combination of
options:

::

   $ python collatz_statistics.py -s 79
   Collatz sequence starting from 79 is:
   79; 238; 119; 358; 179; 538; 269; 808; 404; 202; 101; 304; 152; 76; 38; 19;
   58; 29; 88; 44; 22; 11; 34; 17; 52; 26; 13; 40; 20; 10; 5; 16; 8; 4; 2; 1;
   Max value reached: 808
   Sequence length: 36

   $ python collatz_statistics.py -sg 79
   Collatz sequence starting from 79 is:
   79; 238; 119; 358; 179; 538; 269; 808; 404; 202; 101; 304; 152; 76; 38; 19;
   58; 29; 88; 44; 22; 11; 34; 17; 52; 26; 13; 40; 20; 10; 5; 16; 8; 4; 2; 1;
   Max value reached: 808
   Sequence length: 36
   # Graph "Collatz Function" is correctly displayed

   $ python collatz_statistics.py -sc 79
   Collatz-like ternary sequence starting from 79 is:
   79; 159; 53; 157; 315; 105; 35; 103; 207; 69; 23; 67; 135; 45; 15; 5; 13;
   27; 9; 3; 1;
   Max value reached: 315
   Sequence length: 21

   ...

Multiple Instances of Decorators
********************************

In case of multiple decorators for a single decorated method, developers
can usually choose from two alternative implementation options, both of
which are fully supported by ``decoratewith`` : - keeping distinct names
for multiple decorators and pass them all as ``decoratewith`` arguments,
like in the example above, or - using one generic decorator name for
multiple decorator instances and passing that name in the ``invoke_all``
list of ``mergeclasses`` , so that all the instances of the decorator in
the merged classes are invoked.

The code above uses option #1, but it can be modified to use option #2
as follows (the complete code is available here): - Decorators
“output_graph” and “output_stats” are renamed to “output_wrapper”, -
``@decoratewith("output_graph", "output_stats")`` is
then simplified to\ ``@decoratewith("output_wrapper")`` , and
- decorator name “output_wrapper” is appended in turn to the
``invoke_all`` list in the last ``mergeclasses`` call, which is thus
changed to

::

   CollatzMerged = mergeclasses(
       CollatzMerged,
       CollatzStatistics,
       invoke_all=['output_number', 'output_wrapper']
   )

Multiple Decorators vs Multiple Decorator Instances
***************************************************

Both choices have no significant impact on the overall performance, but
they do have design implications with advantages and disadvantages: -
**keeping distinct names can improve code readability** , since you can
give a meaningful name to each decorator, instead of relying on generic
names, such as “*_wrapper”; on the other hand - **using a single name**
for multiple decorator instances is one step forward in terms of
**adhering to the Open-Closed Principle** , as it allows for easier
extension to other merging classes in the future without the need to
pass new decorator names as ``decoratewith`` arguments.

Ultimately, the choice between using distinct names or a single generic
name for decorators should depend on the specific context and
requirements of the project. I will proceed with option #2 in the next
article, where I will provide practical examples of the mentioned
advantage.

Conclusion
**********

The ``decoratewith`` meta decorator from DynDesign package offers an
easy-to-use solution for Dynamic Decoration, allowing developers to use
**decorators from ancestor, component** or\ **merged classes** , and
even to **create decorators at runtime** . Overall, Dynamic Decoration
is a valuable technique to add to a developer's toolbox, enabling more
modular and extensible software design.

Written by Patrizio Gelosi
--------------------------
