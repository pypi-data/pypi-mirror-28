# EnforsML - Enfors Machine Learning library

Project state: early planning

In its current state, this library only supports chatbot backends.

# text - text-related classes

## word

## ngram

## bagofwords

## utils

## nlp

Functionality related to natural language processing for chatbots and
the like.

### How to create a parser

1. Identify, in general terms, the commands that the parser should
   recognize. These are the Intents.
   
2. For each Intent, amass a collection of sentences that the user
   could be expected to type when they want to invoke this command.
   These sentences will be used to train the Intent to recognize
   similar sentences.
   
3. Add each of these Intents to a Parser.
   
3. When you have text input from a user that you want to parse, give
   it to a Parser and the parser will feed this text to each Intent in
   turn, and the Intents will return an object indicating (among other
   things) how likely the Intent thinks it is that the user was trying
   to invoke that specific Intent. This is called the confidence
   score. The Parser will then return a list of Intents with a
   confidence score higher than zero, sorted by the confidence score
   (descending - highest first).

### Context

An Intent can do (among other things) these things:

1. It can *enable* a context

2. It can *disable* a context

3. It can *require* a context to be active for the Intent itself to be
   triggered
   
#### The context interface - how to create them, etc

A web interface is planned, but for now, we create contexts directly
in the code as part of an intent's training data. Lines in the
training data that begin with an at sign are context directives. They
come in three forms:

    @enable FooContext
	
This (creates and) enables the context named FooContext.
	
	@require FooContext
	
An Intent that has this directive can only be triggered when the
FooContext context is active.

    @disable FooContext
	

#### The context implementation - how they work internally
   
When an Intent is trained, it starts by looking for lines in the
training data that begin with an at sign. If the at sign is followed
by "enable", "disable" or "require", then the Intent data structure is
updated accordingly, and the line is removed from the training data
before it is passed on to the actual training.

The parser also has a list of all contexts that have been created, so
that it can check which of them are enabled at any time.


### EMLB format

The ``EMLB`` (Enfors Machine Learning Bot) format is a format for
storing bots in a text file.

    Hello, I'm ExampleBot. How can I help you?
	
	What can you do?
	I can't really do much, I'm just an example.
	
	Who wrote you?
	Who made you?
	Who programmed you?
	Who developed you?
	Who created you?
	I was created by Christer Enfors.
	
	I want to sign up for the mailing list
	I want to subscribe to the maiiling list
	I want to be on the mailinglist
	All right, what's your email address?
	@enable ReceiveEmailAddress
	
	@require ReceiveEmailAddress
	@storeinput email
	Thank you, you're now subscribed.
