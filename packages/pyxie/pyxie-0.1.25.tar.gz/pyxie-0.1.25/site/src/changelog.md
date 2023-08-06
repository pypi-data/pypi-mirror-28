---
template: mainpage
source_form: markdown
name: Changelog
title: Changelog
updated: February 2018
---
## Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/), within
reason. (Prior to a 1.0.0 release minor version increases may be backwards
incompatible) See doc/Versioning.md for more details

## [0.1.25] - 2018-02-03

The focus of this release is the result of the independent intermediate
node refactoring project I was undertaking. This was to transform the list
oriented data structure for representing a "pure" intermediate form of
code into a more stuctured/generalisable format.

The motivation behind this change was the realisation that implementation
of end user functions (ie `def`) would be very difficult with this more
structured approach. 

### New

* `doc/Versioning.md` - semantic versioning as it applies to pyxie
* `doc/WIPNOTES/6.Models.md` - start of some docs around the models in use
* Added explicit notes on licensing of pyxie's output.
  (Short version: I view the output as being derived from your code by you)
* Language focussed examples / acceptance tests added:
  `if` `if-else` `pass` `print`  `while-break` `while-continue`
* Change `arduino` profile to support the `Adafruit_NeoPixel` library
* `neopixel` example added

### What's been fixed? / Improved

* Handling if if/elif/else improved/fixed
* added `clean.sh` to `arduino` example
* added `clean.sh` to `servo` example
* added `README.md` to `simplest_function` example (won't work yet)

### Internal Changes

* `bin/pyxie` now pulls in functionality from `pyxie.api` to be clearer
   about what the API is
* added `pyxie/api.py` - public API for embedding pyxie. (Assumes
  ubuntu host) Core contents:
    * `initialise_API(profile="default")` - Call first
    * `set_profile(profile_name)` - Call later
    * `PyxieAPI.parse(filename)` - parse file, output goes to console
    * `PyxieAPI.analyse(filename)` - parse & analyse flle, output to console
    * `PyxieAPI.codegen(filename, result_filename=None)` - parse through
       code generation. Output to console
    * `PyxieAPI.compile(filename, result_filename=None)` - Compile file,
       result ends up as "result_filename"
* `pyxie/core` - changed over to drive the conversion of pynodes to
   cppnodes via iinodes. (aim is to simplify pynodes down the line and
   make iinodes our main location for analysis/etc)
* Minor changes to `.gitignore`
* Minor change to the `Makefile` to make editting simpler for me...
* Update `clib.py` based on changes to `clib`
* `pyxie/codegen/simple_cpp.py` - functionality shifted out to
  `pyxie/models/cppnodes.py` to allow a model driven approach
* `pyxie/model/cppnodes.py` Created. A better code representation
   model for C++. Code generation therefore means transforming from the
   `iiNode`s to `CppNode`s 
* `pyxie/model/iinodes.py` - Introduces `iiNode`s - which are used to
  represent an intermediate version of a program such that it can bridge
  the conversion between languages
* `pyxie/model/pynodes/operators.py` - added `args()` method to a number
   of classes to unify behaviours
* `pyxie/model/transform.py` - Major change - converts `PyNode`s to
  `iiNode` representation rather than json objects.

### Other

* `doc/newsletter/07-20161110.Pyxie-Release-0.1.24.md` corrected release date
* `doc/newsletter/XX-TBD.Pyxie-2017-Goals.md` - Unreleased newsletter.
  Interesting notes, will get reused if appropriate later. Rather moot
  contents now though.
* `doc/newsletter/08-TBD.Focus-Or-Pyxie-Release-X.X.XX.md` Template for
   next newsletter


## [0.1.24] - 2016-11-10

### What's been fixed?

* Code generation for `else`/`elif` was failing when the statements inside
  contained identifiers. This was due to context not propogating into
  `else`/`elif`. This was caused by neither `if` nor `elif` adding else clauses
  as children. This was done and now this operates correctly.

### New

* Added playful puppy example that compiles and controls the Dagu Playful Puppy
  robot. (8 leg servos, 2 head/neck servos, infrared array sensor/eye)
  * v0 no funcs Playful Puppy code analyses #213
  * v0 no funcs Playful Puppy code generates code #214
  * v0 no funcs Playful Puppy code compiles, & runs on device correctly #215

* Profile specific code has been extracted to a specific file. In this
  case, the iniitial profile made more managable is of course the arduino
  profile. To configure this/extend this, you now update the file
  `pyxie/profile/arduino.py`

* To add more predefined variables/etc that are used in the context (ala
  A0, etc) you extend the function `populate_profile_context`.

* If you need to add extra types - ala the `Servo` type - you can use
  the `Servo` function call as an example. Note that it has a return
  type of `Servo`. This means of course that the `Servo` function is
  a constructor. For this to work   clearly the type needs to be
  defined - so you define it below in the variable `types`.

* Started on _parsing_ side aspects of definition of simple user functions.
  (ie `def` statements) Hopefully basic functions should be in the next
  iteration of pyxie.

### Internal Changes

* `pyxie-dev` - Pyxie's release management tool, has had an overhaul,
  and transferred into the pyxie package, rather than standalone code.
  In the process code was improved, such that "dryrun" and "verbose"
  now mean precisely that. Help text is deliberately verbose to note
  what the release process is.

* Check all Pynodes add all sub nodes as children correctly #264

* Start of function support:
  * Lexing for function definition succeeds #265
  * Grammar parsing for function definition succeeds #266
  * Pynode support for def statements #269.
  * Add a callable type #270

### Other

* Reorganised backlog based on priorities - need, useful, want, wouldlike.
  Plan going forward is to primarily focus on needs, and one or two from
  each of the other categories.
* Function call code supports simplified type definitions for externals. #34
* Block structure of generated C Code is pretty/human friendly/readable #26
* Add special case for function calls like print #37


## [0.1.23] - 2016-10-11

Not backwards compatible due to changes to "print"

#### print

print is no longer a python 2 style print statement, but rather a python 3 style
print function. The reason for this is primarily down to the fact that things
like Serial.print - necessary for arduino support - are not valid python if you
have print as a statement.

It's for this reason that the new version is 0.1.23

#### Overview

Aims in this release are to start enabling more functions inside an enclosing
profile. Specifically to start enabling more arduino programs using default
pin names (eg A0) and the ability to read from analog pins. (Which requires
implementing analysis of return values of functions)

In order to make this work/work better, work on improving how contexts (mappings
of names to types) are handled has taken place, in particular nested lookups
now work (This will simplify scoping later on too).

### New

* Lots of internal changes to switch print from being a statement
  to a function call
    - Update all tests to use print as function, not as statement
    - Lexer - remove keyword
    - Disable "print" as statement type in the grammar
    - Disable "print" as a pynode in the AST model
    - Transform bare function calls to "print" (not method accesses)
      into print statements internally. This will need improving
      later, but for now is enough. It will need improving once we
      implement custom function support.

* Handle emitting identifiers as rvalues in assignments correctly

* Enable use of function calls as rvalues in assignments (eg enable "analogRead")

* Added README.md for the analog example

* Update examples/README.md overview of the various examples.

* Initial user (single page) documentation of how to use the arduino profile

### Arduino Support

Specific set of functionality checked/added in this release:

* Serial support - .begin(), .print(), .println()
* constrain
* map
* random
* analogWrite
* analogRead
* millis
* Support for constants/ids : A0-A7, HIGH, LOW, INPUT, OUTPUT

This is in addition to:

* Servos
* DigitalWrite
* pinMode
* delay

### Other

* Document how the various autogenerated docs get generated.

* Some extra scripts in test-data - designed to support quick turn around testing of
  specific language features.

* Clarify source of logging messages

* Add recursive lookup through context stacks. This allows us effectively to
  manage scope, to be able to treate profiles as an enclosing scope, and a step
  towards being able to generate better error messages.

* Created a default (empty) global context stack - may provide a better hook for things
  like print-as-function later on.

* Simplify cruftiness/verbosity of logging from parser

* Initial tests with profile nodes (for context). Tag is profile_identifier. Purpose is
  primarily to support analysis. 

* Help with debugging
  * Add tags to contexts
  * Tag global context as program context
  * Tag (test) arduino profile context as "arduino"

* Start of support for analogRead, analogWrite, (arduino) map, and Serial object
  - Example added exercising these

* Update site/src/panels/current-grammar.md to match current grammar...
  - remove print_statement
  - minor cleanups
  - Expression syntax supports expression molecules - object method access

* Updated docs



## [0.0.22] - 2016-09-25

This release sees a practicality change - specifically to allow the user
to specify which arduino board they want their code compiled for. The way
this works is to override the arduino-mk process.

As a result, in order to compile (say) examples/servo/servo-test-target.pyxie
for the arduino Uno, you change the file examples/servo/servo-test-target.Makefile.in
to contain the following:

    BOARD_TAG    = uno
    ARDUINO_PORT = /dev/ttyACM0

This generates the appropriate file. If you had a Dagi Mini, you might change
the contents to this:

    BOARD_TAG    = atmega8
    ARDUINO_PORT = /dev/ttyACM0

Full documentation will come later but this should be sufficient to get started
with.

### New

* Ability to override which arduino board you're working with.

### Other

* Minor cleanups



## [0.0.21] - 2016-09-17

Various small changes that result in the abilty to generate C++ code
for a python arduino program that looks like this:

    #include <Servo.h>

    myservo = Servo()
    pos = 0
    pin=11

    myservo.attach(pin)
    while True:
        for pos in range(180):
            myservo.write(pos)
            delay(15)

        for pos in range(180):
            myservo.write(179-pos)
            delay(15)

This isn't complete because reading arduino sensors won't work like this
yet and so on, but this is a start. The generated code doesn't seek to make
optimisations and aims to be accurate, so the above creates two iterators - one
for each range and runs those.

Internal improvements to contexts also suggest better mechanisms for handling
profiles.

### New

* Code generation for object methods. Allows things like myservo.attach(pin) and myservo.write(pos)
* Started changes regarding how contexts will be managed/accessed by pynodes
* Global context handling improved
* Internals supported for code generation of functions extended to include attribute access

### Other

* Improved notes on how context nodes will operate
* Minimal servo tests extended slightly to support moving servos

### Internal

* Simplified pynode internals (removed explicit tree type)
* Cleaned up/removed extraneous code
* Bump for release



## [0.0.20] - 2016-08-12

Bulk of changes for this release are internal - various refactoring and so
on. This isn't particularly exciting, but a release made just to say "yes
the project is still progressing".

Probably the most interesting addition is actually the creation of "WIPNOTES"
designed to support ongoing (ie WIP) development. You can also now see the
next target for the arduino profile - to support servos. This requires a
fair collection of (useful) improvements to the python type inference which
is not yet complete. As a result while the servo example *parses* it does not
yet *analyse* or *compile*.

Indeed, that's required a fair amount of rethinking about internal structure,
hence the new WIPNOTES :-)

### New

* Update arduino examples; servo target example started
* Introduces a collection of WIPNOTES

### Internal

* Bump packaging for release
* Sync website updates
* Trello/doc sync
* Prettify generated C++ files
* Sync release info
* Add newsletter subscription to site info
* Changes to support debugging analysis -- 
* Version bumps 0.0.20
* Add comment to indenting logger
* Removed use of indenting logger :-)
* Use func_label to refer to the callable, not callable_
* Experimental addition to look at name of thing, not value
* Better python 3 compatibility
* Shorten names in profile definitions for clarity
* Subsume tree functionality into core
* Update changelog



## [0.0.19] - 2016-01-31

### Fixes

* Fix regression in code generation for function calls
 * This was due to FunctionCalls now assuming they work on a callable
   which may be an identifier, but can also be other things too

### New

* Changes to support Python 3
 * Now runs under python 3 as well as python 2 :-)
* (internals) Pynode docs - very much work in progress
* Arduino blink test case copied into examples
 * Makes testing easier and usage more obvious


### Internals

* Massive reorg of pynodes from single file to categorised files
* Use annotated tags for releases - makes them show up on github - showing
  releases
* Help text for pyxie-dev extended to show release process
* Bump versions for 0.0.19

### Other

* Work on arduino profile continues with more work on servos (still WIP)
* Bump copyright notices to 2016(!)
* Add link to latest release on homepage



## [0.0.18] - 2016-01-10

### New

* Parsing of "long" integers, treating "l" as unsigned long values and "L" as signed long values.
* Code generation for long and unsigned long values works
* Add first major example of a pyxie parsable program - for controlling a 4 legged robot - DAGU playful puppy (8 servos for 4 legs, 2 for pan/tilt in head, IR Array)
  -- Does not parse/compile yet! (But will!)
* Add parsing of attribute lookup for objects
 * Parsing tests for object attribute and method access
 * Test cases for attribute access
* Add simple servo example
 * Couple of versions to simplify development - target version + simplest
   working version
* Some helper scripts to help while building/testing examples
* Redo function calls to allow attribute access ordering
* Recast identifier in functions as a callable expression
* Initial version of arduino function call descriptors
* Initial support for arduino profile in pynodes
* Code generation for first arduino specific types (specifically "Servo")


* Re-enable parse only option
* Allow expression atoms to be negatable, not just numbers (allows things like -step/2)
* Remove trailing semi-colons in arduino-blink test
* Fix Missing import regarding parsing testfiles in bin/pyxie
* Changes regarding precedence of brackets to other expression atoms

### Other

* Add a list of the high level things 'missing' to Language status
* Support for dumping the parse tree results as a json file - for debug purposes (disabled in code by default)
* Restores long/unsigned hinting where necessary
* Update range to support start, end and step - replacing max
* Test case for new range implementation
* Make PyAttribute's jdump correctly
* MAJOR Clean up how options are handled - shifted into introspected classes in bin/pyxie, along with improved internal docs
* Initial cleanup inside bin/pyxie-dev
* Improve lexing error messages
* clib updated

### Will need revisiting

* Do not clean up builds temporarily



## [0.0.17] - 2015-08-12

### New

* Implemented "pass" statement.
* For loops now work on arduino profile (reimplemented C++ generators to use
  generator state, not to use an exception)
* Arduino test case using for loop

### Other

* Extracted core code for "pyxie" script into pyxie.core
* Updated usage instructions to include covering using arduino profile
* Documentation updated to current status (to a large extent)



## [0.0.16] - 2015-08-02

Summary: Adds initial Arduino LEONARDO support, improved function call, release build scripts

In particular, to compile for a compilation target you do this:

pyxie --profile arduino some_program.pyxie

This will generate some_program.hex. You then need to load this onto your
arduino. Support for assisting with this will probably be in a largert
version. Requires Arduino.mk to be installed in a standard place. Docs TBD
as functionality stabilises.

### Features

* Arduino LEONARDO compatible compilation profile (#3)
  * Detect that we are in a profile mode from a command line switch (#3.1)
  * Code generation is called with current profile (#3.2)
  * Code generation outputs code targetting "setup" instead of "main" (#3.3)
  * Makefile uses the arduino makefile #arduino leonardo (#3.4)
* Compilation profiles support removal of elements of the clib (#4.1)

* Function calls that do not require arguments work (#2)

### Docs

* Docs in README.md, setup.py and docs/ are generated from website. (#66)
* Documentation in /docs is generated from website source documentation (#63)
* Docs on usage #docs (#64)
* Man page for pyxie (#65)

### Other

* Make Release Script (#61)
* build_release_script.py (#62)
* Core setup.py files/etc now auto-generated from templates

### Other

* Clean up build local script
* Man file added (not installed yet though)
* Build distributed docs from the same source as the website
* Added pyxie-dev script to assist in release automation
* Re-enable doc building



## [0.0.15] - 2015-07-18

* clib converted to py clib for adding to build directory



## [0.0.14] - 2015-07-18

### New

* clib - this will be a collection of C++ code that can be directly or indirectly used in  generated programs. Current focus is iterators
* C++ generator support - to support C++ iterators
* C++ generator implemention of python's range iterator + acceptance test harness
* Lex/Parsing of For
* Type inference/analysis for special cased iterator functions
* Pynode representation of for loops
* Code generation for for loops using iterators

### Other

* Extra test case for while - testing 3 way logical expressions
* Test case for for loops
* Massive website revamp



## [0.0.13] - 2015-06-21

This probably marks the first release that's potentially properly useful when combined with
an appropriate included .h file... We support if/elif/else while/break/continue and arbitray
expressions.

### New

* Support for if statements
* Support for elif clauses (as many as desired)
* Support for else clauses
* Support for boolean operators - specifically and/or/not, including any mixture
* Support for parenthesised expressions



## [0.0.12] - 2015-06-17

### New

* Initial iteration of website - hosted at www.sparkslabs.com/pyxie/ . Stored in repo
* support for while statements:
 * While works with While True
 * Break works with With True
 * 'Continue' works in a While loop
 * While Loop conditional is a expression
  * This allows things like loops that count towards zero and do things... :-)
* Comparison Operators :  < > <= >= <> != ==

Combination of these things allows things like countdown programs, basic
benchmarking and so on. Creative use ( while + break) allows creation of "if" like
constructs meaning the code at this point supports sequence, selection and iteration
as well as very basic datatypes. That's almost useful... :-)



## [0.0.11] - 2015-06-06

### New

* Function call support:
 * Extended Grammar, and pynodes to support function calls.
 * Code generation for function calls
 * Test cases for function calls added
 * Creation of  "Print" built in for the moment- to be replaced by 'print'
* C++ "bridge":
 * Create simple C++ include bridging - #includes are copied straight through
 * Document C++ bridging, and test case

### Changed

* Language Spec updates

### Fixes

* Support empty statements/empty lines



## [0.0.10] - 2015-06-03

* Documentation added to pyxie/__init__.py, to allow project level help from "pydoc pyxie"
* Expression Statements
* Improved type inference in explicit analysis phase 
 * Explicit analysis phase added - decorates AST, focussed on types. Results of this phase viewable.
 * Pynodes are now tree nodes, simplifying tree traversal for common cases
 * Variables are managed by contexts -- context is added to pynodes during analysis phase, simplifying type inference
 * Contexts changes to store name and list of expressions -- not name and identifier, again, simplifying and generalising type inference
 * Ensure all identifies in global context *before* analysis starts, simplifying analysis phase
 * New strategy for type inference documented, opens up lexical scoping
* pyxie compile harness now runs/compiles programs outside the pyxie tree



## [0.0.9] - 2015-05-23

Primary changes are to how the program is run, and fixes to precedence. This is the first
version to support a non-test mode - so you can output binaries, but also JSON parse trees.

### New

* Test modes for pyxie harness moved into a --test mode
* Standalone parse mode -- pyxie parse filename -- parses the given filename, outputs result to console
* Standalone compiler mode --
 * pyxie compile path/to/filename.suffix -- compiles the given file to path/to/filename
 * pyxie compile path/to/filename.suffix path/to/other/filename -- compiles the given file to the destination filename

### Changed

* Switch to left recursion. The reason is because YACC style grammars handle
  this better than right recursion, and the fact it also fixes operator precedence
  correctly in expressions. The reason the grammar was originally right recursive
  is because that's the Grammar that CPython uses, but the parsing process must
  be different (since it's LL(1) and suitable for top down rather than bottom up
  parsing)

### Fixes

* Bracket negative literal values in expressions to avoid confusing C++
* Precedence as noted above.



## [0.0.8] - 2015-05-13

### Changed

Switched compilation over to using PyNode objects rather than lists

Rolls up alot of changes, and improvements:

* Simple test case for testing expressions in assignments
* Added release date for 0.0.7
* Bump revisions for next release
* Use PyNodes to represent python programs
  In particular, this replaces the use of lists with the use of objects.
  The aim here is to simplify type inference from code, and injection of
  context - like scoping - into the tree to be able to infer types and
  usage thereof.

* We're doing this at this stage because the language is complex enough for
  it to start to be useful, but simple enough for it to be not too difficult
  to switch over to.

  Furthermore, by allowing nodes to generate a JSON representation, it's easier
  to see the actual structure being generated - to allow  tree simplification,
  but also to allow - at least temporarily - decoupling of changes from the
  python parsing from the C tree generation, and from the C code generation

* Clean up statements node creation in grammar
* Simplify expression lists
* Support iterating over statements
* Transform pynodes to CST lists for assignment
* Reverse number order to not match line numbers
* Iterate over expressions within an expr_list
* Convert assignments from pynodes
* Remove old code
* Can now transform basic core programs based on pynodes
* Code generation for expressions as rvalues
* Better test for code generation of expression rvalues
* Add context into pyidentifier nodes
* Support transforms for expression rvalues in assignment
* First pass at adding context - variable lookups into the system
* Test case that derives types for variables



## [0.0.7] - 2015-04-29

### Changed
- Bump revision for release
- Compiler structure & testing improvements
- Initial support for infix integer addition expressions
- Support for plus/minus/times/divide infix operations
- Add test regarding adding string variables together
- Make parser more relaxed about source file not ending with a newline
- Bugfix: Fix precedence for plus/minus/times/divide
- Bugfix: Only output each include once



## [0.0.6] - 2015-04-26

Overview -- Character Literals, math expressions, build/test improvements

### Changed
- Character literals - parsing and compilation
- Initial version of changelog
- Mark WIP/TBD, add character
 - Adds character type, mark which bits of the spec are now TBD, and which are WIP
- Add "in progress" section to CHANGELOG
- Build lexer explicitly
- Basic mathematical expression parsing
 - Parsing of basic expressions involving basic mathematical operators, as opposed to just value_literals.
- Test case for parsing mathematical expressions
- Allow parser to be reset
- Restructure test harness to allow more selective testing
  This also changes the test harness to be closer to a standard
  compiler style API.
- Run all tests from makefile
- Codegen test for basic math expressions
  Simplest possible test initially



## [0.0.5] - 2015-04-23

### Added

- Core lexical analysis now matches language spec - collection of changes, which can be summarised as follows:
 - Language spec updated relative to implementation & lexing states
 - Lexical analysis of block structure
 - Lexical analysis of operators, punctuation, numerical negation
 - Implement numbers part of the grammar (including negation), including basic tests
 - Fleshed out lexical tokens to match language spec

### Changed

- Code cleanups



## [0.0.4] - 2015-04-22

### Added

- Extends C AST to match python AST semantics
- Ability to use mixed literals in a print statement (1,True, "hello" etc)
- Argument list management
- Convert argument lists explicitly

### Changed

- Use Print not print

### Fixed

- Cleaned up debug output.



## [0.0.3] - 2015-04-21

### Added

- Adds ability to print and work with a small number of variables
- Better handling, and code gneration for integer literals

### Changed

- Add long description (setup.py)
- Update README.md to reflect project slightly better
- Reworded/tightened up README
- Updated documentation
- Emphasise "yet" when saying what it does (README)
- Zap the source between compilation runs
- Build test results inside the test-data/genprogs directory



## [0.0.2] - 2015-03-30

*Initial Release* -- 0.0.1 was not released and rolled into 0.0.2 (release notes for 0.0.1 below)

Simple assignment

### Added

- Transform Python AST to C CST - compile python to C++ for v simple program

### Changed

- Various tweaks for README/docs
- Packaging for pypi and Ubuntu Launchpad PPA for initial release 0.0.2



## [0.0.1] - Unreleased - rolled into 0.0.2

### Added

- Initial structure, loosely based on SWP from a few years ago
 - http://www.slideshare.net/kamaelian/swp-a-generic-language-parser
- Initial pyxie parsing/model/codegen modules
- Basic parsing of value literals, decorated with source information
- Support for basic identifiers and assignment including simple type inference
- First pass at a simple C++ code generator for concrete C++ AST
- Directories to hold semantic models and for code generation
- Represent C programs as json, and allow construction from json
- Simple program that matches the C++ code generator
