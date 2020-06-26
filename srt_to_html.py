#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
1. Make sure you have python installed https://www.python.org/downloads/ (obviously)
2. Put srt_to_html.py file in a folder with .srt files and execute it (in the terminal or by double clicking it).
3. Style your subtitles in subs.css file
4. Now you can use Yomichan on Japanese subtitles if you're downloading your anime/movies
'''

import os

srt_files = [f for f in os.listdir(".") if f.endswith('.srt')]
if len(srt_files) != 0:
    htmlDir = os.path.join(os.getcwd(), 'srt_to_html')
    if not os.path.isdir(htmlDir):
        os.mkdir(htmlDir)
        
#Scraping data from .srt files
for sf in range(0, len(srt_files)):
    with open(srt_files[sf], 'r', encoding='utf-8') as s:
        srt = s.read().splitlines()
        
    data=[]
    for (i, s) in enumerate(srt):
        text=""
        timing = False
        if(i==0):
            i+=1
            timing = True
        elif(s==""):
            i+=2
            timing = True
        if(timing):
            try:
                start = srt[i].replace(" ","").split("-->")[0][:-1].replace(",",".")
                end = srt[i].replace(" ","").split("-->")[1][:-1].replace(",",".")
                data.append({"Start": start, "End": end})
                x=1
                while(srt[i+x] != ""):
                    text+=srt[i+x]+"<br>"
                    x+=1
                data[-1].update({"Text": text})
            except IndexError:
                pass
    
#Creating .html files with imported font, Noto Sans JP - https://fonts.google.com/specimen/Noto+Sans+JP
    with open("srt_to_html\\"+srt_files[sf][:-4]+".html","w",encoding="utf-8") as html:
        html.write('''<!DOCTYPE HTML>
<html>
<head>
<link rel="stylesheet" href="subs.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400&display=swap" rel="stylesheet">
<script src="script.js" defer></script>
<meta charset="utf-8">
<meta name="author" content="shipurjan@github">
<title>'''+srt_files[sf][:-4]+'''</title>
</head>

<body>
<div class="delay">
	<input value="0" required type="number" id="delay">
	<button onclick="delay()">Delay subtitles (ms)</button>
	<button onclick="makeDefault()">Default</button>
</div>
<div class="jump">
	<input value="00:00:00.00" required type="text" id="timestamp">
	<div class=tooltip>
	<button onclick="jumpToTimestamp()">Jump to closest timestamp</button>
	<span class="tooltiptext">
	Skip to the given timestamp (or to the first one started before the given input)<br><br>
	<u>How to input the timestamp</u>
	<ol>
		<li>(HH):(M)M:(S)S.(ms)</li>
		<li>Minutes (unit: m)</li>
		<li>Seconds (unit: s, but not needed)</li>
		<li>Milliseconds (unit: ms)</li>
	</ol>
	<br>
	<u>Examples</u>
	<ol>
		<li>01:20:03.205</li>
		<li>21:30 (21 minutes, 30 seconds)</li>
		<li>29.5 (29 seconds, 500 milliseconds)</li>
		<li>601 (601 seconds -> 10 minutes, 1 second)</li>
		<li>5m 20 ms (5 minutes, 20 milliseconds)</li>
		<li>5 m 50 600 ms (5 minutes, 50 seconds, 600 milliseconds)</li>
		<li>etc...</li>
	</ol>
	Order of input must follow (m -> s -> ms) and spaces after unit don't matter. Have fun!
	</span>
	</div>
</div>
''')
        for (e, d) in enumerate(data):
            if(len(d.get("Text")) != 0):
                html.write('''<div class="wholeline">
	<div class="index">
		<a class="enumerate" id="'''+str(e+1)+'''">'''+str(e+1)+'''</a>
		<div class="time">
			<span class="start">'''+d.get("Start")+'''</span><span class="end">'''+d.get("End")+'''</span>
		</div>
	</div>
	<p class="text">'''+d.get("Text")+'''</p>
</div>
''')
        html.write('''</body>
</html>
''')

#Creating a .css file
if not os.path.isfile("srt_to_html\\subs.css"):
    with open("srt_to_html\\subs.css","w",encoding="utf-8") as css:
        css.write('''body,
html {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  background-color: #000;
  font-size: 14pt;
  color: #fff;
}

.wholeline {
  position: relative;
  background-color: RGBA(255, 255, 255, 0.03);
}


.wholeline:nth-child(2n) {
  background-color: RGBA(255, 255, 255, 0.01);
}

.text {
  font-size: 150%;
  font-family: "Noto Sans JP", sans-serif;
  font-weight: 300;
  display: inline-block;
  margin: 0;
  padding: 0 20px 20px;
}

.text:hover {
  font-weight: 400;
}

.index {
  height: 20px;
  display: flex;
  justify-content: space-between;
}

.enumerate {
  color: #333;
  user-select: none;
}

.time {
  display: table-cell;
  font-family: "Courier New";
  letter-spacing: -1.5pt;
  user-select: none;
}

.start,
.start_changed {
  background-color: RGBA(0, 255, 0, 0.05);
}

.end,
.end_changed {
  background-color: RGBA(255, 0, 0, 0.05);
  margin-left: 5px;
}

.delay,
.jump {
  display: flex;
  right: 0;
  height: 20px;
  position: fixed;
  z-index: 1;
}

.delay {
  bottom: 0;
}

.jump {
  bottom: 22px;
}

.delay input,
.jump input,
button {
  background-color: black;
  border: 1px solid grey;
  color: white;
}

.delay input:hover,
.jump input:hover,
button:hover {
  background-color: grey;
  border: 1px solid white;
  color: white;
}

.delay input:focus,
.jump input:focus,
button:active {
  background-color: black;
  border: 1px solid white;
  color: green;
}

.tooltip button {
  display: inline-block;
  vertical-align: top;
  height: 20px;
}

.tooltip .tooltiptext {
  font-size: 10pt;
  visibility: hidden;
  width: 350px;
  bottom: 120%;
  left: 40%;
  margin-left: -175px;
  background-color: rgba(80, 80, 80, 0.95);
  color: papayawhip;
  text-align: center;
  border-radius: 15px;
  padding: 5px 3px;
  position: absolute;
  z-index: 1;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}

.tooltip .tooltiptext::after {
  content: " ";
  position: absolute;
  top: 100%;
  /* At the bottom of the tooltip */
  left: 80%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: rgba(80, 80, 80, 0.95) transparent transparent transparent;
}

ol {
  color: powderblue;
  list-style: inside;
  padding-left: 5px;
  text-align: left;
}
''')

#Creating a .js file
if not os.path.isfile("srt_to_html\\script.js"):
    with open("srt_to_html\\script.js","w",encoding="utf-8") as js:
        js.write('''function makeDefault() {
  var timings = document.querySelectorAll("div.time span.start,span.end")
  document.querySelectorAll("div.time span.start_changed,span.end_changed").forEach(e => e.parentNode.removeChild(e));
  timings.forEach(e => e.style.display = "inline-block");
  document.getElementById("delay").value = 0;
}

function stringifyFromMs(ms) {
  hours = parseInt(ms / 3600000)
  minutes = parseInt((ms - hours * 3600000) / 60000)
  seconds = parseInt((ms - hours * 3600000 - minutes * 60000) / 1000)
  milliseconds = parseInt(ms - hours * 3600000 - minutes * 60000 - seconds * 1000)
  string = ("0" + hours).slice(-2) + ":" + ("0" + minutes).slice(-2) + ":" + ("0" + seconds).slice(-2) + "." + (("00" + milliseconds).slice(-3)).slice(0, -1)
  return string
}

function addZeroes(string, length) {
  while (string.length < length) {
    string += "0"
  }
  return string
}

function translateToMs(string, ms) {
  milliseconds = parseInt(addZeroes(string.split(":")[2].split(".")[1], 3))
  milliseconds += parseInt(string.split(":")[2].split(".")[0]) * 1000
  milliseconds += parseInt(string.split(":")[1]) * 60000
  milliseconds += parseInt(string.split(":")[0]) * 3600000
  milliseconds += ms
  if (milliseconds < 0) {
    milliseconds = 0
  }
  return milliseconds
}

function delay() {
  var ms = parseInt(document.getElementById("delay").value);
  document.getElementById("delay").style.backgroundColor = "black"
  if (!isNaN(ms)) {
    var timings = document.querySelectorAll("div.time span.start,span.end")
    timings.forEach(e => e.style.display = "none");
    document.querySelectorAll("div.time span.start_changed,span.end_changed").forEach(e => e.parentNode.removeChild(e));
    for (var i = 0; i < timings.length; i++) {
      var span = document.createElement("span")
      if (i % 2 == 0) {
        span.className = "start_changed"
      } else {
        span.className = "end_changed"
      }
      span.innerHTML = stringifyFromMs(translateToMs(timings[i].innerHTML, ms))
      document.getElementsByClassName("time")[Math.floor(i / 2)].appendChild(span)
    }
  } else {
    document.getElementById("delay").style.backgroundColor = "red"
  }
}

function cutInHalf(list, number) { //cut in half and return the half containing the number
  const half = Math.ceil(list.length / 2);
  const firstHalf = list.splice(0, half)
  const secondHalf = list.splice(-half)
  if (secondHalf[0] > number) {
    return firstHalf
  } else {
    return secondHalf
  }
}

function findSubtitleTimecode(list, number) { // find the last element smaller than or equal to timestampMs -> so if timestampMs = 3000200, find the last element of startTimes which is still smaller than or equal to 3000200
  var cut_list = list
  while (cut_list.length > 1) {
    cut_list = cutInHalf(cut_list, number)
  }
  return cut_list[0]
}

function jumpToTimestamp() { //the closest one that started before given timestamp (so 00:05:20.00 would return the closest one before 00:05:20.00)
  var timestamp = document.getElementById("timestamp").value;
  document.getElementById("timestamp").style.backgroundColor = "black"
  var hours = 0
  var minutes = 0
  var seconds = 0
  var milliseconds = 0
  if (/^[0-5]{0,1}[0-9]{1}\.[0-9]{1,3}$/.test(timestamp)) {
    //*1 OPTIONAL digit (0-5)+1 digit.1-3 digits*
    seconds = timestamp.split(".")[0]
    milliseconds = timestamp.split(".")[1]
  }
  if (/^[0-5]{0,1}[0-9]{1}:[0-5]{0,1}[0-9]{1}$/.test(timestamp)) {
    //*1 OPTIONAL digit (0-5)+1 digit:1 OPTIONAL digit (0-5)+1 digit*
    minutes = timestamp.split(":")[0]
    seconds = timestamp.split(":")[1]
  } else if (/^[0-9]{1,2}:[0-5]{0,1}[0-9]{1}:[0-5]{0,1}[0-9]{1}$/.test(timestamp)) {
    //*1-2 digits:1 OPTIONAL digit (0-5)+1 digit:1 OPTIONAL digit (0-5)+1 digit*
    hours = timestamp.split(":")[0]
    minutes = timestamp.split(":")[1]
    seconds = timestamp.split(":")[2]
  } else if (/^[0-5]{0,1}[0-9]{1}:[0-5]{0,1}[0-9]{1}\.[0-9]{1,3}$/.test(timestamp)) {
    //*1 OPTIONAL digit (0-5)+1 digit:1 OPTIONAL digit (0-5)+1 digit.1-3 digits*
    minutes = timestamp.split(":")[0]
    seconds = timestamp.split(":")[1].split(".")[0]
    milliseconds = timestamp.split(":")[1].split(".")[1]
  } else if (/^[0-9]{1,2}:[0-5]{0,1}[0-9]{1}:[0-5]{0,1}[0-9]{1}\.[0-9]{1,3}$/.test(timestamp)) {
    //*1-2 digits:1 OPTIONAL digit (0-5)+1 digit:1 OPTIONAL digit (0-5)+1 digit.1-3 digits*
    hours = timestamp.split(":")[0]
    minutes = timestamp.split(":")[1]
    seconds = timestamp.split(":")[2].split(".")[0]
    milliseconds = timestamp.split(":")[2].split(".")[1]
  } else if (/^[0-9]{1,}ms$/.test(timestamp) || /^[0-9]{1,} ms$/.test(timestamp)) {
    //*1-inf digits+ms or 1-inf digits+" ms"*
    milliseconds = timestamp.replace(/\D/g, "");
  } else if (/^[0-9]{1,}$/.test(timestamp) || /^[0-9]{1,}s$/.test(timestamp) || /^[0-9]{1,} s$/.test(timestamp)) {
    //*1-inf digits or 1-inf digits+s or 1-inf digits+" s"*
    seconds = timestamp.replace(/\D/g, "");
  } else if (/^[0-9]{1,}m$/.test(timestamp) || /^[0-9]{1,} m$/.test(timestamp)) {
    //*1-inf digits+m or 1-inf digits+" m"*
    minutes = timestamp.replace(/\D/g, "");
  } else if (/^[0-9]{1,} [0-9]{1,3}ms$/.test(timestamp) || /^[0-9]{1,} [0-9]{1,3} ms$/.test(timestamp) || /^[0-9]{1,}s [0-9]{1,3}ms$/.test(timestamp) || /^[0-9]{1,}s [0-9]{1,3} ms$/.test(timestamp) || /^[0-9]{1,} s [0-9]{1,3}ms$/.test(timestamp) || /^[0-9]{1,} s [0-9]{1,3} ms$/.test(timestamp)) {
    //*Seconds 1-inf digits or 1-inf digits+s or 1-inf digits+" s"* AND *Milliseconds 1-3 digits+ms or 1-3 digits+" ms"*
    timestamp = timestamp.replace(/\D/g, " ").split(" ").filter(function(el) {
      return el != "";
    });
    seconds = timestamp[0]
    milliseconds = timestamp[1]
  } else if (/^[0-9]{1,}m [0-9]{1,}ms$/.test(timestamp) || /^[0-9]{1,}m [0-9]{1,} ms$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,}ms$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,} ms$/.test(timestamp)) {
    //*Minutes 1-inf digits+m or 1-inf digits+" m"* AND *Milliseconds 1-inf digits+ms or 1-inf digits+" ms"*
    timestamp = timestamp.replace(/\D/g, " ").split(" ").filter(function(el) {
      return el != "";
    });
    minutes = timestamp[0]
    milliseconds = timestamp[1]
  } else if (/^[0-9]{1,}m [0-9]{1,}$/.test(timestamp) || /^[0-9]{1,}m [0-9]{1,}s$/.test(timestamp) || /^[0-9]{1,}m [0-9]{1,} s$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,}$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,}s$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,} s$/.test(timestamp)) {
    //*Minutes 1-inf digits+m or 1-inf digits+" m"* AND *Seconds 1-inf digits or 1-inf digits+s or 1-inf digits+" s"*
    timestamp = timestamp.replace(/\D/g, " ").split(" ").filter(function(el) {
      return el != "";
    });
    minutes = timestamp[0]
    seconds = timestamp[1]
  } else if (/^[0-9]{1,}m [0-9]{1,} [0-9]{1,}ms$/.test(timestamp) || /^[0-9]{1,}m [0-9]{1,} [0-9]{1,} ms$/.test(timestamp) || /^[0-9]{1,}m [0-9]{1,}s [0-9]{1,}ms$/.test(timestamp) || /^[0-9]{1,}m [0-9]{1,}s [0-9]{1,} ms$/.test(timestamp) || /^[0-9]{1,}m [0-9]{1,} s [0-9]{1,}ms$/.test(timestamp) || /^[0-9]{1,}m [0-9]{1,} s [0-9]{1,} ms$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,} [0-9]{1,}ms$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,} [0-9]{1,} ms$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,}s [0-9]{1,}ms$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,}s [0-9]{1,} ms$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,} s [0-9]{1,}ms$/.test(timestamp) || /^[0-9]{1,} m [0-9]{1,} s [0-9]{1,} ms$/.test(timestamp)) {
    //*Minutes 1-inf digits+m or 1-inf digits+" m"* AND Seconds *1-inf digits or 1-inf digits+s or 1-inf digits+" s"* AND Milliseconds *1-inf digits+ms or 1-inf digits+" ms"*
    timestamp = timestamp.replace(/\D/g, " ").split(" ").filter(function(el) {
      return el != "";
    });
    minutes = timestamp[0]
    seconds = timestamp[1]
    milliseconds = timestamp[2]
  } else {
    document.getElementById("timestamp").style.backgroundColor = "red"
  }
  while (milliseconds >= 1000) {
    milliseconds -= 1000
    seconds += 1
  }
  while (seconds >= 60) {
    seconds -= 60
    minutes += 1
  }
  while (minutes >= 60) {
    minutes -= 60
    hours += 1
  }
  timestamp = hours + ":" + minutes + ":" + seconds + "." + milliseconds
  timestampMs = translateToMs(timestamp, 0)
  if (document.querySelectorAll("div.time span.start_changed").length > 0) {
    var timings = document.querySelectorAll("div.time span.start_changed")
  } else {
    var timings = document.querySelectorAll("div.time span.start")
  }
  var startTimes = [];
  for (var i = 0; i < timings.length; i++)
    startTimes.push(translateToMs(timings[i].innerHTML, 0))
  subtitlesTimecode = findSubtitleTimecode(startTimes, timestampMs)
  for (var i = 0; i < timings.length; i++)
    startTimes.push(translateToMs(timings[i].innerHTML, 0))
  subtitlesIndex = startTimes.indexOf(subtitlesTimecode) + 1
  var url = location.href;
  location.href = "#" + subtitlesIndex;
  history.replaceState(null, null, url);
}
var a = document.getElementById("timestamp");
a.onkeyup = function(e) {
  if (e.keyCode == 13) {
    jumpToTimestamp();
  }
}
var b = document.getElementById("delay");
b.onkeyup = function(e) {
  if (e.keyCode == 13) {
    delay();
  }
}
''')