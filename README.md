# Chord Sheet Maker

This is a basic python script to generate a pdf chord sheet from a formatted txt file.

## Input Formatting

The input chord sheet must have the special identifiers

```
title:
artist:
album: 		(optional)
key:
scan:		order of the song parts (mandatory)
part:		Intro, V1, Chorus, etc. key must match the scan (mandatory)
chord:		line for chords (mandatory)
lyric:		line for lyrics (mandatory)
```

Some examples are in the `test` folder.

## Improvement Ideas

- Generate an html page with css to enforce style, then convert html to pdf
