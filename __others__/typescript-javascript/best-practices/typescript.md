# Extracted Notes - TypeScript

## Table of Contents

- [Overview](#overview)
- [Browser](#browser)
- [Types](#types)
- [Functions](#functions)
- [Object](#object)
- [Loops](#loops)
- [Patterns](#patterns)
- [Async and Events](#async-and-events)
- [Events](#events)
- [jQuery](#jquery)
- [Hoisting](#hoisting)
- [Symbols](#symbols)
- [Maps and Sets](#maps-and-sets)
- [Recursion](#recursion)
- [Closure](#closure)
- [Modules](#modules)
- [JSON](#json)
- [Web-workers](#web-workers)
- [Linting](#linting)
- [Regex](#regex)
- [AJAX](#ajax)
- [Error Handling](#error-handling)
- [Polyfills](#polyfills)
- [Compilers](#compilers)
- [Data Structure](#data-structure)
- [Problem Solving](#problem-solving)

## Overview

- JavaScript was originally called Live Script, Netscape changed its name to JavaScript, and it is believed that this was because of the hype of Java within the industry.

- It is like a JavaScript, with guard rails. An interface defines the shape of data. It is like a mold used to create baked goods such as muffins. It drives consistency across the objects.

- Typescript also support new features of ECMAScript and other features which even didn't introduced yet in ECMAScript like interface.

- When using the typescript types we should not use the uppercase javascript types, we should be using the typescript types i.e. lowercase versions of them – like number instead of the Number.

- Order of operations – PEMDAS.

- It is like a JavaScript, with guard rails.

- JavaScript has nothing to do with Java, similar names for marketing reasons. Developed by Netscape in 1995 to create products and applications that run in the browser. It is primarily client side. It was originally designed as a scripting language, it is actually a fully featured language.

- Lexical scope and dynamic scope: Perl and bash languages only have dynamic scope. Lexical scope means compile time scope, when it is parsing our code. Lexical scope is like building going from first floor to top floor to find, or nested scope bubbles.

- Dynamic scope – The decision of how scoping works in dynamic scoping, is a runtime decision as opposed to, in lexical scoping it is an author time decision. In dynamic scope inside the function of foo, when we reference a variable bar, it will not look where the code was written but it instead would look at the call stack.it will look for the code which called this foo function, so it will go one level up to the call stack.

- In JavaScript if we keep a reference to an object around, that object doesn't get garbage collected until it is not referenced any variable. Same behavior works with closure, when we execute a function, it creates a scope object. If there is anybody that gets a reference to that scope object via closure, that scope doesn't get garbage collected when the function ends.

- JavaScript and Lua are only two languages which are object oriented; others like C# are just class oriented languages. Only in these languages we can create object without a class.

- ES2017 is unofficially called ES8. JS was created by Brendan Eich, he was told to create java like language for Netscape browser. ES is a standard that guides the path of JS.

- Human head has two systems – head and gut. Head is the higher level one, its analytic, its algorithm, it is where we do mathematics and reasoning and logic, it requires tremendous amount of effort and a bit slow, most of the time we need to turn it off, due to its slowness only we needed to invent computer. Another part is gut, it is intuitive, heuristic, associative and very, very fast, requires no effort and we cannot turn it off, it is on all the time. Head gets its assumptions from gut and it is not aware of that connection, its think it is getting results from vault of deep truth, but as it is getting from gut, sometimes head can get wrong input.

- The computer programs are most complicated things that people make, there is nothing else in human experience which is composed of as many tiny little pieces which all have to go together perfectly that have to work in real time with changing states and changing inputs in a dynamic situation.

- Initially the goal of the AI originally was to figure out a way to have the computer write their own programs because it was just too hard to have humans writing them.

- There is no test for the perfection of a program, we have tests for imperfection. None of our programs are perfect.

- Programming uses head and gut both. But we don't understand how we write program, we just write instruction to create a program and hand it over to someone else those instructions, we cannot tell someone else how to do it and that's why we can't tell the machines how to do it. We look at a problem and we will look at top-down and bottom-up and take a macro view and a micro view, we keep constantly shifting our point of view until eventually a program emerges and we don't know how we do that.

- JS was designed as a language for beginners, that was the original goal.

- A good style can help produce better programs, it should not be about personal preference and self-expression but to reduce the error rates.

- In English language itself lowercase, word breaks, and punctuation into their manuscripts to helped reduce their error rates and easier to read, earlier it was all caps letter with no space.

- History of JS – at the national centre for super computing applications at the university of Illinois, there were couple of kids who were developing a client program for internet for number of protocols like WAIS, Archie, Gopher, FTB, Finger and WWW, they called this program MOSAIC. Finally, out of these protocols the WWW won, this format can also display image tag. A bunch of the people from that project were lured to California where they become part of a company called Netscape. Netscape made the first commercial web browser called Netscape navigator and it was a huge hit. For the new release of this navigator they also wanted to make it easy for end-user programming, they remembered something that had been on Macintosh called HyperCard, that was a simple application program based on a simple metaphor of stacks of cards and it was an event driven script thing and remarkably easy to use and they wanted something like that in the web browser. So, they gave this job to Brendan Eich, his idea was he would write a scheme interpreter to do this like he was told to do in a language like java or visual basic which people like and popular at that time, this if for the kids. He was given 10 days to create a prototype of this new interactive browser and in those 10 days he designed and implemented a new programming language which is an amazing achievement. So, from java he took syntax another language was scheme which is a dialect of LISP, scheme has lambdas i.e. functions, there is a dialect of small talk called Self it was having better performance and expressive, from Self he didn't took the feature of classes, by removing classes they could make it much faster and much better to program. Netscape called this initial language as LiveScript. While this is going on another language that was being developed by a guy at Sun named Jim Gosling, they wrote a web browser in this language the browser called hot java, the language name was Java and become wildly successful. These both companies were working against Microsoft, so they form an alliance the first thing they agreed upon that Netscape adds java to the web browser in-exchange for that Sun will drop their hot java browser. Another thing is that they have to kill LiveScript as they were saying to the world that Java is the last programming language world ever need, but Netscape denied that because Java was not for beginners and they also wanted to launch the new browser right away and so the way they put Java in was they had Java talk to LiveScript through an interface called Live Connect. So, LiveScript could talk to the browser and java could talk to LiveScript through Live Connect. And if they took LiveScript out, Java wouldn't work, so to save the alliance they change the name of language from LiveScript to javascript, and to showcase not a new language but as a subset to javas, interpreted java and they lied about the relationships of these two languages.

- Meanwhile after seeing this Microsoft had completely missed the web and the internet, they thought the future of telecommunications was going to be fax and cable TV. So they bought out a browser company, it was another spinoff out of Illinois called spyglass, took their thing and relabelled it as IE and decided that they also need one more thing related to JS. So, they reverse engineering the first JS engine. MS also noticed all the blunders, bugs, errors, design defects, MS carefully documents all of them and replicates them, they called it JScript. Then Netscape went to w3c to make the standard of their language, but w3c denied then they went to ISO, and then European computer manufactures association (ECMA), MS also joined this committee and dominates the committee. Also, MS told that all the bugs will remain in the standard, those standards where published by name ECMAScript.

- Javascript provides concept of delegations i.e. differential inheritance, where an object can only do what it can do and if its asked to do something that it can't do, it will designate another object to do that work on its behalf.

- ECMAScript versions -

  ![node-js-ecmascript-versions](./images/node-js-ecmascript-versions.png)

- REPL stands for Read, Eval, Print and Loop. Use the ctrl + l to break the REPL session.

## Browser

- Alert pop-up box is given by the browser not by the JavaScript.

- Browsers are typically single threaded, either do update UI or executing JavaScript a piece of time. Unless we use web workers concept to avoid this. Long running process make UI unresponsive. To avoid this use timeout for realize the thread to go back to the UI process quickly to avoid this unresponsiveness.

- BOM refers to the browser object model and that lets us access functionality in the browser. We can change the URL we are pointing at, get information on the URL. DOM is document object model we use this to change the actual web page.

- Window is a global object in JS, we can access it from anywhere. Important key things are below –

  ![typescript-important-document-api](./images/typescript-important-document-api.png)

- Unfortunately, in the browser the use of global variables is required because there is no kind of linkage mechanism that allows one compilation unit to find another. They just share a common global scope. So, in browser use very minimum global variables and named the as UPPER_CASE.

- Initially HTML was intended for simple document viewers, it wasn't intended to be an application platform. The DOM is the API that the browser presents to JS and it is one of the worst APIs ever invented. The inventory tried to implement the HyperCard like system as DOM.

- When those kids then move to Netscape, their goal was to kill Mosaic, they wanted to create a monster that kills Mosaic so they make a Mozilla. In this instead of waiting for the images to get downloaded they put a placeholder at that point and continue resume parsing, it improved the user experience.

- W3C was not happy about JS surviving in the web after they rejected it. There was a lot more sympathy for Java at W3C then JS, so over these years they have been trying to replace the API with something that would be more friendly for Java than for JS, even though the Java has never lived in browsers in this way. So, they added methods like getAttribute() and setAttribute().

- CSS and DOM were both designed about the same time and each project was aware of the other. The guy who designed CSS was aware that someday programming language were going to manipulate style sheets, he thought that was a certainty, and yet he choose to use the minus sign as a hyphen, knowing that most of our programming languages want to do subtraction with it and this creates syntactic difficulty for all of us.

- The W3C standard doesn't provide access to the HTML parser, all browsers implement MS innerHTML property but it is a security hazard.

- Browsers are really good at is parsing HTML and they can do that really quickly and they can get the whole thing done in one transaction whereas messing with the DOM, every time we touch the DOM we are going to pay a big time penalty.

- Netscape 2 version introduced the Events, the browser has an even-driven, single threaded programming model. Events are targeted to particular nodes; events cause the invocation of event handler functions. The target is the topmost (z-index) node containing the cursor.

- Trickling and Bubbling – MS choose the bubbling approach which was correct way to do it.

- Servers are significantly different than browsers, in a server, we are not dealing with events, we are dealing with messages like messages coming from network, we will do something, we will send another message out.

## Types

- The REST parameter is used in function definition and the Spread operator is used in function invocations.

- Static and Dynamic typing – typescript is static typing and have type safety is a compile time feature.

- In JavaScript, the variable does not have types but value has types. So, any variable can have any type of values. It is different behavior from the static languages.

- JavaScript is also a complied language, not interpreter. Because in interpreter while executing line 3 it has no idea what it is on line 4. In JIT just in time compilation, it won't compile the function at instance, but when it was force to, means when we will call that function.

- Undefined means the variable was declared, but it has a special empty value that we mistakenly called undefined. It is uninitialized. It doesn't mean undeclared, it is like vacuum. Undefined is a proper value.

- The number type in JS is IEEE-754 format, this format is prone to rounding errors, but by this we can represent integers and floating point numbers.

- We can use String.raw() method if we don't want special character to get render on the UI like '\t', '\n', etc, they will get printed as a raw string.

- The length of the emoji is not 1 unlike normal string characters, it can vary from 1 to 7, etc. String a Unicode character can get fit into 16-bit unit, but not emoji.

- The "void 0" is a primitive value of undefined.

- We can use special characters inside strings but it needs backslash notation like below

```typescript
"Flight #: \t921\t\tSeat:\t21C"
```

- We cannot add a property to interface declaration if it is private or protected. Only public properties can be added to the interface signature.

- The void type is not exist in javascript language.

- We can use 'never' type when a function is not going to return any value like if that function throw an error.

- To define different types of data in a array we can use tuple to enforce king of fixed structure instead of a loosely one. So, if use type as [string, number, boolean] then the values should match the same order type unlike union type.

- An interface defines the shape of data. It is like a mold used to create baked goods such as muffins. It drives consistency across the objects. Unlike Interface, Type can also be used to represent primary types not just object like data structure.

  ![typescript-interface-vs-types](./images/typescript-interface-vs-types.png)

- The 'typeof null' will return generic 'object' value.

- Type Guards – they are a way for us to check the type of a variable. They are a way for the compiler to narrow a variable to a specific type. By this the compiler can check more error based on type. The typeof type guard, instanceof guard, user-defined type guards

- Symbols – they are new primitive data type, they are unique and immutable. Every symbol we create is different from every other symbol. Once we created them we can't change them. Use case for them – to make good unique constants, enum like behaviour, computer property declarations to avoid name collisions, customize internal language behaviour. The string passed below in symbol is just for debugging purpose.

  ![typescript-symbol1](./images/typescript-symbol1.png)

  ![typescript-symbol2](./images/typescript-symbol2.png)

- Decorators - They are like annotations in java and attributes in c#. In JS they are implemented as functions.

- Generic Constraints – they describe the types that may be passed as a type parameter. Constraints are most often implemented as interfaces that describe the shape of types that may be used as a type parameter. We need to use the extend keyword.

- We can't use generic with static functions or classes as generic gets applied on the instances. Generic classes offer type-safe versality (with or without implementing an interface).

- Abstract class are created with the abstract keyword, we cannot directly instantiate this class but they can contain the implementation details but also can have abstract methods which are not implemented but these methods must be implemented in derived classes.

- Duck Typing – in below we don't need to specify the probablyADuck variable as a Duck type, it is considered automatically as it has all its methods.

  ![typescript-duck-typing2](./images/typescript-duck-typing2.png)

- Type Declaration Files - They are also called type definition types or type libraries, these are just wrapper for existing javascript libraries. The goal of type declaration file is to declare types for the variables, functions, objects and other constructs in the library that match the intended use of those items. This allows the typescript compiler to make sure that we are using the library correctly. We can find the problems at compile time. They are just development-time tool to assist the compiler. They end with "d.ts" extensions.

- Generics – as below we can create collection of T, it is being to known when we create the instance of the class. Behind the scene the typescript will create a hidden class of that type and will be present in the transpiled code. We can also create generic interfaces and functions not just classes.

- Generics are not supported in Javascript, due to this it is a feature of Typescript. It is a reusable code that works with multiple types. It may be function, interfaces or classes, it uses a type (`<T>`) parameter. Generic constraints increase practicality and generic function type add flexibility. We can't use generic with static functions or classes as generic gets applied on the instances. Generic classes offer type-safe versatility (with or without implementing an interface).

- TypeScript implements structural type system, so in below the object developer can be directly treated as interface as it has all the interface properties. As long as the structure match, we can treat the object as the type with that structure event if it wasn't explicitly declared with that type. This is also called duck typing:

  ![typescript-duck-typing](./images/typescript-duck-typing.png)

- Static members are a nice way to add utility or helper methods that are related to the purpose of class but aren't dependent on any data that might be stored in instances of the class.

- Traditional functions are still easier to read when we are writing function that will be called from multiple places, however arrow functions are nice when we need to pass an anonymous function to another function.

- Basic typescript types – Boolean, Number, String, Arrays, Enum, Void, Null, Undefined, Never – it's the type assigned to values that will never occur like function that will never return because it throws exception or kicks off an infinite loop, Any – use when we effectively want to opt out of type checking of the compiler like while using third party javascript library .

- Type assertions – if we do not know the type of a variable, then we can assign it a specific using type assertion. (`<number>` value) or use "as" keyword

- In 40s when the first Von Neumann machines start coming online they are integer-only machines, but most of the programmers are mathematicians and they are trying to figure out how to do read computation and it is hard, they were trying to do stuff with scaled integers and it is lot of work, and it is error prone. And someone figures out floating point, that we will have two numbers per number, one is the number itself and other is a scale factor, which tells us how many positions to move the decimal point. Then we can just give it to a subroutine, and subroutine will figure out how to add these things. And it worked and it made programming much easier to do. Unfortunately, those libraries were really slow. So, when we get to the 50s, there is now interest in putting floating point into hardware, but we were making out stuff of tubes, and it is hard to do. Someone has figured it out that if we use binary floating pinot instead of decimal floating point, we don't have to implement a dive by 10 in order to do a scaling, we can just shift 1 bit, which is free. That worked great for scientific computing because in scientific computing, our lower digits are probably wrong anyway, but it doesn't work for business processing because they are adding up money and they need to be exact. They have to give the cents exact. So, even successor like java is not good with business types, that is the tragedy we are in now. The solution might be below, this might be only 1 number system which a future language needs to be adopt –

  ![typescript-dec-64](./images/typescript-dec-64.png)

- If we are adding integers in a software implementation, it can add two integers and five instructions, in a hardware implementation adding integers should happen in once cycle, which means we don't need to have int as a separate type in order to get performance. We can get performance and range of values that we need in one number type.

- As a developer we don't assign undefined to variables, we let the JavaScript to do that, we should use null assignment in that case. The null is an object type and type of undefined is undefined itself.

- Crude computation bug – below will make the infinite loop. JavaScript only has 1 number type and it is IEEE 754 double-precision floating point, by this we can represent wide range of values but downside is that some of the precession can be lost in the process.

  ![typescript-number-type](./images/typescript-number-type.png)

  ![javascript-number-type-2](./images/typescript-number-type-2.png)

- We cannot compare NaN with NaN, it will give false. So we need to call isNaN(NaN) function instead

- Pregnable property bug – for-in works with arrays and other types, however, it is most valuable when iterating over an object, but it will also iterate the prototype properties as-well, to avoid this use hasOwnProperty() method.

- The '++' operator was used to do pointer arithmetic, now it is used to add 1 to variable, we should not use this operator. Instead of this use compound operators like '+='.

- We also get NaN as a confusing thing from IEEE format; it is the result of confusing or erroneous operations.

- Array is a contiguous series or span of memory divided into equal size slots where each slot is indexed by a number; very fast, very efficient. One advantage is that we don't need to provide length or type when creating an array. We don't have to worry about out of bound array, as it is not an actual array but an hash table, so every value is in bounds, in first version of javascript they forget to add the concept of array.

Timestamps - A timestamp represents the time elapsed since January 1st, 1970, at midnight (UTC). This is also called the Unix Epoch. It's measured in milliseconds (1 second = 1000 milliseconds). Timestamps are absolute values, meaning they're great for calculations like finding time differences. Timestamps are super handy because they're precise and easy to work with, especially for: Generating unique IDs, Setting expiration times (like cookies), Calculating differences between dates.

Timestamps are simple numbers that represent milliseconds since 1970. Use them for unique IDs, date calculations, or expiration logic. JavaScript provides multiple methods to work with timestamps. Absolute values make timestamps great for finding differences between times.

## Functions

- The pop, push and shift method will automatically modify the array’s length as they don’t assign the undefined to the deleted array element.

- Arrow function have lexical binding scope, it means they get bind to the scope where they are defined, not where there are run.

- By using an immediately-invoked function, we can call returning function instantly instead of variable storage.

- Nested arrow functions share the same 'this' instance, the 'this' value is always the containing code which is also called Lexical Binding.

- There is no built-in arguments object in arrow function, if we need to iterate over arguments the use ES6 rest parameter instead. Also arrow functions aren't new-able as they use lexical scope. Always use a standard function as the constructor of a function style class.

- Constructors – special type of function gets executed when new instance of the class are created. Using super() we call constructor of parent class from child class, if child class has constructor method then we need to call super()

- While passing the values to a function called arguments, and in function declaration they are called parameters. These two terminology cannot be used interchangeably.

- Call site of "this" keyword – four rules – default binding rule , this rules says that if we are in strict mode, default 'this' keyword to the undefined value, if we are not strict mode, then default the 'this' keyword to global value. Example for this rule is foo(); call. Third rule is implicit binding rule, the call site binding object will become the "this" keyword value. Example is o2.foo().

- Explicit binding – if we use .call() or .apply() at the call site, both of those utilities take as their first parameter a "this" binding.

- Ways in which we can define JavaScript function, last one is preferred and myObject name should be like a namespace name for your application. Function 2 and function 5 will be available on the global scope.

  ![typescript-function-defining-ways](./images/typescript-function-defining-ways.png)

- The apply() let us use a parameter name args which has all the arguments, unlike call() method in which we need to specify the each parameter separately.

- Function has a 'function' type in JavaScript. In JavaScript functions are first class object we can assign them to a variable.

- Avoid call-back hell or Christmas tree code in your program by using named function. Do not use anonymous functions. In our final callback call we should return it by 'return' keyword to specify that everything is done.

- Using callbacks – we can take something that is fundamentally asynchronous like a timer, and express it in such a fashion that we can reason about that asynchronously code in a synchronous fashion.

- Callback hell: it is not about the indentation, there is a trust issue with callbacks, in this we can giving our piece of code to many some 3rd party library to execute, which call it many times like in a credit card transaction scenario. So we are giving the control of this program code to untrusted library, which is also called inversion of control. Callback hell is giving over control of your program.

- Arrow functions are used to make 'this' easier to understand. Below code will return the window object, not the document object which would be the case if we do not use arrow function. So, we are no more limited to have access only object which called the function means context of the function:

  ![typescript-arrow-function-issue](./images/typescript-arrow-function-issue.png)

- Below code as well will return the window object not the invoice object:

  ![typescript-arrow-function-issue2](./images/typescript-arrow-function-issue2.png)

- Iterator is an object that let us iterate through an array, an object, a string, or even our custom objects.

- Generators is a special kind of function that function can yield right in the middle of execution and return to the calling function example if we want to create a function that will return a dataset row by row we can create generator for that.

- Using same method name at multiple levels in an object is called shadowing.

- The `prototype` points to the prototype of the constructor used to create the object. It is a linkage from one object to another object. By this we can call a property or a method on an object reference , and it can't handle that object or property, if it can't handle that, it delegates up to prototype chain to a different object. We can find out where an object's [[prototype]] points to using dunder proto, Object.getPrototypeOf, and ".constructor.prototype".

- Inheritance vs. prototypical inheritance – they are opposite to each other, one of them is copy down, one of them is a delegation up the chain. We should say JavaScript has behavior delegation not inheritance.

- Use omitBy() function from lodash to send only the changed property with a PATCH request –

  ![node-js-using-omitby-with-patch-request](./images/node-js-using-omitby-with-patch-request.png)

- Arrow Func – it is used to deal with the issue with scope in callback function in which anonymous function passed as callback to other function create their own scope. Arrow function bind the scope of where they are defined, not where they are used which is also known is lexical binding. We get rid off the function name and use arrow for it.

- Braces are used to create blocks in JavaScript.

- Nested functions are in scope of outer function, braces do not create scope. Variables declared inside a function would not be accessible outside of that function.

- We can use IFFE, revealing module pattern to create encapsulation for module and to avoid global scope pollution. IFFE gets invoked when declared, it won't be callable from another code, but they are not for dependency management.

- We can use function for creating encapsulation, functions are objects that does something. We can have higher order function which we can pass around within other function as a parameter. Functions have scope.

- Arguments is a special keyword that lives inside a function and it gets a value of the arguments that we pass in the form of an array-like object. It is an array like object as it won't have many array methods like slice on it.

- Scope is created dynamically whenever we call a function. Whenever we call a function we create a new scope, using the same function we can have different values based on the parameters.

- Higher order function either takes a function as an argument or it returns a function as an output.

- Underscore library - Difference between map and each function – from each we cannot return anything, use map if we want to return something like array. For returning an object then wrap each into map. We need to use return in map otherwise we will get an array of undefined.

- Function expression also called functions on the fly, also it gets builds only when we call that function. A variable that holds a function can be passed into other functions. Function expression can give flexibility in choosing which functionality to build. Function expression are never hoisted, they are treated as assignments.

- Using inheritance, we can create new objects with our existing objects as prototypes

- hasOwnProperty() methods helps identify property location, searching prototype chains for potential overridden properties becomes easy with this function, it helps us in finding the owner of a particular property. Use `__proto__` to move up the prototype chain to find that property.

- Pure Functions - List transformation (map), list exclusion (filter), list composition (reduce), list iteration (forEach).

- An impure function is a function that produces side-effects, it changes the state of the programs by indirect means. The console.log() is also side-effect, or a function is returning value on each time. Below is the example of impure function. We should not leave something impure publicly exposed. To make a impure function pure, we should wrap a another function on it to contain all of those side effects within that function and from outside world that function itself the outer function becomes pure, it has be pure on highest most level not all the deep nested level. Impure functions make the code harder to reason about

- A pure function is a function that has no side-effects, it operates entirely on its own variables, its own state or any of the things that are passed into it like arguments. It can access the outside variables but don't change them.

- Composition is about taking the output of one function and putting it directly in as the input to another function. So, instead of calling the once function and then calling another function, we are going to call one function, and its output is going to become at least part of the input for another function and then the output of that could become part of the input for another function.

- To make overloading work in javascript, instead of creating different methods, we should handle it manually in same method by taking consideration of arguments length or types

- The call() and apply() methods allows us to call a function and change the 'this' value, but sometimes we need to make a copy of the function and also change the this value, we can do this by 'bind()' method.

- Value of 'this' in function for different cases invocation. We need to use call, bind or prototype to control this context –

  ![typescript-value-of-this-based-on-context](./images/typescript-value-of-this-based-on-context.png)

  ![typescript-value-of-this-based-on-context2](./images/typescript-value-of-this-based-on-context2.png)

- A common approach to encapsulation in JS is using a constructor function. But adding functions to prototype required quite a bit coding and some repetition. Using class we can write it into much simpler way. The class syntax is not introducing a new object model to javascript. It is just syntactical sugar over the existing prototype-based inheritance.

- The exponentiation operator can be use by `**`, earlier we used to use Math.pow() method.

- Functional programming has main terms like pure functions, higher order functions, immutability, and side effects.

- Pure functions – similar to math functions, they don't depend on data other than what is passed in, and don't alter data other than what they returned, but math.random() is not a pure function.

- In JS constructor functions are used to create new objects. When we use the new keyword the function gets a branch new empty context, here we store the properties and functions for this object on 'this'. By using prototype property we can create a function directly on function without having duplicate copies on every object. Prototype also helps us to extend an objects to add new functionalities to the instance of that object. Polyfills also uses prototypes for their working.

- By using eval() keyword, it will open our application for injection attacks. Like the string is coming from database or web api which might be compromised, then eval will execute then string as a javascript script.

- Key terms of functional programming – pure functions, composition, higher order functions, currying, immutable data, closure. We can use libraries like – immutable.js, ramda, folktale, skit, sanctuary, monet.

- The console.log() is not pure function as it change the state of console. We should never return null or undefined from a pure function.

- Higher order functions – a function which takes a function as a parameter or return a function as a value.

- Currying function – the process of taking a function with multiple arguments and turning into multiple arguments and turning into multiple functions that take a single argument is called currying. It is named after Haskell Curry who is a mathematician. By normalizing all functions to take only one argument, it made a lot of operations easier to think about.

- Currying is the act of taking a function which accepts 1 to n parameters, and producing a collection of 1 to n function, which each take 1 parameter.

- The Date function is based on Java's Date class and due to this it was no Y2K ready.

- The big advantage in prototypal systems is we eliminate or reduce coupling between classes unlike classification inheritance.

- Generators enabled the functionality for async-await keywords because of pause-resume feature. Generator functions can be paused and resumed unlike normal functions. They also stored the state of the function while paused. They return generators object which implement the iterator protocol by this they provide a method name 'next()', this method restarts a paused generator function. They works upon concept of lazy execution by which they compute the values on demand.

- Instead of using console.log() use debug(), it will only log when we are running in development mode not in production mode.

## Object

- By using Object.assign, the source object remain unchanged, the target object is modified and used as return value. In case of duplicate properties on source objects, the value from the last object on the chain always prevails.

- Iterables return an iterator object. This object knows how to access items from a collection 1 at a time, while keeping track of its current position within the same sequence.

  ![typescript-iterables](./images/typescript-iterables.png)

- Proxies and reflection are both forms of meta programming generally to know information about itself or for a program to control how is executing while it is executing other programs. Reflection is getting information about the program and proxy is changing how the program execute during execution. Proxy object sits between other code and target object. Proxies are slower than regular object. Revocable proxies allow the system to recover resources – use in very large applications with lots of data.

  ![typescript-proxy-and-reflection](./images/typescript-proxy-and-reflection.png)

- Other OO programming language has inheritance is classical where objects are instance of classes and classes inherit from other classes, but in JS it is based on prototypes where objects inherit from objects and that's it. There are no classes, this idea it got from Self language.

- Immutability helps in performance, if we have an object that needs to be change the value stored in one of its properties, it may take a long time for JS to recognize that that properties has been changed, basically every property on that object has to be checked to see if its changed in order to determine that our data has changed. By enforcing immutability all JS has to do is check the object reference to see if that's changed. If it has changed then that some property value is changed, checking for object reference changes in very fast. So in this case immutability is performance enhancer. It is mainly for objects/arrays other data types are already immutable.

- The 'new' keyword – this is the fourth rule – when we put new keyword in front of any function call, it magical turns that function call into what we might call a constructor call. It will do four things, a brand new empty object will be created, this new object will get linked to a different object, this new object also gets bound as the this keyword for the purposes of that function call, and if that function doesn't return anything then it will return "this", so this new object will be return for us. Below code will print undefined undefined

- The 'this' keyword refers to an object. That object is whatever object is executing the current bit of code. By default it is global object in browser it is window object. The new keyword creates a new empty JavaScript object, sets the context of 'this' to that new object and then calls the function. So if we do not use 'new' keyword it will be undefined, because that function does not return anything. Object literal and object constructor are syntactic sugar for object.create() function.

- Even if the property is marked for the writable as false, we can change the value of a property of the object that name property was pointing to. But we cannot change the value if it is not pointing to an object. We can prevent the object from being changed by using object.freeze() method

- If we set the configurable as false then we cannot change the attribute of that object except the writable attribute, also we cannot delete the property.

- The alternate name for `__proto__` is dunder proto. It is a getter function, which is actually resides only at main object prototype object. This getter function returns the internal prototype linkage. IE11 above supports it, we can use Object.getPrototypeOf() function in IE9.

- Prototype linkages – it will go one level up to the prototype if that property / function doesn't get found on the current instance. If we have same property on the object same as prototype then object property will over shadow the prototype ones. Need to use foo.prototype.identify.

- A prototype is an object that exists on every function in JavaScript. Initially it is just empty object for new created function. New object do not have prototype property but `__proto__`. If current object do not have required asked property then JavaScript will search in its prototype. Functions also behave in the same way because functions are also a property in JavaScript. Object prototype is null.

- Prototype – every single "object" is built by a constructor function. Each time a constructor is called, a new object is created. A constructor makes an object linked to its own prototype. [[prototype]] are called internal linkage with its constructor call function's prototype.

- Object.freeze utility, it reaches into an object and at a shallow level i.e. is the top level of all of its properties, it makes all of those read-only. So, it will only do shallow immutability. Changing of binding is not that much of problem, but changing the values underneath us. Because bindings are always localized, they are always within the program that we can see immediately in front of us. But values are portable and can be shipped elsewhere, and over there somebody can change that value, this is much bigger problem. It helps in a situation where you give someone an object in function parameter and they modified it and misunderstood as they are using a local copy of it. Arrays are also passed by reference. Browser consoles don't work like real JavaScript environments.

- By using Object.values we can get the values of all keys, it is the same way in which we get all the keys from Object.keys method. By using Object.entries we can get both the keys and values in one go, it produces array of arrays.

- By using Object.create(null) we can create an object that inherits nothing, not even from object.prototype. It will act much more like hash table.

- Everything in JS are objects like from number, Boolean, string, array, date, regexp, function, etc. In JS there is only one number type, no integer types, it is based on 64-bit binary floating point which is also call double based on IEEE-754. But binary floating point and a binary floating point cannot accurately represent most of the decimal fractions. It can only approximate them, but it approximates them with infinite repeating bit patterns.

- In JS all values are objects, except null and undefined, they are bottom values in JS. So, we should only choose one bottom values that is undefined.

- The Object.create() is a primitive which makes a new object that inherits from another object. It gives us a direct way of doing prototypal inheritance.

- Meta object API – a property is a named collection of attributes, earlier this api wasn't exposed for outside world.

  ![typescript-meta-object-api](./images/typescript-meta-object-api.png)

- We can stop object extensibility by using preventExtensions() method, the object won't accept new property assignment. The freeze() stop its extension and also make all property as read-only and immutable. By this we can pass this object to third party and be confident that third party can't be able to corrupt this object

- Object.toString() doesn't show you anything about what it is in the object so it is useless, so we need to use JSON.stringify()

- We have two distinct kind of objects, we have objects which just contain data, only data, and objects contain only functions, which are frozen, and those objects are very strong and very reliable, they cannot be tempered with, they provide the interface for dealing with the objects which are containing the data. By this we can create good API which can defend themselves, which can remain robust in the face of all the confusion happening inside our system. So, in above image put data in member variables.

## Loops

- The for and for-of are the constructs of the language itself, whereas the for-each is the method on the array, map and set objects and can access it on the interables.

- The for-each loop skips absent values for absent value which got created while doing like below, these are not undefined or null values. The array will be called Sparse Array.

- With for or for-each loops, we can' use the "continue" or "break" keywords. For this, we should use "filter()" method then further chain the "forEach()" method. To convert and transform a value, we need to use the map() method.

- The for-in loop produces indices instead of values unlike for-of loop. The for-in loop present from the start of the language but for-of has been introduced in ES6 version.

- Also, with for-in loop the order of the iteration is not guaranteed also it will enumerated the inherited properties. We should not use for-in loop to iterate arrays or other iterables but use for-of loop. We should use for-in only to iterate the properties on a object, with for-of we will get an error that object is not iterable. To still make the use of for-of we can use Object.entries() or Object.keys() methods to iterate. So, we should use for-in only if we also want to iterate the inherited properties.

- The for-in loop can be used to loop through the property on an object. If we set enumerable false we cannot loop through that property. Also that property will not be JSON serialized.

- The for-of loop iterates over property values, and it is a better way to loop over arrays and other iterable objects.

- The for-of statement cannot be used to iterate over properties in plan JS object out of the box. In order to work with for-of, objects need a special function assigned to the Symbol.Iterator property. The presence of this property allows us to know whether an object is iterable

## Patterns

- The jQuery is the best example of Facade pattern on over complicated object interface like DOM. It provides common vocabulary while discussing the problem.

- Types of patterns

  - Creational – deals with creation of new objects. Example – constructor, module, factory, singleton
  - Structural – making up the actual objects themselves. Example - decorator, facade, flyweight
  - Behavioral – how objects are relates to each other and operates. Example – command, mediator and observer.

- Facade pattern – it is used to provide a simplified interface to a complicated system. It is like seeing a building from outside, which looks very clean but inside there might be chaos. So, it hides the chaos form us. It is different from decorator, as we are not adding any functionality to it.

- Observer Pattern – it allows a collection of objects to watch an object and be notified of changes. It allows for loosely coupled system. One object is the focal point and group of objects watch for changes. There are three vocabulary subject, notification and observers. Subject has ObserverList {} and Notify () function.

- Flyweight pattern – conserves memory by sharing portions of an object between objects. Like I have created 5000 tasks and for the name property the data will be the same and repeated. Flyweight shares data across objects. So, my name string will be shared among other object data. It is like creating prototype instead of creating function on an object for reuse. It is only useful if it has large numbers of objects.

- Mediator pattern – it controls communication between objects so neither object has been to be coupled to the others. It allows loosely couple system. One object manages all communication. It allows many too many relationships.

- Command pattern – encapsulates the calling of a method as an object as it is own individual thing. By this it allows fully decouples the execution from the implementation. Allows for less fragile implementations. It also allows undo operations. Supports audition and logging of operations. It is like USB which provides a generic interface for implementation.

- Module pattern – this is useful ness of closure mechanism. Classic module pattern has two characteristics, first there must be wrapping function that's gets executed, secondly there must be one or more functions that get returned from that function call, so one or more inner function that have colure over the inner private scope. So by this it can access the internal state that makes it a module. It implements encapsulation and principle of least exposure. It is like a module factory.

- Module Pattern - This is the pattern Douglas Crockford came up initially. The main pros is that it expose only public members which hiding private members. So, unlike prototype pattern we can define variables or functions as public or private. Main con is that function will get duplicated because we are not using prototype, also it is very hard to extend, so we want to create a library that can be extend by consumer then this is not a good pattern, we should choose prototype pattern in this case.

- Revealing Prototype Pattern - It combines prototype and revealing module pattern to get the best from both of them. Functions loaded into memory once, also it is extensible.

- Solid Principles - It is an acronym for five design principles aimed at enhancing the understanding, development, and maintenance of software. By applying this set of principles, you should notice a reduction in bugs, improved code quality, the production of more organized code, decreased coupling, enhanced refactoring, and encouragement of code reuse.

- Single Responsibility Principle - one class should have one, and only one, reason to change. It also avoids Lack of cohesion, Too much information in one place, Challenges in implementing automated tests as it's hard to mock such a class. ou can (and should) apply it to methods and functions as well.

  ```typescript
  class AuthenticationManager {
    authenticateUser(username: string, password: string): boolean {
      // Authenticate logic
    }
  }

  class UserProfileManager {
    showUserProfile(username: string): UserProfile {
      // Show user profile logic
    }

    updateUserProfile(username: string): UserProfile {
      // Update user profile logic
    }
  }

  class PermissionManager {
    setUserPermissions(username: string): void {
      // Set permission logic
    }
  }

  // ❌
  function processTasks(taskList: Task[]): void {
    taskList.forEach((task) => {
      // Processing logic involving multiple responsibilities
      updateTaskStatus(task);
      displayTaskDetails(task);
      validateTaskCompletion(task);
      verifyTaskExistence(task);
    });
  }

  // ✅
  function updateTaskStatus(task: Task): Task {
    // Logic for updating task status
    return { ...task, completed: true };
  }

  function displayTaskDetails(task: Task): void {
    // Logic for displaying task details
    console.log(`Task ID: ${task.id}, Description: ${task.description}`);
  }

  function validateTaskCompletion(task: Task): boolean {
    // Logic for validating task completion
    return task.completed;
  }

  function verifyTaskExistence(task: Task): boolean {
    // Logic for verifying task existence
    return tasks.some((t) => t.id === task.id);
  }
  ```

  ![typescript-single-responsiblity](./images/typescript-single-responsiblity.avif)

- Open Closed Principle - Objects or entities should be open for extension but closed for modification. Modifying an existing class to add new behavior carries a serious risk of introducing bugs into something that was already working. Open for extension: You can add new functionality or behavior to the class without changing its source code. Closed for modification: If your class already has a functionality or behavior that works fine, don't change its source code to add something new.

  ```typescript
  interface Shape {
    area(): number;
  }

  class Circle implements Shape {
    radius: number;

    constructor(radius: number) {
      this.radius = radius;
    }

    area(): number {
      return Math.PI * this.radius ** 2;
    }
  }

  class Square implements Shape {
    sideLength: number;

    constructor(sideLength: number) {
      this.sideLength = sideLength;
    }

    area(): number {
      return this.sideLength ** 2;
    }
  }

  class AreaCalculator {
    totalArea(shapes: Shape[]): number {
      let total = 0;

      shapes.forEach((shape) => {
        total += shape.area();
      });

      return total;
    }
  }
  ```

  ![typescript-open-closed](./images/typescript-open-closed.avif)

- Liskov Substitution Principle - A derived class must be substitutable for its base class. If S is a subtype of T, then objects of type T in a program can be replaced by objects of type S without altering the properties of this program.

  ```typescript
  class Person {
    speakName() {
      return 'I am a person!';
    }
  }

  class Child extends Person {
    speakName() {
      return 'I am a child!';
    }
  }

  const person = new Person();
  const child = new Child();

  function printName(message: string) {
    console.log(message);
  }

  printName(person.speakName()); // I am a person!
  printName(child.speakName()); // I am a child!
  ```

  ![typescript-liskov](./images/typescript-liskov.avif)

- Interface Segregation Principle - A class should not be forced to implement interfaces and methods it does not use. This way, the behavior is isolated correctly within our context, and we still respect the Interface Segregation Principle.

  ```typescript
  interface Readable {
    read(): void;
  }

  interface Downloadable {
    download(): void;
  }

  class OnlineBook implements Readable, Downloadable {
    read(): void {
      // does something
    }

    download(): void {
      // does something
    }
  }

  class PhysicalBook implements Readable {
    read(): void {
      // does something
    }
  }
  ```

  ![typescript-interface-segregation](./images/typescript-interface-segregation.avif)

- Dependency Inversion Principle - Depend on abstractions and not on implementations. High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions. In the above example, UserService directly depends on the concrete implementation of MySQLDatabase. This violates DIP since the high-level class UserService is directly dependent on a low-level class. If we want to switch to a different database system (e.g., PostgreSQL), we need to modify the UserService class, which is AWFUL! Let's fix this code using DIP. Instead of depending on concrete implementations, the high-level class UserService should depend on abstractions.

  ```typescript
  // Abstract interface (abstraction) for the low-level module
  interface Database {
    getUserData(id: number): string;
  }

  class MySQLDatabase implements Database {
    getUserData(id: number): string {
      // Logic to fetch user data from MySQL database
    }
  }

  // Another low-level module implementing the Database interface
  class PostgreSQLDatabase implements Database {
    getUserData(id: number): string {
      // Logic to fetch user data from PostgreSQL database
    }
  }

  class UserService {
    private database: Database;

    constructor(database: Database) {
      this.database = database;
    }

    getUser(id: number): string {
      return this.database.getUserData(id);
    }
  }
  ```

  ![typescript-dependency-inversion](./images/typescript-dependency-inversion.png)

## Async and Events

- The smallest timeout delay period will be 4 milliseconds, even 0 will be bumped to 4 milliseconds. Timers will not start until the outer most function is finished.

- Single threaded means a bank with one teller or a bar with only one bathroom. This behaviour is unlike with multithreaded environment more than one piece of code can execute at the same time.

- The event queue – if at a time only person can go to the teller, then there has to be a queue to hold the other people, this queue is a part of event loop in JS. This is where work is stored until the current operation or task is done executing.

  ![typescript-event-queue](./images/typescript-event-queue.png)

- The javascript engine will only execute one piece of JS code at a time, behind the scenes there are a pool of threads that are used for things like making web requests. This pool of threads can have multiple connections open to multiple different servers to request data for multiple different requests at the same time. This is all hidden behind the scenes, this is how we can still achieve parallelism within JS. We still have behind the scenes the ability for multithreading, it is not just applied to our JS code itself.

- So, JS supports concurrency by not blocking for I/O, the non-blocking nature of code in JS allows us to still have performant programs because we don't have to wait for results of long running operations to complete like a web requests or opening a file. It is like a person forget the ID or paperwork, then the teller can serve the next person in queue, and once that person come back then the teller can pick up where they left off.

- Run to completion – for a blocking operation it will run for completion, until that code runs completely like a 'for' loop, then only next code will rung. It is like satisfy customer before next by a teller. If we need to avoid this then we need to use web workers, it would be lot like opening up another line at the bank if somebody is taking a long time. This run to completion approach in JS is in stark contrast to multithreaded language where it is possible that a chunk of code could be pre-emptied, means essentially interrupting our code wherever it is executing, to give the thread to somebody else. It is like if a person is taking more time, then moving him back at the bottom of line and serving next customer.

- Cooperative concurrency – the person servicing the queue usually has control over the queue like the teller can eject someone from the queue, but in JavaScript that is not the case, in JS it is much more like bar/bathroom situation. The person who is using the bar has control over the rest of the line means he use read newspaper while others are waiting outside. Cooperative concurrency means customers play nice to each other. As long as our program doesn't abuse and hold up the rest of the queue, our programs will appear to have the ability to execute multiple things at the same time. So, each program should execute itself in smaller pieces of chunks.

- The JS engine and the browser tab that we are working has a separate event loop dedicated just to our application, this event loop contains a queue, inside of this queue work can be placed that will be eventually executed when whatever is running is complete. In addition to this queue, there is a call stack it contains whatever is executing at this current time, a call stack is like a todo list while performing a task. Work will be pushed on call stack and then once it is done it will vanish. A todo item can also have sub-task like to create a hamburger we might need to find many items to look for same with the work, it will be further pushed to the stack only, as usual after completion of that subtask, it will be removed from the stack and controls get back to the earlier item on the stack.

  ![typescript-event-loop2](./images/typescript-event-loop2.png)

- The black box items will be handle by browser behind the scenes for us, and a mechanism in browser will also listen for the their responses as-well, after getting the response it will push those response inside the queue. Behind the scene the browser is handling these requests not the JS engine, so that multiple threads handling multiple request at the same time. So it is possible while our single-threaded JS engine is doing work that behind the scenes other things can be happening, we just don't have those things happening inside of our JS engine –

  ![typescript-event-loop3](./images/typescript-event-loop3.png)

- In setTimeout() function there is not guarantee that our function will be called at exactly at the mentioned time, at that time elapse the function will be pushed in the queue, but it will called once all other prior work in the queue gets completed. Also when we say 0 milliseconds the browser is putting in as 4.

- In the browser the call stack pane is real life stack of JS event queue.

- The process.nextTick take precedence over setTimeout. In nextTick() all the callbacks that we register will be run at the end of the current event loop turn. Means whatever is running right now once it is done, the registered nextTick() will be called. nextTick() is like a bouncer that lets people cut in line, lets the VIP people get in ahead of everybody else.

- If you call setTimeOut with 0ms and resolve a promise immediately, which would console log first? The answer is Promises and the reason is that Job queue gets more priority than Event Queue.

- For callbacks, use arrow function instead of normal function.

- Promises are invented for JS for single threaded environment.

- The setImmediate will take preference over setTimeout. So, use setImmediate if we want to execute it on next tick of the event loop, node has similar api called process.nextTick.

- Async-await let us write the asynchronous code more like the way we write the synchronous code. Data returned from async func is automatically wrapped in a promise. Using the await keyword will automatically extract data from a promise. Also, we need to use try-catch while using async-await because await will only return value when it gets success result.

- We can write event-driven code with EventEmitters classes. The EventEmitter calls all listeners synchronously in the order in which they were registered. This ensures the proper sequencing of events and helps to avoid race conditions and logic errors. But we can made them async for a particular case by using setImmediate(), it will push the code execution into the next cycle of the event loop.

- Promises – much cleaner code than callbacks. Simple API – then and catch methods, chain together as then function also returns promise.

- Promises are like pub/sub but more designed for asynchronous operations.

- The promise returns just a subset of the deferred that let us attach handlers like we have been doing, but doesn't allow the state of the deferred to be changed by us.

- Asynquence – promise are very low level implementation, in future we use a abstraction on it, to have more complex flow control. Asynquence and queue are some of the third party abstraction library. It creates automatically chain promise for us.

- A deferred object is really just a wrapper that can be placed around asynchronous processing. Instead of trying to manage multiple success and failure callbacks for a series of async calls, the deferred object can wrap them all together in to a single process that will work regardless of the sequence. Once a deferred is rejected or resolved, it cannot change state again. The jQuery deferred object can only have one failure as soon as that happened, all subsequent failures were ignored.

## Events

- Event handlers are not supposed to return any value at all. But if we return false it will tell browser to stop any subsequent processing associated with that event. But we should use a JavaScript function by name preventDefault() to cancel and event because all browser do not support to cancel the event if we return as false. Example scenario if we apply double click event on div which contains text then it will by default also select the text.

- Event listeners are synchronous like below – it is because to avoid race condition which happens with the order of operations in the queue with async requests. Then if the data coming from events are not in sync order then it could jumble up the form or operation, and the order of the events won't be persevered. But there would be asynchronicity between an event and another event of the same type being raised.

- Event driven model was inspired by HyperCard

  ![typescript-hyper-card](./images/typescript-hyper-card.png)

## jQuery

- jQuery has two methods for this stopPropagation() and stopImmediatePropagation(). And also preventDefault().

## Hoisting

- Hoisting is JavaScript's default behavior of moving all declarations to the top of the current scope.

- Hoisting – there is no such thing hoisting in JavaScript specification. It is a mental construct that we have invented to explain the behaviors of JavaScript. The variable declaration will moved top of the code. Functions will also work in same way, function declaration will get hoisted, but function declaration will not get hoisted.

- Temporal dead zone: if we try to reference the variable before it has been declared with a let, it is a reference error.

- Let keyword will implicitly hijack the scope of whichever block we happened to be in, and will add that variable to that block, rather than attaching it to that function. So, like in below it will attach the baz variable to "if" statement block, not with the function level scope, i.e. with the two pairs of curly braces. This also has performance benefits as value of variable will be garbage collected earlier. Let keyword doesn't get hoist.

## Symbols

- Symbols is a concept in ES6 to provide some unique string. It is a unique and immutable data type and may be used as an identifier for object properties. There is no way to access its unique ID value. Well-known symbols used in meta programming, meta programming involves looking more deeply in objects or functions even how JavaScript operates.

## Maps and Sets

- Map and Weak Map – ES5 to create map like functionality we use object with key and value pair. But we cannot make key as an object, that's why map is created in ES6. And weak map let that object to be garbage collected it is no longer referenced.

- Set and Weak set – they are similar to map but deals with single value or single object. There is no mapping from key to value as in map. The purpose of set is to guarantee of uniqueness of its item. It will simply ignore the duplicate object.

- We should use map if keys are unknown until runtime, if keys are predefined then we can use normal javascript object as a map

- Issues with using Objects as Maps – when using objects as maps, its key are always converted to strings. We should stop using the object, but use Map objects which is a simple key/value data structure. Any value may be used as either a key or a value, and the objects are not converted to strings. Also, we can use maps when keys are unknown until runtime, use objects if keys are predefined. We should also use maps when keys are of same type and all values are of same type. Maps are iterable, so they can be used in a for-of loop. Each run of the loops returns a [key, value] pair for an entry in the Map.

  ![typescript-using-maps-instead-of-objects](./images/typescript-using-maps-instead-of-objects.png)

- The WeakMap is a type of Map where only objects can be passed as keys, primitive data types such as strings, numbers, Booleans, etc. are not allowed. WeekMaps are not iterable, so they can't be used with for-of loop. Weakmaps are better with memory, they can be garbage collected. Individual entries in a weakmap can be garbage collected, while the weakmap itself still exists.

- Limitations with arrays, they don't enforce uniqueness of items, duplicate entries are allowed. But the set object stores unique values of any type, whether primitive values or object references, it will ignore the duplicate entries. Sets objects are iterable so we can use them for-of and destructuring.

- Weaksets is a type of set where only objects are allowed to be stored. But we cannot use for-of loop with them. Good use case of weaksets, we want to add a different background color to posts that have not yet been read. One way to 'tag' unread posts is to change a property on each post objects once they are read, but we can use weaksets to create special groups from existing objects without mutating them. Favouring immutable objects allows for much simpler code with no unexpected side effects.

## Recursion

- Mutual recursion refers to two or more functions calling each other until a some terminating condition. To support mutual recursion hoisting feature is required, as one of the function will be declared too late. Interpreted language couldn't handle this mutual recursion. It is like manually hoisting the head files in C language.

- Recursion – it means a function that we define, it is going to perform some action and we want for that function to stop calling itself, it is going to call itself as a part of solution, but we want for it to stop calling itself when it reaches what we call it as a base case. Mutual recursion is two or more functions calling each other until they reach a base case. But recursion is not good for memory, when one function calls another function, even if that function is itself, the first function call allocates in memory what we call a stack frame. Stack frame is a place in memory where all the variables and state are held, and program counter as its walking through. When it finishes with that stack frame, it throws stack frame away means on finishing of that function, it throws away that memory and reclaims it and reuses it. In earlier IE the limitation of call stack was 13 deep only, but for now for modern browser it is more than 10K. It is worst for memory if device ran out of memory it will restart the device i.e. worst UX. In new browser engine there is new thing TCO (tail calls optimization), and if we done the recursion with proper tail calls, then we can do arbitrary deep recursion with O (1) memory (constant memory) usage. Virtually all recursion can be rewritten to use proper tail calls, but that technique is difficult.

- In ES6 there is proper tail calls, so the compiler will turn that into a jump instead of a call return. It will go a little faster, take less memory in getting there. It enables continuation passing style, by this JS become finally become the real functional programming language.

- Retursion - it is when we have a function that returns itself. In recursion a function calls itself.

- Recursion example of conversion of normal function into recursion, anything we can write recursively, we can also write iteratively. The recursive version is smaller, more elegant but one danger is that they are building up one after another on the stack, we can run out of memory if we put a very large number, but with modern computers, that is not much a problem.

## Closure

- Closures are very useful in creating function ‘construction zones’, a closure can make the creation of very similar functions ultra-efficient. We should aware that bound variables won’t be evident in the stored function, examining the contents of our new variables doesn’t reveal closures. Closure functions can even modify bound variable in the background.

- A closure wraps up an entire environment, binding necessary variable from other scope. It is unlike a function's local variables as they aren't available once the function's scope is closed. Closures are very useful in creating function 'construction zones', a closure can make the creation of very similar functions ultra-efficient. We should aware that bound variables won't be evident in the stored function, examining the contents of our new variables doesn't reveal closures.

  ![typescript-closure](./images/typescript-closure.png)

- Closure – function is called in the scope in which it was declared, not in the scope in which it is invoked. The way closure works is that a function is going to scope its variable at the time it is declared, not at the time it is run.

- Closure is a mathematical concepts, it comes from lambda calculus, it is when a function 'remembers' its lexical scope even when the function is executed outside that lexical scope. That lexical scope stayed attached to that function, no matter where he got transported.

- Closure is a necessary mechanism for a language with first-class function as values to be useful. If functions could be passed around with their values, but they couldn't remember anything about their lexical scope then nobody would pass functions around. Closure gets created when inner function is transported outside of the outer function.

- Closure is when a function "remembers" the variables around it even when that function is executed elsewhere.

- Closure are good parts of JS. Closure – the context of an inner function includes the scope of the outer function. An inner function enjoys that context even after the parent functions have returned. Function scope works like a block scope. To the value of a retain while executing the inner function for this the solution was don't allocate the activation records on the stack, allocate them on the heap, get a good garbage collection. JS was the first language to bring this concept then python, ruby, C#, C++, then java followed it

## Modules

- Module formats – es2015 syntax is in-built one which TypeScript adapted from JavaScript. Earlier ones were CommonJS, AMD (for browser), UMD, System JS formats.

- UMD module format – at runtime scripts in the UMD format check for global variables that are distinctive between AMD and CommonJS and depending upon which globals are found the module will be initialized in the appropriate manner. If we writing a module that is appropriate to use in both CommonJS and AMD environments we can consider using the UMD format.

- Ambient modules – large JS libraries could potentially have lots of modules in them. Each module in a large library would have its own d.ts file and that would quickly become unwieldy and inconvenient. The solution is to declare ambient modules inside a single d.ts file. Ambient modules don't provide any implementation details. In type definition files they are just the wrapper aournd an implementing that defined in the actual library. Since there aren't any top-level exports, it can't be imported directly. We first need to add a triple slash reference to the d.ts file, then we can write the import statement, we don't need to define the path for the module to import but just the name of the module in the double quote exactly it was defined in d.ts file.

  ![typescript-ambient-modules](./images/typescript-ambient-modules.png)

- Module loaders – Node has inbuilt module loaders capability means it understands the Common JS format and how to retrieve all of the necessary dependencies when running code written in or compiled to that format. As of now browsers don't provide that capability natively. However, there are couple of very good libraries that give us the ability to load and use modules in browser apps like Require.js, it understands AMD format, System JS understands AMD, Common JS, ES2015 and its own system format.

- Default Exports – they are useful when we only want to export one item from a module. Once we have specified that item as the default export, other modules can import it without even knowing its name. assigning a name to a default export is optional since the importing module doesn't need to know its name.

- Modules - By this we can have separation in our code, we are able to separate out in different units of work that we have in different module like one for Animation, UI integration, Data Access. It improves testability, reusability and maintainability.

- Creating an internal module – if we don't wrap our class in module keyword then that class name will be added to global namespace on widow object. It is an internal module that gets added and extended to the global namespace.

- There is different module syntax like AMD, Common JS, TS has adapted ES2015 module syntax by default. Benefits – encapsulation, reusability, create higher-level abstraction. We will also need module loader/bundler to run our code. Webpack will prepare our modules to execute in a browser as part of a build step.

  ![typescript-supported-technologies](./images/typescript-supported-technologies.png)

- Relative vs. non-relative imports – './', '/', '../' all are same for current directive. We should give relative reference when giving our own modules and non-relative paths when referring third party modules.

- Module formats are just a syntax which is used to define a module, module loaders are generally JS library which we can include in our project that understand the module format we have decided to use and how to load and execute the modules we define in that format. This relationship is similar to JS and browser and itself.

  ![typescript-module-type-format](./images/typescript-module-type-format.png)

- Common JS format is used mostly with server side, Universal module definition (UMD) is a single format that attempts to be compatible with both the AMD and Common JS formats. We might consider using this format if we need to same module on the server in a node application and as part of a browser application. It would be supported by the CommonJS module loader in Node, as well as an AMD loader in the browser like RequireJS.

- Module formats – non-native – AMD, common js, UMD, system.register. Native format – ES2015.

- Module loaders – for different types of module formats we need different module loaders. AMD for require JS, for AMD, common JS, UMD and system.register we need SystemJS.

- The AMD format gives us all of the encapsulation benefits with private members and a clean public API we got with the revealing module pattern but it doesn't add new objects to the global scope and it does support dependency management between modules.

- Using the AMD format with RequireJS – we just need to give the main file and it will load the dependency accordingly.

- It is better to have only one function defined globally than perhaps dozens of modules, so in below unlike revealing module pattern, every module will be inside require function. The AMD module format is great option for building browser based JavaScript applications.

- Common JS format – like the require function, the exports object is a special object that a common js module loader will use when creating the structure of the module and the API it will expose to other modules in the application.

- AMD modules are the first choice for doing client-side development, because they are optimized to load modules asynchronously in a browser, common JS format is most often used in server-side code. Node js code natively uses the common js format, which makes it the perfect format to use in that environment.

- These are native modules and built-in into the language. We don't need any helper libraries or packages in order to write them, but we need to transpile them to earlier version of JS to use them in a browser as browser still don't support them largely.

- Babel – it is a transpiler, it is tool which helps bridge the gap between what is possible in the latest versions of JS and code that can actually be executed in modern browsers. Because browsers takes years to implement new features. Babel converts all of the newer ES2015 features into equivalent code in an earlier version of JavaScript.

- They can replace module loaders in a browser, as they can be used in build steps rather than run time. A bundler follows the chain of module dependencies in an application, just like a loader, but instead of downloading a dependency when it's needed, it just adds it to the bundle in the proper order. The result of the bundling process is that we are left with far fewer files that the browser has to download. Browserify and webpack are famous bundlers.

- Module formats - IIFE, Asynchronous Module Definition (AMD), CommonJS (CJS), Universal Module Definition (UMD), ES6 Modules.

- Package vs. module – a module is a single javascript file that has some reasonable functionality, a package is a directory with one or more models inside of it and package.json file which has metadata about the package. It can be from simpler like from lodash to complex one like express. While working with NPM we are working with packages, which is why it is called node package manager.

## JSON

- JSON is a subset of the object literal notation of JavaScript – JSON keys need to be double quotes and JSON strings are also need to be double quoted. But object literals are much more flexible, they can have single quote or double quoted, or keys can have without quote. There is no such thing as JSON object, JSON is a string, it is not an object but it is serialized data which comes from server which gets formed with some kind of special library.

- The reason that JSON requires quotes around its names was because of this deign problem in ES3 which got fixed in ES5 in which we can use the reserved word on property names

## Web-workers

- A web-worker is another option to run tasks in parallel in JS. They are designed for browsers. They are started by main thread and every worker gets his own isolated global environment, nothing is shared between main thread and worker thread. SharedArrayBuffer supports a scenario where many worker thread need to share same data. Normal arrays are not optimized for this kind of work, due to which ArrayBuffer and TypedArrays have been introduced, they reduces memory footprint and optimize data transfer.

## Linting

- JSLint defines a professional subset of JS, it will hurt our feelings as we get really emotional about how we write our programs.

- Switch statement is having fall-through hazards, so we should use 'break' keywords.

## Regex

- In top 15 languages, only assembly language doesn't support regular expression.

  ![typescript-regex-basic-syntax](./images/typescript-regex-basic-syntax.png)

  ![typescript-regex-short-codes](./images/typescript-regex-short-codes.png)

- RegExp are not readable and understandable easily if they are long, there is tool regulex (<http://jex.im/regulex/>) which we can use to see it in a diagrammatic form to understand it better.

- In a function object there is basically an object with two extra pointers in it, one for the pointer to the code and one for the pointer to the activation of the creating function. There will also be a link to the prototype object which is a waste because we are not going to use it. So, no much memory in these things, not a lot of work to initialize them, so it is very light weight.

## AJAX

- The Metamorphosis of AJAX - The web comes from word processing and word processing historically comes in two very distinct schools – binary proprietary and textual open. For this the first program was runoff then GML (general mark-up language then html comes from GML). The angular brackets for tabs from Brian Reid's scribe to distinguish between format and content.

## Error Handling

- Types of errors – compile time errors, runtime errors, syntax error, logic error

- Types of runtime error – SyntaxError, TypeError, ReferenceError, URIError, RangeError, EvalError, InternalError.

## Polyfills

- Polyfills handles the cross browser feature gaps. It is a technique to add missing features to older browsers, allowing them to support newer features that are only available in modern browsers. It ensures that websites can run correctly across all browsers. It also support for deprecated features on newer browsers for older applications. The famous library for polyfills is core-js which includes methods like includes(), find(), findIndex(), flatMap(), sort(), padStart(), padEnd(), assign(), entries(), sing(), trunc(), promises, etc.

## Compilers

- Modern web browsers have good support for the latest versions of JS, including features that were introduced in newer versions of the language. But we still need transpiling for few advanced language feature that are not yet supported by all modern browsers might need transpiling.

- When ES6 was released, it was not able to run directly in browsers. To run it into the browser, this process is called transpilling to convert ES6 into ES5 before getting served to browser.

- Unlike compiler transpilers transform the code of a language into another form of the same language. They are also referred to as source to source compilers. This process converts one higher level language to another higher level language.

- Declaration merging - The compiler merges two seperate declarations declared with the same same into a single definition. allowed merges - interfaces, enums, namespaces with classes/functions/enums. disallowed - classes with classes. We can use declaration merging to implement module augmentation. It is a technique that allows us to extend existing modules with new members. It is a nice way to extend modules that we might not maintain or to extend the 3rd party code that we may not be responsible for maintaining.

  ![typescript-declaration-merging](./images/typescript-declaration-merging.png)

- Babel is a second stage transpiler and provides a handy backup plan just in case Typescript doesn't transpile something as we expected.

  ![typescript-babel-working](./images/typescript-babel-working.png)

- Transpilers - Babel, TypeScript, Elm

  ![node-js-transpilers-typescript-vs-babel](./images/node-js-transpilers-typescript-vs-babel.png)

- Webpack support many module formats, code splitting, it can bundles more than just JS modules, also use loaders feature for transformation before bundling.

- Cache busting – by default we set the cache expiration to 1 year, and if JavaScript file changes then change the bundle name to force request for latest version. For this we need to hash the bundle filename, and generate that name into HTML dynamically.

- Webpack process –

  ![typescript-webpack-process](./images/typescript-webpack-process.png)

- We can use webpack web server for local development environment, it serves the bundle file in-memory which makes our debugging and application fast on localhost. It will keep all JS files into one bundle file.

- But when our application is complete we need to build it for a production environment, so we need a package file that we can send off to store on the server, we need to minimize the code for production. For production, webpack will create a dist folder and files like below, it will also have a map file, this file is useful in some tools for getting the exact line numbers, it maps the minimize code to the original code. Webpack do all of these for us. Three main files one is html, another is JS file and finally one is a map file

- The overall computer system doesn't care for the source code, but the compile or interpreter does. It only understands the binary instructions. Source code is for us to understand and for developers.

- JS is interpreted, in C# compilation includes verification of syntactically correctness of code and creating intermediate language (IL) code packages. But in JS we can use JSLint to check for correctness and minification for packaging.

## Data Structure

- Node chains –

![ds-node-chains](./images/ds-node-chains.png)

- Linked list – single chain of nodes, head pointer, tail pointer, operations – add, remove, find, enumerate.

- Doubly linked list – singly linked list works great when we need only forward access to the nodes, but for backwards compatibility as-well we need to use doubly linked list.

![ds-doubly-linked-list](./images/ds-doubly-linked-list.png)

- Stack - It is based on LIFO concept. Each pop reduces the stack depth.

- Stack using linked list – pros with linked list approach – no hard size limit, easy to implement – no bounds checking, empty list means empty stack, cons – memory allocation on push, per node memory overhead, potential performance issues.

- Stack using arrays – cons with arrays approach – over-allocation of array. While enumerating we need to iterate it backwards.

- Postfix calculator – postfix notation also known as reverse polish notation in this approach operator follows the operands by this, we can avoid the ambiguity in operation order.

![ds-postfix-calculator](./images/ds-postfix-calculator.png)

- Undo implementation using Stack – we use stack to store the changes and to reverse the changes when undo is clicked.

- Queue - It is based on FIFO concepts. We can do enqueue and dequeue operations on it.

- Queue using linked list implementation – in this we will add last and remove first, not add first and remove last due to enumeration order. Add last/remove first allow list enumeration to “just work”. Queue allows to take incoming data and store it in a way that allows us to process it later, but in the order, it showed up, which is a sort of fairness.

- Handling growth of an array – we also need to copy from 0 to head – 1 in case of non-empty values. Arrays has benefits over linked list approach like data locality and performance gains, reducing the overall number of allocations and incredibly fast enqueue and dequeue times when there isn’t an allocation being performed.

- Priority queue – highest priority items dequeued first, not first in and first out. Only enqueue operation need to be change in implementation others operations will be same.

- What is a tree – instead of a linear structure which can be traversed backward and forward, these are a hierarchical rather than a linear manner. Terms are root or head node, leaf nodes, child nodes. A node can have any number of children but only one parent. Fundamental rule for a tree structure is that there is exactly one path from the head node to any other node in the tree and likewise exactly one path from any node in the tree back to the head node, therefore there is exactly one path can be taken between any nodes in the tree.

- Binary tree – it can have most 2 child nodes called left and right children.

- Binary search tree – sorted hierarchy of data. Small values on left and larger values are on right. Left most node contains the smallest value and right most node contains the largest value.

- Finding data – searching. Data ordering requirements make the binary search tree a really efficient structure for searching for data, as we don’t need to traverse all node to search the data.

- Traversals – to enumerate in well-defined order they are pre-order, in-order and post-order. Pre-order and post-order are used in mathematical expression evaluation, and evaluation of run time behaviour in a language like compilers use trees, dependency graph for which depends upon which operation.

- Hash Tables - Hash tables are fit into the broad category of structures knows as associative arrays. Associative arrays provide the storage of key/value pairs into an array or an array like collection. But unlike an array, the index can be any comparable type not just an integer, each key is unique. The key type is mapped to an index.

- This GetIndex() method hashed the string, hashing is a process that derives a fixed size result from an arbitrary input. Any string of any length when hashed would return a fixed size i.e. 32-bit integer hash value. The features of a hashing algorithm - stable (same input generates the same output every time), uniform (hash value should be uniformly distributed through available space), efficient and secure.

- String hashing - Naive implementation - summing of the ASCII value of character.

- Handling collisions – if two distinct items have same hash value, then we have collision as items are assigned to the same index in the has table. To handle this, we can follow two strategies – open addressing (moving to next index in table), chaining (storing item in a linked list)

- Counting words – real world example of hash table. Hash table shines in a scenario where key/value pairs we are updating the values and we have a stable key.

- Sorting means arranging data in a collection based on a comparison algorithm like any object with a notion of greater-than/less-than/equality. Two general families of sorting algorithms – linear sorting, divide and conquer. Linear algorithms treat the problem of sorting as a single large operation. Divide and conquer algorithms partition the data to be sorted into smaller sets that can be independently sorted. Measuring performance – number of comparisons, swaps operations.

- Bubble sort – simplest sorting algorithm. Consist of many passes until no swaps are performed in a pass. Performance is not good O(n2), not appropriate for large unsorted data sets. But for the best-case performance is very good i.e. O(n) also for the space requirement it is good i.e. O(n) as it directly operates on the input array and it is a candidate algorithm when minimizing space is paramount.

![ds-bubble-sort1](./images/ds-bubble-sort1.png)

![ds-bubble-sort2](./images/ds-bubble-sort2.png)

- Insertion sort – sorts each item in the array as they are encountered. It uses only simple pass, everything left of the item is known to be sorted and everything to the right is unsorted. Performance and space matrixes are same as bubble sort.

![ds-insertion-sort](./images/ds-insertion-sort.png)

- Selection sort – another linear algorithm, hybrid between bubble and insertion sort. It sorts the data by finding the smallest item and swapping it into the array in the first unsorted location. Performance is similar to bubble and insertion sort. Best case performance is O(n2). It Is not appropriate for large unsorted data set. For a system where comparison is cheap and swaps are costly then we can use this algorithm.

![ds-selection-sort1](./images/ds-selection-sort1.png)

![ds-selection-sort2](./images/ds-selection-sort2.png)

- Merge sort – it is a divide and conquer algorithm. They array is recursively split in half, and splitting continues until the array is in groups of 1, it is reconstructed in the sort order. Each reconstructed array is merged with the other half. Worst, average and best cases performance is O (n log n), data splitting means that the algorithm can be made parallel, that’s why it is appropriate for large datasets. Space required is O(n), merge can be, but is often not, performed in-place. These extra allocations increase the memory footprint required to sort data.

![ds-merge-sort](./images/ds-merge-sort.png)

- Quick sort – commonly used general purpose language and also based on divide and conquer. Pick a pivot value and partition the array.

![ds-quick-sort1](./images/ds-quick-sort1.png)

![ds-quick-sort2](./images/ds-quick-sort2.png)

![ds-quick-sort3](./images/ds-quick-sort3.png)

- Worst case is O (n2) not appropriate for large pathologically sorted (inverse sorted) data sets, average case performance is O (n log n) appropriate for large data sets, best case performance is O (n log n) very good best case performance and can efficiently sort small and nearly sorted data sets, space required O (n).

- AVL Tree - Binary tree is a collection that stores data in a tree structure. AVL tree are self-balancing binary tree invented by Adelson-velsky and landis (1942). Only insertion and deletion differ in running the balance algorithm from binary tree. AVL tree new concepts are self-balancing, height, balance factor, right/left heavy. An unbalance binary tree can cause performance issues like reduce the search time; it might become a linked list as below, like loading a English dictionary –

![ds-avl-unbalance-tree](./images/ds-avl-unbalance-tree.png)

- Balanced binary tree – the tree remains balanced as nodes are inserted or deleted, height or left and right tree differ by at most 1.

![ds-balance-tree](./images/ds-balance-tree.png)

- Balancing is done using node rotation. Rotation changes the physical structure of the tree within the constraints of the binary tree, smaller values on the left and larger or equal on the right. Rotation algorithms are right rotation, left rotation, right-left rotation, left-right rotation.

- AVL tree vs. Binary tree visualization – AVL tree won’t get much height and depth unlike binary tree. For bad 100 number, the binary tree will become the linked list like linear structure. Also, it is shows the difference between balanced tree and unbalanced trees.

![ds-avl-tree-visualization](./images/ds-avl-tree-visualization.png)

![ds-binary-tree-visualization](./images/ds-binary-tree-visualization.png)

- String Searching Algorithms - API Overview – by using interface we can implement algorithms in a uniform manner and this will allow us to use them interchangeably.

- Naïve Search - We can use run the loop till the string length minus the search string length to get some optimization. This algorithm is most appropriate when the string to search and find are both small.

![ds-naive-search1](./images/ds-naive-search1.png)

![ds-naive-search2](./images/ds-naive-search2.png)

- Boyer Moore Horspool Search – it minimizes the overall cost of search by skipping as many characters as possible. This is appropriate as a general-purpose string search algorithm. It will also improve the performance if search string is longer.

![ds-boyer-moore-horspool-search.png](./images/ds-boyer-moore-horspool-search.png)

- Data structures is a way of storing data. Data structures and algorithms are heavily linked. DS typically use some sort of algorithm to perform their inner organization, and algorithms typically uses data structure to store internal states.

- Ways of measuring performance – timing with stopwatch (but it depends on hardware, programming language, environment, etc.), counting instructions executed by machine, looking at execution curve, best case, worst case, average case.

- Asymptotic performance – In Asymptotic Analysis, we evaluate the performance of an algorithm in terms of input size (we don’t measure the actual running time). We calculate, how does the time (or space) taken by an algorithm increases with the input size.

- Big Theta – it can be used to express the complexity of a program.

- Big O – worst-case complexity of the program.

- Binary search – complexity in terms of Big O

![ds-binary-search-big-o](./images/ds-binary-search-big-o.png)

- Amortized complexity – it deals with the complexity of performing the same operation multiple times for varying inputs like inserting multiple elements in a data structure.

- Priority queues – internally elements are organized in a data structure called heap, types of heaps are min heap, max heap and min-max heap, interval heap. A heap is an binary balanced tree structure where each node has at most two children, in min-heap each element is smaller than its immediate children.

- Hash table – two flavours – first is a container that store the values that are added directly, just like arrays and linked lists, this container is often called a set or a hash set. The other flavour is a container that maps a setup of keys to a set of values, this is referred to as a map or a dictionary. Search operation is much faster in hash table.

- By hash table we can quickly lookup the name of a certain user id and this makes hash tables ideal data structure for caches, fast insertion, fast lookup and fast deletion, but elements order as per we receive them can’t be possible in hash table unlike arrays.

![ds-common-big-o-examples](./images/ds-common-big-o-examples.png)

- Brute force and greedy algorithm – problem solving strategy where all possible combinations or solution candidates are tried out blindly until a solution is found is called brute force.

![ds-brute-force-combinations](./images/ds-brute-force-combinations.png)

- Greedy algorithms work smarter than brute faster, they may speed up the search for a solution, but they come with a catch of stalling at a local maximum or minimum if we search for a small solution.

![ds-greedy-algorithms](./images/ds-greedy-algorithms.png)

- Divide and conquer – key ingredient is to discover how to divide the larger, original problem into sub-problems. Once divided, each of the smaller and easier-to-understand sub-problems are solved, leaving us with sub-solutions. Finally, find a way to combine, or deduce these sub-solutions into a solution to the original and larger problem, thereby conquering it. We can also apply it recursively. Example – quicksort

![ds-quick-sort-divide-and-conquer](./images/ds-quick-sort-divide-and-conquer.png)

- Dynamic programming – this is also built on the core idea of divide and conquer. If sub problems cannot be separated but overlaps, then overlapping part would need to be solved in both sub-problems. We can cache the solved result of sub-problem. It will improve the performance.

- The 0/1 Knapsack problem – using dynamic problem we can get the performance advantages as it has lower complexity.

![ds-knapsack-problem](./images/ds-knapsack-problem.png)

- Other examples – where to put line breaks to obtain a nice and even text justification, finding shortest paths, finding difference between two files, sequence alignment, various games

![ds-knapsack-problem-other-examples.png](./images/ds-knapsack-problem-other-examples.png)

- P vs. NP – exponential functions grow much faster than polynomials. The complexity category P covers problems that can be solved in polynomial time i.e. easy problems like sorting, traversing, lists, etc. But problems in NP category are decision problems (in which answer is yes or no) verifiable in polynomial time.

![ds-p-vs-np1](./images/ds-p-vs-np1.png)

![ds-p-vs-np2](./images/ds-p-vs-np2.png)

- NP hard – at least as hard as NP complete, they don’t need to be decision problem, and they do not need to be verifiable in polynomial time like knapsack problem, halting problem, traveling salesman problem.

![ds-np-hard](./images/ds-np-hard.png)

- Heuristics and approximation algorithms – they are general techniques for dealing with computationally hard problems. Heuristics – wanted speed, trade with accuracy.

- Cuckoo hashing to create hash table – it is an open addressing scheme, inspired by cuckoo bird.

- Prefix-querying Sequences Efficiently with Tries - Tries – represent a number of strings in a single tree structure where the root node represents the enter string with no letters added yet and with each subsequent level of the tree corresponding to a pending one more letter to a string.

![ds-tries](./images/ds-tries.png)

- Radix tree – a compressed tries structure, it improves the performance. We can use it if read-only or read-mostly operations. Tries is useful for autocompletion, prefix only scenario.

![ds-radix-trees](./images/ds-radix-trees.png)

- Suffix trees also allows to search a pattern anywhere in a string.

![ds-suffix-trees](./images/ds-suffix-trees.png)

- Data structure is a method of organizing information so that the information can be stored and retrieved efficiently.

- Big O notation – computer science defines performance by something called Big O notation. It shows how the data structure will perform as the data increase.

![ds-big-o-notation](./images/ds-big-o-notation.png)

![ds-big-o-notation2](./images/ds-big-o-notation2.png)

![ds-big-o-notation3](./images/ds-big-o-notation3.png)

- One of the problems with a hash structure is when we run into collisions when putting data into the hash. Collisions slow down the performance of the hash, which kind of defeats one of the main points of using the hash. We can reduce has collisions by increasing the has capacity or improve the hashCode() method quality to improve the uniqueness of hash value.

- The binary tree doesn’t need to always have two nodes per parent. the tree additions are based on comparisons rather than keeping the tree balanced. Because the tree data is dispersed based on comparison, it makes adding and finding the data quite efficient, so don’t have to traversed all the elements like array list due to which the Big O notation would be logarithmic which is one of the best access performance we can get out of a data structure. But implementing a tree data structure is a bit of complex in code.

- Safely Using Arrays - Arrays are used in examples like storing share prices of a company in different points of time, use arrays of pixels to store and process images. Arrays properties – contiguous memory locations as it is a very cache friendly data structure, same element type cannot have mixed up type of elements in a same array, direct fast element access by index, indexes are zero-based.

- Data transfer algorithms – physical vs. internet data transfer. We should pick the constant one because at some point it will be faster than linear complexity.

![ds-physical-vs-internet-data-transfer](./images/ds-physical-vs-internet-data-transfer.png)

![ds-physical-vs-internet-data-transfer2](./images/ds-physical-vs-internet-data-transfer2.png)

- Stack overflow – if internal array to store stack values gets full, then push operation will cause it outside of stack area which is not owned by stack. In this case, we should throw an exception from code.

- Arrays vs. linked lists – memory layout – direct fast element access by index not possible in linked list we have to traverse all the elements, also it is not cache friendly as it is not having continuous memory allocations. Linked list is good for inserting new item as all don’t have to shift. So, no reallocation overhead. The nodes of the linked list are stored in sparse memory locations. They are scattered all over computer’s memory.

![ds-array-vs-linked-list](./images/ds-array-vs-linked-list.png)

- Makes it easier to inspect deeply nested objects — you can see all nested properties without manually expanding or guessing what's inside -

  ```typescript
  console.dir(obj, { depth: null });
  ```

## Problem Solving

To be created...

## Misc

- With proxy traps we can handle operations in any way we like, all above internal methods can be used for traps. To create a short-lived proxy, use revocable while creating the proxy. Proxies are slower than regular object. Revocable proxies allow the system to recover resources – use in very large applications with lots of data.

- When using the typescript types we should not use the uppercase javascript types, we should be using the typescript types i.e. lowercase versions of them – like number instead of the Number.

- The void type is not exist in JS language.

- Module formats – es2015 syntax is in-built one which TypeScript adapted from JavaScript. Earlier ones were CommonJS, AMD (for browser), UMD, System JS formats.

- In typescript, there can be only one constructor function per class unlike other languages. For different constructor parameters we need to use the optional parameters feature instead of having multiple constructors.

- The "in" operator in JavaScript validates prototype properties rather than object values. While "includes()" checks the array values directly, "in" only checks the prototype for available properties or methods. When to Use in - in is best suited for checking if a property or method exists on an object rather than its specific values. Some good uses include: Checking for object keys before accessing, Validating methods exist before calling, Iterating over all properties with a for/in loop. It's not ideal for checking array values directly. For that, use includes(), indexOf(), etc.

- ES3 new features – strict equality, switch statement, try-catch block.

- ES4 – never released as developer group never agreed on specifications.

- ES5 – use strict, various array methods, JSON support (stringify and parse methods), getters/setters

- ES6 features – arrow functions, classes, object destructuring, let & const and promises.

- Compiler convert high level human readable code into lower level machine code. Transpilers transfer the code a language into another form of the same language. Transpiler also referred to as source to source compilers. This process converts one higher level language to another higher level language.

- The core-js is poly-filling library. Some built-in functions are not included in all browsers or they take some time to implement these functions, for this we need poly-filling. It ensure websites can run correctly across all browsers. It also helps in support for deprecated features on newer browsers for older apps.

- Event bubbling vs. event capturing – we should use event bubbling for event listening not the event capturing.

- Unlike keydown, the keypress only gets fire in case of letters, digits or special characters but not for shift, ctrl, f keys or arrow keys.

- We should avoid using keypress event because of browser inconsistencies, we should use key-up event or keydown event.

- Keyboard event data – the code property contains string representation of the hardware key, key property is the one which we see on the text editor as a final representation, keyCode (deprecated) is the ascii code for the key that is pressed, we should use charCode property instead of keyCode to return Unicode value. We should prefer to use key property and in case of hardware specific key like ctrl, shift we should use code property.

- Originally there were two kinds of JS library – libraries that added a global object, e.g. jQuery, another one is libraries that extended built-in objects, e.g. Prototype. Both approaches have significant downsides as extending built-in objects in unwise in case the object changes. Global objects are convenient, but can easily be overwritten. Instead of these both approach, we should use modular-based coding which is much safer paradigm that eliminates the worst aspects of working with globals and brings many other benefits.

--------- page 28

- TypeScript - For larger codebases, or ones maintained over time (with many people working on them), TypeScript still likely delivers good returns (maintainability, avoidance of bugs, easier refactoring). But for smaller tools / experiments / prototypes, the pay-off may not justify the extra work. Also, there’s mental overhead: developers have to think about types, strictness, compile errors, etc., which sometimes distracts from iterating ideas quickly.
