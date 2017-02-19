Go open when developing quirky
##############################

:tags: Free Software, Outreachy, Cornice
:date: 2017-01-25 23:15
:category: Outreachy
:author: Gabriela Surita
:slug: quirky-foss


First, I've reached the middle of my internship at Mozilla. :)

And today I'm probably gonna do a much different post than the usual,
but on the `last post <https://gabisurita.github.io/self-documented-apis.html>`_,
I've explained briefly what's
`Cornice Swagger <https://github.com/Cornices/cornice.ext.swagger/>`_,
and how it works, but I also want to talk about how was the experience
to get involved and contribute to Cornice Swagger.

If you read my last post, there's a good chance you thought that the
use case Cornice Swagger applies is very unusual, and why put effort in
developing and maintaining a package like it when the use case is so specific?
Why don't hack a much simpler solution that works for each your use case and
dedicate time improving your own software?

**Side note:** I agree that the use case is specific, but it shouldn't be.
People really should begin documenting HTTP APIs in a more intelligent and
automated way. Getting back to the post...

Well, I've considered that. When I've begin to contribute with the package,
it didn't suited many aspects of the solution I needed, and I would probably
have to rewrite a good part of the code. I discussed the changes with
my mentor and the part of the team and we were afraid that the maintainers
wouldn't be receptive to the changes we needed. But we decided to try.

I've started with a large PR changing a lot the package structure, and it was
awesome! The maintainers agreed that the package need those changes and they
were willing to change their applications to use the modified API. And
that made everyone's life better.

**Another side note:** If we want to make it popular, it's also important to make
it modular and pluggable, and that's another relevant part of doing stuff on
a separate package.

I realized that's how free and open software should work. The whole idea
is that there should be cooperation to make everyone's software better.
We have to be willing to contribute to someone else's software, as well as
accept other people changes when they make sense. I could use it for my use
case, and we all lived happily ever after...

And, well, not really. There's still
`a lot of open issues <https://github.com/Cornices/cornice.ext.swagger/issues>`_
to solve, but there's also good news. There are more people willing to use,
contribute and making breaking changes to the package like I did, and that's
my turn to be receptive and make our (and other people) software more mature.

But let's go back to work... together!

**Footnote:** I definitely should write some CSS to make side notes be side notes.
