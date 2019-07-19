Git Bisect Tutorial
###################

When we we are not sure which commit in our git repository broke something, we need some tool to find that bad/buggy commit.
This situation becomes complex when there are large number of commits and we have no clue. In this situation git bisect is our saviour.
Suppose we found bug in u-boot v2017.07 version and we know that v2017.05 version is working fine. But the number of commits
between v2017.07 version and v2017.05 version are huge. In this situation checking each of the commits would take enormous time and
it wouldn't a wise thing to do.

In such scenarios git bisect plays a very vital role and saves our efforts and time in finding buggy or bad commit.
We will see how to find buggy commit using git bisect. Lets starts!
To start, we would need git commit ids of v2017.07(say 2f4c1d83f4e8) and v2017.05 (say a63d800196eb)

Steps:

step1: In our git repository we run,

::

   git bisect start

   git bisect good a63d800196eb

   git bisect bad  2f4c1d83f4e8

.. image:: /images/step1.png

Git bisect looked at all of the commits between a63d800196eb  and 2f4c1d83f4e8, picked the middle one i.e be62fbf37626, and switched the current checkout to that instead.
Now, we need to check  whether commit be62fbf37626  is buggy/bad or not. We build at this commit and check whether it has that bug or not.

step2: Build repo at checkout commit in our case it is be62fbf37626

step3: Run  either git bisect bad  or git bisect good based on above build.

If commit id is buggy(say it is) then we run git bisect bad  else we would run git bisect good

.. image:: /images/step.png
Step4 .... N: keep repeating above step 2 and step3

.. image:: /images/step3.png

.. image:: /images/4.png

Now that we are commit aab203eb2e0d, we build repo at this commit and check again whether this repos is buggy or not.
Lets say it is not buggy, then execute git bisect good  and after this will the first first bad commit , i.e, the first time when the bug was introduced in the repo.

.. image:: /images/5.png   

Now we know that  d1e204b56681 is buggy commit. We can check changes this commit introduced that caused bug.

After a bisect session, to clean up the bisection state and return to the original HEAD (i.e., to quit bisecting), issue the
following command:

::

   $ git bisect reset

Thats all!!
