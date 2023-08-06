y!
==

**Pronounced as "why not?"**

Why not?
========

That's the way ***y!*** is pronounced.

And that's the question I asked myself when I had the the idea to
implement a programming language completely different from the ones I
know so far:

***y***\ *aml-based* ***no***\ *-XML* ***t***\ *ransformation*

***y!*** is the answer to the question ***"why not?"***
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So what does ***y!*** focus on?

-  ***y!*** is an incredibly simple programming language for processing
   structured data (``json``, ``yaml``, ...).

   Therfore it is also perfectly suited for processing output from
   various NOSQL databases! And with little effort even from relational
   databases.

-  ***y!*** focuses on quickly and easily producing output.

   This output can be:

   -  Text
   -  Structured data

-  ***y!*** supports self-verification of programs by simply providing
   samples for input and output.

   No need for using test-frameworks, writing unit-tests or any other
   hassle.

-  ***y!*** supports producing well-formatted documentation without any
   tools-magic.

   It doesn't require any more than a command-line flag.

It works similar to xslt but is significantly simpler and therefore
providing much better readability and writability.

Quick Start
===========

Unfortunately tradition forces me to start with a *hello world*
application:

Hello World
^^^^^^^^^^^

``$ cat hello_world.ynot``

.. code:: yaml

    actions:
    - print: Hello World

::

    $ ynot -t hello_world.ynot
    Hello World

| Not very interesting, right?
| Not useful at all, right?

But quite simple, right?

Process input data
^^^^^^^^^^^^^^^^^^

Now let's do something a bit more useful. Let's process data - that's
what ***y!*** is made for:

Let's say we have an input that represents multiple text documents with
sections and chapters:

``$ cat sample01.yaml``

.. code:: yaml

    - title: Some document title
      sections:
      - title: Some section title
        chapters:
        - title: Some chapter title
          text: |
            Some long text
            with lots of paragraphs
        - title: Some other chapter title
          text: |
            Some long text
            with lots of paragraphs
      - title: Some other section title
        chapters:
          - title: Some chapter title for some other section
          text: |
            Some long text
            with lots of paragraphs
    - title: Some other document title

Now we want to print all the titles and nothing else.

So for the given input file we expect the following output:

::

    Some document title
    Some section title
    Some chapter title
    Some other chapter title
    Some other section title
    Some chapter title for some other section
    Some other document title

The program for achieving that looks as simple as this:

``$ cat sample01.ynot``

.. code:: yaml

    actions:
      - for:
          path: '..title'
          actions:
            - print: '@y!{.@}'

Let's try it:

::

    $ ynot -t sample01.ynot sample01.yaml
    Some document title
    Some section title
    Some chapter title
    Some other chapter title
    Some other section title
    Some chapter title for some other section
    Some other document title

Looks good so far.

But while developing and testing the program we don't always want to
manually check if the output is correct, do we?

With verification
'''''''''''''''''

| ***y!*** has a very simple and straightforward solution.
| You can add samples to the program:

``$ cat sample01.ynot``

.. code:: yaml

    actions:
      - for:
          path: '..title'
          actions:
            - print: '@y!{.@}'

    samples:
      sample1:

        input:
          - title: Some document title
            sections:
            - title: Some section title
              chapters:
              - title: Some chapter title
                text: |
                  Some long text
                  with lots of paragraphs
              - title: Some other chapter title
                text: |
                  Some long text
                  with lots of paragraphs
            - title: Some other section title
              chapters:
                - title: Some chapter title for some other section
                  text: |
                    Some long text
                    with lots of paragraphs
          - title: Some other document title

        output: |
          Some document title
          Some section title
          Some chapter title
          Some other chapter title
          Some other section title
          Some chapter title for some other section
          Some other document title

... and simply verify the program against expected output for given
input by cust invoking it without input files or with the ``--dry-run``
option:

``$ ynot -t sample01.ynot --dry-run``

*Oh! No output!*

| That's intended. When everything is right it doesn't output anything.
| Let's prove that in case of problems they are reported.

With failing verification
'''''''''''''''''''''''''

So we change the program slightly by prepending \_title: \_ to the
actual title:

``$ cat sample01.ynot``

.. code:: yaml

    actions:
      - for:
          path: '..title'
          actions:
            - print: 'title: @y!{.@}'

    samples:
      sample1:

        input:
          - title: Some document title
            sections:
            - title: Some section title
              chapters:
              - title: Some chapter title
                text: |
                  Some long text
                  with lots of paragraphs
              - title: Some other chapter title
                text: |
                  Some long text
                  with lots of paragraphs
            - title: Some other section title
              chapters:
                - title: Some chapter title for some other section
                  text: |
                    Some long text
                    with lots of paragraphs
          - title: Some other document title

        output: |
          Some document title
          Some section title
          Some chapter title
          Some other chapter title
          Some other section title
          Some chapter title for some other section
          Some other document title

Now we can see that the actual output doesn't match the expected one:

::

    ynot -t samples/trafos/sample01.yaml --dry-run
    ERROR:ynot.globals:Verifying sample sample1 failed

    Expected:
    Some document title
    Some section title
    Some chapter title
    Some other chapter title
    Some other section title
    Some chapter title for some other section
    Some other document title

    Got:
    title: Some document title
    title: Some section title
    title: Some chapter title
    title: Some other chapter title
    title: Some other section title
    title: Some chapter title for some other section
    title: Some other document title


    ERROR:ynot.globals:Verifying sample sample1 failed for trafo <undefined>

Nice, isn't it?

You can add as many samples as you want - all of them will be processed
and verified.


