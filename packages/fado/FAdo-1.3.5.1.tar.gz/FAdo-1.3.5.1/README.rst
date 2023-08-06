=============
What is FAdo?
=============

The **FAdo** system aims to provide an open source extensible high-performance software library for the symbolic
manipulation of automata and other models of computation.

To allow high-level programming with complex data structures, easy prototyping of algorithms, and portability
(to use in computer grid systems for example), are its main features. Our main motivation is the theoretical
and experimental research, but we have also in mind the construction of a pedagogical tool for teaching automata
theory and formal languages.

-----------------
Regular Languages
-----------------

It currently includes most standard operations for the manipulation of regular languages. Regular languages can
be represented by regular expressions (regexp) or finite automata, among other formalisms. Finite automata may
be deterministic (DFA), non-deterministic (NFA) or generalized (GFA). In **FAdo** these representations are implemented
as Python classes.

Elementary regular languages operations as union, intersection, concatenation, complementation and reverse are
implemented for each class. Also several combined operations are available for specific models.

Several conversions between these representations are implemented:

* NFA -> DFA: subset construction

* NFA -> RE: recursive method

* GFA -> RE: state elimination, with possible choice of state orderings

* RE -> NFA: Thompson method, Glushkov method, follow, Brzozowski, and partial derivatives.

* For DFAs several minimization algorithms are available: Moore, Hopcroft, and some incremental algorithms. Brzozowski minimization is available for NFAs.

* An algorithm for hyper-minimization of DFAs

* Language equivalence of two DFAs can be determined by reducing their correspondent minimal DFA to a canonical form, or by the Hopcroft and Karp algorithm.

* Enumeration of the first words of a language or all words of a given length (Cross Section)

* Some support for the transition semigroups of DFAs

----------------
Finite Languages
----------------

Special methods for finite languages are available:

* Construction of a ADFA (acyclic finite automata) from a set of words

* Minimization of ADFAs

* Several methods for ADFAs random generation

* Methods for deterministic cover finite automata (DCFA)

-----------
Transducers
-----------

Several methods for transducers in standard form (SFT) are available:

* Rational operations: union, inverse, reversal, composition, concatenation, star

* Test if a transducer is functional

* Input intersection and Output intersection operations

-----
Codes
-----

A *language property* is a set of languages. Given a property specified by a transducer, several language tests are possible.

* Satisfaction i.e. if a language satisfies the property

* Maximality i.e. the language satisfies the property and is maximal

* Properties implemented by transducers include: input preserving, input altering, trajectories, and fixed properties

* Computation of the edit distance of a regular language, using input altering transducers




Versions
========

1.3.5.1
=======

  * fa: NFA.HKequivalence() added Hopcroft & Karp linear equivalence
    test added

  * fa: type of operands of NFA intersection fixed

  * reex: counting snfs


1.3.5 (Giessen)
=====
  * Myhill-Nerode relation computed for DFAs (DFA.MyhillNerodePartition())

1.3.4.1
=======
  * fixed bug in the random generator seed initialisation (thanks to Héctor L Palacios V <hectorpal@gmail.com>)

1.3.4
=====
  * rndfa & rndfap Generators now accept a seed for the random generation

1.3.3
=====
  * fa.DFA.regexp bug fixed
  
  * Watson-Daciuk's ADFA incremental minimisation
  
  * DFA reversability test implemented
  
  * DFA intersection made faster
  
  * FA state deletion made faster
  
  * FA product construction made faster
  
  * makeCode made faster

1.3.2.1
=======
  * Some bugs solved (thanks to David Purser to spot them)

1.3.1
=====
   * fa.DFA.succintTransitions and fa.NFA.succintTransitions corrected

1.3
===
   * Methods added to construct error detecting languages

1.2.1
=====
   * Random generator for ADFAs (rndadfa.py)

   * Implementation of Asperti, Coen and Tassi "au-point" conversion
     of regexp to DFA regexp.dfaAuPoint()

   * Implementation of Yamada, McNaughton and Glushkov conversion to
     DFA regexp.dfaYMG()

   * JSON format for Automata

   * Ipython suport 
	 

1.2
===
   * Better interface to FL objects

   * enumDFA() and enumNFA() added to enumerate languages

   * CodePprop is now UDCodeProp

   * IPTProp removed

   * Strict concatenation implemented (DFA.sop() for now!)

   * binary operations with NFAs now deal correctly with epsilon-NFAs

   * uniform random word generator for finite languages
	 
   * Codes hierarchy implemented
	 
   * Words are now objects (defined in commom.py)

1.1.1
=====

   * corrected bug in fa.NFA.elimEpsilon()

   * Resulting NFA from __or__ gets the union of both alphabets as its alphabet

1.1
===
   
   * FL.ADFA.minDFCA() corrected with the addition of ADFA.forceToDCFA()

   * random generation via cfg bug fixed

   * ICDFArndIncomplete bug fixed

   * xre fixed with context for negation

   * fa.DFA.hasTrapStateP() added

   * ICDFA random generator flag bug fixed

   * ICDFA random generators now written in python

   * New display methods to be usable inside IPython notebooks

   * Problems in Linux instalation

   * SFT.evalWordP() was returning the negation of what it should.

1.0 (Halifax)
-------------

    * addState() does not create states with clashing names (int/str)
      anymore.

    * New property builders having transducers as strings instead of
      stored in files.

    * yappy_parser permanent tables recover from reading problems, and
      quit shelf usage as last resort solution. Now it should work in
      all OS and in every possible conditions, even in a Apache
      execution environment 

    * Intersection of properties corrected for input altering transducers

    * Normal Form Transducers

    * Conjunction of input properties described by input altering and
      input preserving transducers fixed 

    * Infix Property added

    * Error corrected with the import of new yappy_parser

    * Now display() works in MSwindows, with ''start'' instead of ''open''

0.9.8
=====

    * Cover automata
      
    * New fio module that deals with i/o

    * Two-way automata starting to be supported

    * Distinguishability of a language

    * New xre (extended Regular Expressions) module

0.9.7
=====

    * stupid error in DFA.__repr__() fixed

    * better dealing of incomplete automata

    * new DFA and NFA file format

    * better integration with GRAIL+

0.9.6
=====

    * some random bugs corrected in combo and single operations
      
0.9.5
=====

    * star and concatenation for DFAs aiming minimal transition
      complexity
      
    * new API documentation

    * better regular expression random generation
      
0.9.4
=====

    * A primitive (but working) uninstall. 

    * New setup for generator (bug fixed)

    * Shufle was migrated to fa.py	

    * Shuffle for NFAs

    * comboperations: shuffle corrected

    * fa: dump added to NFA and DFA
      
0.9.3
=====

    * Prefix-free and prefix-closed finite languages random trie added

    * Renaming of AcyclicP to acyclicP. Loops are now excluded from
      the test unless a strict flag is passed as an argument.

    * trimP corrected accordingly

    * Version in package now reflects the proper version and not the
      major one 

    * Corrections and simplifications added to ADFA.minimal()

    * Random balanced and "unbalanced" trie generation

    * Solved a bug with a mutual inclusions between fa and fl.

    * DFAtoADFA now resides in fl.

    * sigmaInititialSegment() added to fl

    * fa: product of dfas now ensures that its argument is a dfa.

0.9.2
=====

    * Grammar tables for grail, reex and FAdo now start with a "."

    * fl.py (Finite Languages) added to the project: AFA, ADFA and
      ANFA supported

    * Grail+ interface inproved. Now, only if the command hasmore than
      one argument a temporary file is created.

    * Uniform random generation of trie automata with (at least) a
      word of a maximum lenght added (fl.py)

    * rndfa.py added: a wrap for the ICDFA random Generator.

    * Errors corrected in minimazation methods.

    * readFromFile now supports comments as documented.

    * saveToFile deals correctly with append flag.

    * Bugs on deleteState() were corrected. 
