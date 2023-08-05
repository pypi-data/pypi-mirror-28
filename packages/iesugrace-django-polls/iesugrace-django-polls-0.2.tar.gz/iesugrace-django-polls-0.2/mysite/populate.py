import os
import random

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'mysite.settings')
django.setup()
from polls.models import Question, Choice


def populate_question(questions):
    for q in questions:
        Question.objects.create(question_text=q)


def populate_choice(choices):
    for q in Question.objects.all():
        choice_group = choices[:3]
        choices = choices[3:]
        for c in choice_group:
            Choice.objects.create(choice_text=c, question=q)


questions = [
    """Template picks const reference over const pointer""",
    """List of tuples into a binary table?""",
    """Delegating constructor gives segmentation fault when using class field for argument""",
    """Why do the MDN docs state that the initial display value for all elements is inline? [closed]""",
    """Why does the expression (true == true == true) produce a syntax error?""",
    """“Inline” static declaration of object with initializer list""",
    """Redux State Resets On Window Reload (Client Side)""",
    """Most vexing parse with array access""",
    """How to format numbers in scientific notation with powers in superscript""",
    """How to parse complex text files using Python?""",
    """What is the best way to check if IEnumerable has a single element?""",
    """Why does this comma inside a ternary operator throw a syntax error in JavaScript?""",
    """Confused about vectors""",
    """Toggle between two stylesheets""",
    """Stream filtering for best match""",
    """How to XOR two lists in Python?""",
    """Why can C++ deduce template arguments on the right side of an assignment operator from the left side?""",
    """Merging JSON objects with same key together""",
    """Why can't I use 'as' with generic type parameter that is constrained to be an interface?",""",
    """JSON @attributes and @association levels with js and / or angularjs""",
]

choices = [
    """material achieved Education Subcategories Time""",
    """major Gentoo back Eesti The""",
    """code asymco countries developing like""",
    """macOS scale into capabilities extensive""",
    """hard evolved drives brought stability""",
    """Inc Jones reshaping asterisk brands""",
    """MediaWiki and Whether refers shell""",
    """platforms that below ubiquitous Licensee""",
    """record reputation student Sometimes title""",
    """previews Illinois collectively renamed sometimes""",
    """before embedded Popular System host""",
    """if lettering Impact capabilities GE""",
    """PDP began business active plot""",
    """compiled higher important drivers Ilokano""",
    """options number derive Hierarchy Rik""",
    """configured give adopted raised Edit""",
    """around byte watershed Chesson thought""",
    """Morabito tool worldwide well widely""",
    """expectations simple Sequent archive Research""",
    """kill References available means Appeals""",
    """Reilly top adjective Will brands""",
    """Random settlement Their lister trend""",
    """K drivers Making Ossanna about""",
    """file through source just build""",
    """beyond not final generic hierarchical""",
    """Association Licensee icon able hard""",
    """presenting Photo List Page invariables""",
    """instrumental IEEE mainframe smaller Books""",
    """Wikibook bottled idea terminals does""",
    """designed Completes phenomenon need languages""",
    """English toolkit upper does genericized""",
    """POSIX effort Computer its nine""",
    """November occasionally Elements find Open""",
    """V6 Powered stop explosion site""",
    """employees copy Labs Greg student""",
    """reputation Early healthiest tools basic""",
    """over casually mobile addition May""",
    """Ghostscript binary stream reasons Reilly""",
    """Inspur allows based certain disk""",
    """Stallman watershed backing perform basic""",
    """Manual after Shack reference USA""",
    """generation renamed in replaced no""",
    """Contributions Varies derivative Pascal below""",
    """hardware working product dates should""",
    """USA cost by inspired features""",
    """tape levels We everyone Policy""",
    """who Corporation designed as documentation""",
    """apply systemsUnix Certified Search Find""",
    """but available profit September passed""",
    """GE Interview V range combine""",
    """technology Style facilities cc organization""",
    """More cite creation Subcategories Boston""",
    """Cumming Tel cp Alfred Specification""",
    """pages share invented outside Illinois""",
    """copies We Command mid announced""",
    """mobile return contemporary since complicated""",
    """nm ShareAlike USL dependent run""",
    """coining variety Malagasy basic Latina""",
    """extensive Making agree excerpts but""",
    """events doc adapt group V7""",
]

populate_question(questions)
populate_choice(choices)
