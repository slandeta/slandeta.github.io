# BJJ Tournament Web Application
#### Video Demo: https://www.youtube.com/watch?v=JYwpOzXkGsc
#### Description:
This project is a web application for organizing a Brazilian Jiu Jitsu tournament. It allows users to create a profile and register for a tournament, then displays all competitors, organized by age, belt rank, and weight. I was inspired to make this project over other ideas for two main reasons.

Reason one: I thoroughly enjoyed PSET 9 (finance) because it felt very powerful to be able to combine several languages to create something, in this case, a web application. As I consider where to go next in my programming journey, I wanted to practice all of these languages (HTML, CSS, Javascript, Python, and SQL).

Reason two: I am an active Brazillian Jiu Jitsu competitor and have experienced many websites as I've signed up for tournamnets. Some of the smaller tournaments struggled immensely to organize the event, starting with displaying information on their website. I figured I could probably do a better job of creating a web app that accepted user sign ups and displayed their opponents. The only thing that would need to be added if this was a real website would be a way to pay.

Other options I considered were a website for the jiu jitsu gym I train at, a website for my chorus (I am a choral director), some type of game using pygame, and a website showcasing songs I would have written (coded) in sonic pi. Ultimately, I settled on the BJJ tournament web app for, mainly, the above-mentioned reasons.

The files for this project are set up similarly to the finance pset. In the project directory, there are three other directories (flask_session, static, and templates) as well as app.py, tournament.db and this file (README.md).

The static directory contains styles.css as well as all of the pictures included in the website. I intended to make greater use of bootstrap, but, aside from the tables, ended up just writing my own, relatively simple, css instead. This is an area that I intended to spend more time on, but decided to keep it simple as the weeks went on. I got some of the basics of css down a little better, but definitely need more practice here.

The templates directory contains all of the html files that make up the website. layout.html was created first. I then used jinja to extend the layout to all the other html pages. Most of these files are fairly straight forwad. fakeio_bracket.html took the longest to figure out, as it used jinja and python to display the competitors that had registered for the tournament and were in one of the tournament SQL tables. I used the example of some of the code written for the finance pset to help me figure out how to do this. It was similar, but some key differences caused a bit of an issue for me.

app.py is the file where most of the magic happens. There are ten functions that allow users to create a profile, log in and log out, view their profile, browse for a tournament (I have only created one), sign up for the tournament, and view the competitors signed up for the tournament. The login and logout functions are very similar to the ones used in the finance pset. I chose not to make an apology function when users don't behave. Instead, I used apology.html and jinja syntax to display something different based on what the user did wrong.

Suggestions to myself for future improvements:
1- Allow users to change divisions once they've signed up for a tournament
2- Allow users to deregister for a tournament
3- Create more tournaments
4- Include a profile picture on the profile page
5- Improve the look and feel of the website with more css and javascript
6- Understand how to include a payment method if this were to be used for a real tournament

I have enjoyed CS50 immensely and look forward to continuing my programming journey with other courses and projects!