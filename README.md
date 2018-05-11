Feeds for org mode!

# Usage

Create an org file, each top level header represents a feed, the property drawer should cointain a TYPE (rss or twitter are supported right now), and an URL.

```
#+SEQ_TODO: UNREAD(u) | READ(r)

* Nasa RSS

:PROPERTIES:
:URL: https://blogs.nasa.gov/stationreport/feed/
:TYPE: rss
:END:
```

Then run the script `python bin/refresh.py feeds.org`

A bunch of sub headers will appear under the feed:

```
** UNREAD ISS Daily Summary Report – 5/08/2018
:PROPERTIES:
:ENTRY_ID: https://blogs.nasa.gov/stationreport/?p=4202
:LINK: https://blogs.nasa.gov/stationreport/2018/05/08/iss-daily-summary-report-5082018/
:DATE: Tue, 08 May 2018 16:00:38
:END:
** UNREAD ISS Daily Summary Report – 5/04/2018
:PROPERTIES:
:ENTRY_ID: https://blogs.nasa.gov/stationreport/?p=4197
:LINK: https://blogs.nasa.gov/stationreport/2018/05/04/iss-daily-summary-report-5042018/
:DATE: Fri, 04 May 2018 16:00:28
:END:
** UNREAD ISS Daily Summary Report – 5/03/2018
:PROPERTIES:
:ENTRY_ID: https://blogs.nasa.gov/stationreport/?p=4194
:LINK: https://blogs.nasa.gov/stationreport/2018/05/03/iss-daily-summary-report-5032018/
:DATE: Thu, 03 May 2018 16:00:46
:END:
** UNREAD ISS Daily Summary Report – 5/01/2018
:PROPERTIES:
:ENTRY_ID: https://blogs.nasa.gov/stationreport/?p=4190
:LINK: https://blogs.nasa.gov/stationreport/2018/05/01/iss-daily-summary-report-5012018/
:DATE: Tue, 01 May 2018 16:00:53
:END:
** UNREAD ISS Daily Summary Report – 4/30/2018
:PROPERTIES:
:ENTRY_ID: https://blogs.nasa.gov/stationreport/?p=4187
:LINK: https://blogs.nasa.gov/stationreport/2018/04/30/iss-daily-summary-report-4302018/
:DATE: Mon, 30 Apr 2018 16:00:58
:END:
** UNREAD ISS Daily Summary Report – 4/27/2018
:PROPERTIES:
:ENTRY_ID: https://blogs.nasa.gov/stationreport/?p=4184
:LINK: https://blogs.nasa.gov/stationreport/2018/04/27/iss-daily-summary-report-4272018/
:DATE: Fri, 27 Apr 2018 16:00:34
:END:
** UNREAD ISS Daily Summary Report – 4/26/2018
:PROPERTIES:
:ENTRY_ID: https://blogs.nasa.gov/stationreport/?p=4182
:LINK: https://blogs.nasa.gov/stationreport/2018/04/26/iss-daily-summary-report-4262018/
:DATE: Thu, 26 Apr 2018 16:00:31
:END:
````
Also the flag `--mark-as-read` will tag any new entry as "NEW", and `--forget-new` will remove the "NEW" tags of existent entries.

# Emacs Setup

I recommend adding two capture commands, one for each type of feed:

- `fr` rss feed, check the template in `emacs/tpl-rssfeed`
- `ft` twitter feed, check the template in `emacs/tpl-twitterfeed`
