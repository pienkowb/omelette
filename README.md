# Omelette 

Omelette is a language dedicated to describe UML diagrams. Currently we support only class and use case diagrams, but the language and compiler are designed to be extensible.

Omelette consists of three parts:

1. Omelette - Language used to describe UML diagrams
2. Fromage - Simple IDE for editing, generating and exporting diagrams.
3. cli - command line compiler of Omelette

## Dependencies
Omelette requires **pyQT** and **pyparsing**.

Although it's not required, we encourage you to install **pygraphviz**. We offer two built-in layout algorithms, but they aren't very impressive.

## User Manual

Currently there's no such thing.

If you speak polish you can read [our report](omelette/raw/master/doc/raport/raport.pdf). 
You will find the manual and semi-formal description of language syntax there.

## Code Example
    class Student
      +learn(stuff)

    class University

    association
        source-object : Student
        target-object : University 

    prototype class course
        stereotype : "course"

    course Course

    course compSci
        name : "Computer Science"
        +code()

    course Art
        +dance()
        +paint()
        +play()

    prototype generalisation is_crs 
        target-object : Course 

    is_crs
        source-object : compSci
    is_crs
        source-object : Art

This compiles to:

![uml diagram](raw/master/doc/example/university.png)

As you can see, the language is pretty powerful.
This example covers some features of Omelette:

1. classes, and different types of relations (currently we also support notes, use cases, actors, and other types of relations)
2. properties and operations (we also support attributes)
3. prototyping (objects `compSci`, `Course` and `Art` inherit stereotype from `course`; There are also two anonymous `is_crs` objects, which inherit theirs target object from `is_crs`).

[more examples](tree/master/doc/example)
