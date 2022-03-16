#!#!/usr/bin/env bash

open -a "qBittorrent"

#osascript -e 'tell application "Finder"' -e 'set visible of process "qBittorrent" to false' -e 'end tell'

sleep 1

osascript -e 'tell application "qBittorrent" to set visible of process "qBittorrent" to false'

# osascript <<EOF
# -- Click the “Allow” button.
# delay 1.863783
# set timeoutSeconds to 2.000000
# set uiScript to "click UI Element \"Allow\" of window 1 of application process \"UserNotificationCenter\""
# my doWithTimeout( uiScript, timeoutSeconds )
#
# on doWithTimeout(uiScript, timeoutSeconds)
# 	set endDate to (current date) + timeoutSeconds
# 	repeat
# 		try
# 			run script "tell application \"System Events\"
# " & uiScript & "
# end tell"
# 			exit repeat
# 		on error errorMessage
# 			if ((current date) > endDate) then
# 				error "Can not " & uiScript
# 			end if
# 		end try
# 	end repeat
# end doWithTimeout
# EOF
