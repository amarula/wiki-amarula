How to Merge Classes using the Builder Design Pattern
#####################################################

.. figure:: /images/dyndesign-builder-intro.png
   :alt: Original image created with DALL·E

   Original image created with DALL·E

In earlier articles within this series (Merging Classes: an alternative
path to the SOLIDness and Dynamic Decoration of Methods in Python), I
presented the DynDesign package, as well as several methods for merging
classes in Python and dynamically decorating methods with decorators
that are loaded or created at runtime.

Motivation
**********

After implementing in real-world scenarios the class merging techniques
presented in the previous articles, I discovered areas for improvement
in terms of adherence to the Single Responsibility Principle (SRP) and
the Open-Closed Principle (OCP) of the SOLID principles: - The code
implementing the **class merging** can be **encapsulated into a class**
(specifically, a Class-Builder class), in order to adhere more closely
to the SRP. - Additional options can be incorporated into the script and
the corresponding optional classes can be **merged without the need to
modify the class builder** , so as to fulfill the OCP.

Eliminating multiple calls to mergeclasses
******************************************

Below is an excerpt from the latest version of the script for studying
Collatz sequences (the complete code for all the examples of this
article can be found here):

::

   #collatz_statistics_deco_overloaded.py

   import argparse
   from dyndesign import mergeclasses, decoratewith
   import matplotlib.pyplot as plt

   class CollatzGraph:
       ...

   class CollatzStatistics:
       ...

   class CollatzSequence:
       ...

   class CollatzCustom:
       ...

   class CollatzOutput:
       ...


   if __name__ == "__main__":
       parser = argparse.ArgumentParser(description='Calculate Collatz sequence.')
       parser.add_argument('n', help='an integer to calculate the Collatz sequence')
       parser.add_argument('-c', action='store_true', dest='custom_collatz',
                           help='use custom Collatz instead')
       parser.add_argument('-g', action='store_true', dest='collatz_graph')
       parser.add_argument('-s', action='store_true', dest='collatz_statistics')
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
       if args.collatz_statistics:
           CollatzMerged = mergeclasses(
               CollatzMerged,
               CollatzStatistics,
               invoke_all=['output_number', 'output_wrapper']
           )

       collatz = CollatzMerged(args.n)
       collatz.output_sequence()

Firstly, I want to ensure that ``**mergeclasses**`` **is called only
once** in order to follow the DRY principle and to optimize performance.

This change can be implemented because in this example the
``invoke_all`` arguments passed in the last call (“[‘output_number’,
‘output_wrapper’]”) can be extended to all previous ``mergeclasses``
calls without impacting the results. To implement this change, the
classes to merge are collected in a list and then merged together in a
single call to ``mergeclasses`` :

::

   #collatz_mergeclasses_list.py

   ...
   classes_to_merge = [CollatzSequence, CollatzOutput]
   if args.custom_collatz:
       classes_to_merge.append(CollatzCustom)
   if args.collatz_graph:
       classes_to_merge.append(CollatzGraph)
   if args.collatz_statistics:
       classes_to_merge.append(CollatzStatistics)
   CollatzMerged = mergeclasses(
       *classes_to_merge,
       invoke_all=['output_number', 'output_wrapper']
   )

   collatz = CollatzMerged(args)
   collatz.output_sequence()

It worth noting that, in this version of the script, the complete “arg”
object is passed to initialize the “CollatzMerged” class instead of just
“args.n”, in order to provide greater flexibility for future
implementations.

Testing the new version results in:

::

   $ python collatz_mergeclasses_list.py -cgs 187
   Collatz-like ternary sequence starting from 187 is:
   187; 375; 125; 373; 747; 249; 83; 247; 495; 165; 55; 111; 37; 75; 25; 51;
   17; 49; 99; 33; 11; 31; 63; 21; 7; 15; 5; 13; 27; 9; 3; 1;
   Max value reached: 747
   Sequence length: 32

.. figure:: /images/dyndesign-builder-graph.png

Dynamically importing the optional classes
******************************************

If the scope of the SRP is broaden to include modules as well as
classes, the next logical step becomes evident: **moving each class to
a** **separate module** and **dynamically importing it** **only if the
corresponding options is set** . This approach has also a positive
impact on performance, particularly when dealing with a large number of
optional classes that need to be imported.

Conveniently, ``mergeclasses`` can also accept path strings as
arguments, where the path string are path to the classes in dot
notation. Therefore, each class from the single-file script
“collatz_mergeclasses_list.py” can be moved to a corresponding module
with the class name in snake case and located in a directory named
“components”. As a result, the script is refactored into
“collatz_dynamically_imported.py” + multiple modules, each of which
containing a single class, so that the directory structure looks like:

::

   ...
   collatz_dynamically_imported.py
   components/
       collatz_custom.py
       collatz_graph.py
       collatz_sequence.py
       ...

and the script is shortened to the following:

::

   #collatz_dynamically_imported.py

   import argparse
   from dyndesign import mergeclasses

   if __name__ == "__main__":
       parser = argparse.ArgumentParser(description='Calculate Collatz sequence.')
       parser.add_argument('n', help='an integer to calculate the Collatz sequence')
       parser.add_argument('-c', action='store_true', dest='custom_collatz', 
                           help='use custom Collatz instead')
       parser.add_argument('-g', action='store_true', dest='collatz_graph')
       parser.add_argument('-s', action='store_true', dest='collatz_statistics')
       args = parser.parse_args()

       classes_to_merge = [
           "components.collatz_sequence.CollatzSequence",
           "components.collatz_output.CollatzOutput"
       ]
       if args.custom_collatz:
           classes_to_merge.append("components.collatz_custom.CollatzCustom")
       if args.collatz_graph:
           classes_to_merge.append("components.collatz_graph.CollatzGraph")
       if args.collatz_statistics:
           classes_to_merge.append("components.collatz_statistics.CollatzStatistics")
       CollatzMerged = mergeclasses(
           *classes_to_merge,
           invoke_all=['output_number', 'output_wrapper']
       )

       collatz = CollatzMerged(args)
       collatz.output_sequence()

Employing a Class Builder for Merging Classes
*********************************************

The final steps in achieving SOLID principles involve **automating the
process of merging optional classes** and **organizing** **the related
code within a Class Builder** . By following this approach, the addition
of a new script option typically involves simply placing the
corresponding class in the “components” directory, thereby streamlining
the development process.

To achieve this, the destination properties of the ``argparse`` options
are modified to correspond directly to the class names:

::

   #collatz_building_merged.py

   import argparse
   from collatz_class_builder import CollatzClassBuilder

   if __name__ == "__main__":
       parser = argparse.ArgumentParser(description='Calculate Collatz sequence.')
       parser.add_argument('n', help='an integer to calculate the Collatz sequence')
       parser.add_argument('-c', action='store_true', dest='CollatzCustom')
       parser.add_argument('-g', action='store_true', dest='CollatzGraph')
       parser.add_argument('-s', action='store_true', dest='CollatzStatistics')
       args = parser.parse_args()

       class_builder = CollatzClassBuilder(args)
       CollatzClass = class_builder.build_class()

       collatz = CollatzClass(args)
       collatz.output_sequence()

The Class Builder is implemented as follows:

::

   #collatz_class_builder.py

   from dyndesign import mergeclasses
   import re

   class CollatzClassBuilder:
       COMPONENT_DIR = 'components'

       def __init__(self, args):
           self.args = args

       @staticmethod
       def camel_to_snake(value):
           return re.sub('([a-z0-9])([A-Z])', r'\1_\2', value).lower()

       def build_class(self):
           classes_to_merge = ['CollatzSequence', 'CollatzOutput']
           for opt_class, value in self.args.__dict__.items():
               if opt_class != 'n' and value:
                   classes_to_merge.append(opt_class)
           paths_to_merge = (
               f"{self.COMPONENT_DIR}.{self.camel_to_snake(c)}.{c}"
               for c in classes_to_merge
           )
           return mergeclasses(
               *paths_to_merge,
               invoke_all=['output_number', 'output_wrapper']
           )

The method “build_class” in “CollatzClassBuilder” first adds the names
of the base classes and the classes corresponding to the script options
(i.e., all the valued script arguments except “n”) to the
“classes_to_merge” list. Then, the class names in “classes_to_merge” are
converted into dot-notated class paths by prepending the component
directory and the package name, which is obtained by converting the
class name from camel to snake case. Finally, the class resulting from
merging all the class paths is returned.

Testing the adherence to the OCP
********************************

This section show how to introduce a new option, which would typically
require modifying existing code, just by adding a new 6-line class. The
new option provides the ability to analyze multiple Collatz sequences
starting from the next M consecutive integers after the argument “n”,
where M is an integer passed to the script from the option “-m”.

The challenge is to **introduce this new feature** **without making
changes to the existing code** , except for adding the ``argparse``
setting for the “-m” option. Indeed, the new feature can be implemented
simply by adding the following file to the project:

::

   #components/collatz_multiple.py

   class CollatzMultiple:
       def __init__(self, args):
           self.m = args.CollatzMultiple

       def output_wrapper(self, func):
           for self.n in range(self.n, self.n + self.m + 1):
               func(self)

and the following ``argparse`` setting to the main script:

::

   parser.add_argument('-m', type=int, dest='CollatzMultiple')

The main magic behind this code lies in the dynamic decorator
“output_wrapper”, which, being passed in the ``invoke_all`` argument
list of ``mergeclasses`` , is applied in a nested chain together with
other decorator instances from different classes. The order of chaining
the decorator instances is important as it affects the final result, and
it is ultimately determined by the order of appearance of the
``argparse`` settings. Here are some results obtained if the setting for
option “-m” is positioned before the ones for “-g” and “-s” in the
script’s code:

::

   $ python collatz_building_merged.py -m5 20
   Collatz sequence starting from 20 is:
   20; 10; 5; 16; 8; 4; 2; 1;
   Collatz sequence starting from 21 is:
   21; 64; 32; 16; 8; 4; 2; 1;
   Collatz sequence starting from 22 is:
   22; 11; 34; 17; 52; 26; 13; 40; 20; 10; 5; 16; 8; 4; 2; 1;
   Collatz sequence starting from 23 is:
   23; 70; 35; 106; 53; 160; 80; 40; 20; 10; 5; 16; 8; 4; 2; 1;
   Collatz sequence starting from 24 is:
   24; 12; 6; 3; 10; 5; 16; 8; 4; 2; 1;
   Collatz sequence starting from 25 is:
   25; 76; 38; 19; 58; 29; 88; 44; 22; 11; 34; 17; 52; 26; 13; 40; 20; 10; 5;
   16; 8; 4; 2; 1;

   $ python collatz_building_merged.py -m5 -cs 20
   Collatz-like ternary sequence starting from 20 is:
   20; 58; 117; 39; 13; 27; 9; 3; 1;
   Max value reached: 117
   Sequence length: 9
   Collatz-like ternary sequence starting from 21 is:
   21; 7; 15; 5; 13; 27; 9; 3; 1;
   Max value reached: 27
   Sequence length: 9
   Collatz-like ternary sequence starting from 22 is:
   22; 45; 15; 5; 13; 27; 9; 3; 1;
   Max value reached: 45
   Sequence length: 9
   Collatz-like ternary sequence starting from 23 is:
   23; 67; 135; 45; 15; 5; 13; 27; 9; 3; 1;
   Max value reached: 135
   Sequence length: 11
   Collatz-like ternary sequence starting from 24 is:
   24; 8; 22; 45; 15; 5; 13; 27; 9; 3; 1;
   Max value reached: 45
   Sequence length: 11
   Collatz-like ternary sequence starting from 25 is:
   25; 51; 17; 49; 99; 33; 11; 31; 63; 21; 7; 15; 5; 13; 27; 9; 3; 1;
   Max value reached: 99
   Sequence length: 18

The script gives the expected results with any combination of options:
if option “-g” is also set, then a graph is displayed after printing
each sequence.

Final Thoughts
**************

In this series of articles, I presented powerful techniques provided by
package DynDesign for creating flexible and modular Python code that
adheres to the SOLID and other principles. The initial idea of Merging
Classes to provide developers with an easy-to-use developer tool has
been implemented and enriched with additional tools to improve its
usage, such as Dynamic Decoration and Dynamic Import from a Class
Builder.

The outcome is an approach that complements established Design Patterns
and enables the writing of code that aligns with widely employed design
principles, such as the **SRP** and the **OCP** , and best practices.

Feel free to dive in and give DynDesign a shot, unlocking the boundless
potential of Dynamic Design in your projects. Embrace this innovative
approach and experience the transformative power it brings to your code
organization.

Written by Patrizio Gelosi
--------------------------
