# tv-program-polling
When run periodically, script polls the given finnish tv programs and if maches found, sends results to email.
Results include program name, channel and time when aired.

You can define searched tc program names, as well as an exclusion list; if the program name is match but is also a macth to an exclusion list item, the match is skipped. E.g. "auto" and excluded "autokoulu" -> "autoilu" is match, "autokoulu" is skipped.

you need to define your own mailgun API key and email address to the script. For now, they are just in this single .py file.
