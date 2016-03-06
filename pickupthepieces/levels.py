# meta data for game levels
level_0 = {
    "name" : "Instructions",
        "text" : [ 
        "You are recovering from the aftermath of the blitz bombings",
        "Your precious photographs have been torn and scattered about",
        "Can you recover the pieces and reassemble the photos",
        "before the next bombing?",
        "",
        "Click on the photo pieces to move them about",
        "You can also rotate the pieces when they are clicked",
        "'A' to rotate LEFT, 'D' to rotate RIGHT",
        "or 'LEFT' to rotate LEFT, 'RIGHT' to rotate RIGHT"
    ],

}

level_1 = {
    "name" : "Level 1",
    "tutorial_text" : True,
    "rows":2,
    "cols":2,
    "max_angle" : 0,
    "max_dist" : 100,
    "text" : [ 
        "An Observer Corps spotter",
        "scans the skies of London",
        "",
        "Click to select and move the pieces",
        "",
        "Source: https://en.wikipedia.org/wiki/Battle_of_Britain,"
    ],
    "image_name" : "level-1.jpg",
    "music" : "level-1.wav",
    "time_limit" : 60  
}

level_2 = {
    "name" : "Level 2",
    "tutorial_text" : True,
    "rows":3,
    "cols":3,
    "max_angle" : 100,
    "max_dist" : 20,
    "text" : [ 
        "Many homes were destroyed during the blitz",
        "But this didn't damage the famous Dunkirk spririt",
        "",
        "Rotate the pieces into place with 'A' and 'D' or 'LEFT' and 'RIGHT'",
        "",
        "Source: http://www.historiccoventry.co.uk/blitz/next-day.php"

    ],
    "image_name" : "level-2.jpg",
    "music" : "level-2.wav",
    "time_limit" : 60  
}

level_3 = {
    "name" : "Level 3",
    "tutorial_text" : True,
    "rows":3,
    "cols":3,
    "max_angle" : 90,
    "max_dist" : 200,
    "text" : [ 
        "Queen Elizabeth, followed by the King,", 
        "inspected the wreckage of Buckingham Palace caused",
        "by the explosion of a German time bomb",
        "",
        "Source: http://flashbak.com/"
    ],
    "image_name" : "level-3.jpg",
    "music" : "level-3.wav",
    "time_limit" : 120  
}

level_4 = {
    "name" : "Level 4",
    "tutorial_text" : True,
    "rows":4,
    "cols":4,
    "max_angle" : 180,
    "max_dist" : 300,
    "text" : [ 
        "Regardless of the devastation",
        "Londoners carried on and tried to lead normal lives",
        "",
        "Source: http://www.gohistorygo.com/#!the-london-blitz-/c23cg"
    ],
    "image_name" : "level-4.jpg",
    "music" : "level-4.wav",
    "time_limit" : 120  
}

level_5 = {
    "name" : "Level 5",
    "tutorial_text" : True,
    "rows":5,
    "cols":5,
    "max_angle" : 360,
    "max_dist" : 500,
    "text" : [ 
        "Homeless family plucking a chicken..",
        "",
        "Source: http://www.unionhistory.info/timeline/Tl_Display.php?irn=169&QueryPage=..%2FAdvSearch.php"
    ],
    "image_name" : "level-5.jpg",
    "music" : "level-5.wav",
    "time_limit" : 120  
}


levels = [
    level_0,
    level_1, 
    level_2,
    level_3,
    level_4,
    level_5
]
