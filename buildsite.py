#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator.

Example:

    >>> python3 buildsite.py

Author:   
    Erik Johannes Husom

Created:  
    2021-01-27

"""
import datetime
from email import utils
import html
import os
import re

import markdown as md

class Website():

    def __init__(self):

        self.baseurl = "https://erikjohannes.no/"
        self.layouts_folder = "layouts"
        self.posts_folder = "posts"
        self.pages_folder = "pages"
        self.standalone_folder = "standalone"
        self.photography_folder = "photography"
        self.photofeed_folder = "photography/photofeed"
        self.activities_folder = "activities"
        self.posts_folder = "posts"

        self.layout_filenames = ["head.html", "header.html", "footer.html"]
        self.layout_files = []
        self.img_exts = [".jpg", ".png", ".PNG", ".JPG", ".jpeg", ".JPEG"]
        self.activity_exts = [".gpx"]


        self.wide_pages = [
                "adventure.html",
                "landscape.html",
                "mans-best-friend.html",
                "plants.html",
                "wildlife.html"
        ]

        # Read the common layouts of each page
        for f in self.layout_filenames:
            with open(self.layouts_folder + "/" + f, "r") as infile:
                self.layout_files.append(infile.read())

    def combine_layouts(self, body):

        page = "<!DOCTYPE html>\n"
        page += '<html lang="en">\n'
        page += self.layout_files[0]
        page += "    <body>\n"
        page += self.layout_files[1]
        page += body
        page += self.layout_files[2]
        page += "    </body>\n"
        page += "</html>"

        return page

    def save_page(self, page, name):

        with open(name, "w") as outfile:
            outfile.write(page)

        print("Created", name)

    def build_pages(self):

        for f in os.listdir(self.pages_folder):

            # Check that the page is a .html file
            if os.path.splitext(f)[1] != ".html":
                continue

            # Read the content for this specific page
            with open(self.pages_folder + "/" + f, "r") as infile:
                body = infile.read()

            # Combine the common layouts and the page content
            page = self.combine_layouts(body)

            # Check if the page should have a wide body
            if os.path.basename(f) in self.wide_pages:
                page = page.replace("<body>", "<body class=wide>")

            self.save_page(page, f)



        for f in os.listdir(self.standalone_folder):

            # Check that the page is a .html file
            if os.path.splitext(f)[1] != ".html":
                continue

            # Read the content for this specific page
            with open(self.standalone_folder + "/" + f, "r") as infile:
                body = infile.read()

            self.save_page(body, f)


    def build_blog(self, exclude_drafts=True):

        blog_links = []
        blog_titles = []
        blog_dates = []
        blog_rfcdates = []
        blog_contents = []
        blog_image_links = []

        for f in os.listdir(self.posts_folder):
            # if os.path.isdir(f) and "index.md" in os.listdir(f):
            if os.path.isdir(self.posts_folder + "/" + f):
                if "index.md" in os.listdir(self.posts_folder + "/" + f):

                    draft = False

                    with open(self.posts_folder + "/" + f + "/" + "index.md",
                            "r") as infile:
                        lines = infile.readlines()

                    title = ""
                    date = ""

                    for line in lines:
                        if line.startswith("title:"):
                            title = line.replace("title: ", "")
                        if line.startswith("date:"):
                            date = line.replace("date: ", "")
                        if line.startswith("draft:"):
                            draft = line.replace("draft: ", "")
                            draft = draft.replace('"', "")
                            draft = draft.strip()

                    if draft == "true" and exclude_drafts:
                        continue

                    title = title.replace('"', "")
                    date = datetime.datetime.strptime(date[:10], "%Y-%m-%d")
                    rfcdate = utils.format_datetime(date)
                    print_date = datetime.datetime.strftime(date, "%d %b %Y")

                    # os.system(
                    #         "pandoc {}/{}/index.md -o {}/{}/index.html".format(
                    #             self.posts_folder, f, self.posts_folder, f
                    # ))

                    with open(f"{self.posts_folder}/{f}/index.md", "r") as infile:
                        md_version = infile.read()

                    md_post = md_version.split("---")
                    md_front_matter = md_post[1]
                    md_content = " ".join(md_post[2:])

                    html_version = md.markdown(md_content)

                    with open(f"{self.posts_folder}/{f}/index.html", "w") as outfile:
                        outfile.write(html_version)

                    
                    # body = "<h2>blog</h2>"
                    # body += "\n"
                    body = "<article>"
                    body += "\n"
                    body += "<h2>" + title + "</h2>"
                    body += "\n"
                    body += "<h3>" + print_date + "</h3>"

                    blog_link = self.posts_folder + "/" + f + "/" + "index.html"

                    with open(blog_link, "r") as infile:
                        content = infile.read()

                    content = content.replace("{{&lt; rawhtml &gt;}}", "")
                    content = content.replace("{{&lt; /rawhtml &gt;}}", "")

                    body += content

                    body += "</article>"
                    body += "\n"


                    page = self.combine_layouts(body)

                    self.save_page(page, blog_link)

                    date = datetime.datetime.strftime(date, "%Y-%m-%d")
                    blog_links.append(blog_link)
                    blog_titles.append(title)
                    blog_dates.append(date)
                    blog_rfcdates.append(rfcdate)
                    blog_contents.append(content)
                    blog_image_links.append(blog_link)

        body = "<article>"
        body += "<h2>Blog</h2>"
        body += "\n"
        body += "\n"
        body += "<ul>"
        body += "\n"

        blog_dates, blog_titles, blog_links, blog_contents, blog_rfcdates, blog_image_links = zip(
                *sorted(zip(blog_dates, blog_titles, blog_links, blog_contents,
                    blog_rfcdates, blog_image_links))
        )


        blog_dates = list(reversed(list(blog_dates)))
        blog_links = list(reversed(list(blog_links)))
        blog_titles = list(reversed(list(blog_titles)))
        blog_contents = list(reversed(list(blog_contents)))
        blog_rfcdates = list(reversed(list(blog_rfcdates)))
        blog_image_links= list(reversed(list(blog_image_links)))


        shortblogfeed = "<ul>"
        length = 5
        counter = 0

        for l, t, d in zip(blog_links, blog_titles, blog_dates):
            

            if counter < length:
                shortblogfeed += f"<li><span class=date>{d}</span><a href='{l}'>{t}</a></li>"
                counter += 1


            # d = datetime.datetime.strftime(d, "%d %b %Y")
            # d = datetime.datetime.strftime(d, "%Y-%m-%d")
            body += f"<li><span class=date>{d}</span><a href='{l}'>{t}</a></li>"
                    
        body += "</ul>"
        shortblogfeed += "</ul>"

        page = self.combine_layouts(body)
        self.save_page(page, "blog.html")

        self.blog_dates = blog_dates
        self.blog_links = blog_links
        self.blog_titles = blog_titles
        self.blog_contents = blog_contents
        self.blog_rfcdates = blog_rfcdates
        self.blog_image_links = blog_image_links


        with open("index.html", "r") as f:
            index = f.read()
            index = index.replace("<!--BLOGFEED-->", shortblogfeed)

        with open("index.html", "w") as f:
            f.write(index)
            
    def read_photo_feed(self, granularity="yearly"):

        photofeed_links = []
        photofeed_absolute_links = []
        photofeed_titles = []
        photofeed_dates = []
        photofeed_months = []
        photofeed_years = []

        for img_name in os.listdir(self.photofeed_folder):
            print(img_name)

            if not os.path.splitext(img_name)[1].lower() in self.img_exts:
                continue

            date = datetime.datetime.strptime(img_name[:10], "%Y-%m-%d")
            year_and_month = img_name[:7]
            year = img_name[:4]
            rfcdate = utils.format_datetime(date)
            print_date = datetime.datetime.strftime(date, "%d %b %Y")

            # Take the second part of filename (after the date) and
            # split at the extension. Replace dashes with space.
            title = img_name[11:].split(".")[0]
            title = title.replace("-", " ")

            if granularity == "monthly":
                link = "photofeed-" + year_and_month + ".html#" + img_name[:10]
            else:
                link = "photofeed-" + year + ".html#" + img_name[:10]
                
            image_link = self.photofeed_folder + "/" + img_name

            content = f"<img src=\"{image_link}\" alt=''/><figcaption>{title}</figcaption>"

            date = datetime.datetime.strftime(date, "%Y-%m-%d")
            self.blog_links.append(link)
            self.blog_titles.append(title)
            self.blog_dates.append(date)
            self.blog_rfcdates.append(rfcdate)
            self.blog_contents.append(content)
            self.blog_image_links.append(image_link)

            photofeed_links.append(image_link)
            photofeed_absolute_links.append(self.baseurl + link)
            photofeed_titles.append(title)
            photofeed_dates.append(date)
            photofeed_months.append(year_and_month)
            photofeed_years.append(year)


        photofeed_dates, photofeed_links, photofeed_absolute_links, photofeed_titles, photofeed_months, photofeed_years = zip(
                *sorted(zip(photofeed_dates, photofeed_links,
                    photofeed_absolute_links, photofeed_titles,
                    photofeed_months, photofeed_years))
        )

        photofeed_dates = list(reversed(list(photofeed_dates)))
        photofeed_links = list(reversed(list(photofeed_links)))
        photofeed_absolute_links = list(reversed(list(photofeed_absolute_links)))
        photofeed_titles = list(reversed(list(photofeed_titles)))
        photofeed_months = list(reversed(list(photofeed_months)))
        photofeed_years = list(reversed(list(photofeed_years)))

        self.blog_dates, self.blog_titles, self.blog_links, self.blog_contents, self.blog_rfcdates, self.blog_image_links = zip(
                *sorted(zip(self.blog_dates, self.blog_titles, self.blog_links,
                    self.blog_contents, self.blog_rfcdates,
                    self.blog_image_links))
        )


        self.blog_dates = list(reversed(list(self.blog_dates)))
        self.blog_links = list(reversed(list(self.blog_links)))
        self.blog_titles = list(reversed(list(self.blog_titles)))
        self.blog_contents = list(reversed(list(self.blog_contents)))
        self.blog_rfcdates = list(reversed(list(self.blog_rfcdates)))
        self.blog_image_links = list(reversed(list(self.blog_image_links)))

        photofeed_pages = []

        month_set = sorted(list(set(photofeed_months)))[::-1]
        year_set = sorted(list(set(photofeed_years)))[::-1]

        if granularity == "monthly":
            period_set = month_set
            photofeed_periods = photofeed_months
        else:
            period_set = year_set
            photofeed_periods = photofeed_years

        for i, period in enumerate(period_set):

            body = "<article>"
            body += f"<h2>Photofeed</h2>"
            body += "\n"
            # Add links to other years
            body += "<ul>"
            for period2 in period_set:
                if period2 == period:
                    continue
                body += f"<li><a href='photofeed-{period2}.html'>{period2}</a></li>"
            body += "</ul>"
            body += "<br/>"
            body += "\n"
            body += f"<h3>{period}</h3>"
            body += "\n"
            body += "\n"
            body += "<section class=gallerymasonry>"
            body += "\n"

            for l, a, t, d, p in zip(photofeed_links, photofeed_absolute_links, photofeed_titles,
                    photofeed_dates, photofeed_periods):

                # If image not in current period (month or year), skip it
                if p != period:
                    continue
                
                body += "<section class=galleryitem>"
                body += "\n"
                body += f"<a href=\"{l}\">"
                body += f"<img id=\"{d}\" src=\"{l}\" title=\"{t}\"/>"
                body += "</a>"
                body += "\n"
                body += f"<figcaption>{d}: {t} "
                body += f"<a href=\"{a}\" class=\"shareButton\">(shareable link)</a>"
                body += "</figcaption>"
                body += "\n"
                body += "</section>"
                body += "\n"

            body += "</section>"
            body += "\n"
            body += "</article>"
            body += "\n"

            page = self.combine_layouts(body)
            self.save_page(page, f"photofeed-{period}.html")

            if i == 0:
                self.save_page(page, f"photofeed.html")

            photofeed_pages.append([f"photofeed-{period}.html", period])
            print(period)

    def create_activity_feed(self):

        activities_links = []
        activities_absolute_links = []
        activities_images = []
        activities_titles = []
        activities_texts = []
        activities_dates = []
        activities_months = []
        activities_years = []

        gpx_filename = None

        for f in os.listdir(self.activities_folder):
            # Each activity must have its own folder
            if os.path.isdir(self.activities_folder + "/" + f):
                activity_folder = self.activities_folder + "/" + f + "/"
                gpx_filename = None
                activity_text = None
                activity_images = []
                # Find gpx file in folder
                for f2 in os.listdir(activity_folder):
                    if os.path.splitext(f2)[1].lower() in self.activity_exts:
                        gpx_filename = f2
                    # If there is a Markdown file in the folder, use the text
                    # as content.
                    if os.path.splitext(f2)[1].lower() == ".md":
                        with open(activity_folder + f2, "r") as infile:
                            activity_text = infile.read()
                            activity_text = md.markdown(activity_text)
                    if os.path.splitext(f2)[1].lower() in self.img_exts:
                        activity_images.append(activity_folder + f2)

                # If no gpx file is found, continue to next filder
                if gpx_filename == None:
                    continue

            else:
                continue

            date = datetime.datetime.strptime(gpx_filename[:10], "%Y-%m-%d")
            year_and_month = gpx_filename[:7]
            year = gpx_filename[:4]
            rfcdate = utils.format_datetime(date)
            print_date = datetime.datetime.strftime(date, "%d %b %Y")

            # Take the second part of filename (after the date) and
            # split at the extension. Replace dashes with space.
            title = os.path.splitext(gpx_filename[11:])[0]
            title = title.replace("-", " ")

            link = "activities-" + year + ".html#" + gpx_filename[:10]
                
            gpx_link = activity_folder + gpx_filename

            if activity_text == None:
                content = title
            else:
                content = activity_text

            date = datetime.datetime.strftime(date, "%Y-%m-%d")
            self.blog_links.append(link)
            self.blog_titles.append(title)
            self.blog_dates.append(date)
            self.blog_rfcdates.append(rfcdate)
            self.blog_contents.append(content)
            self.blog_image_links.append(gpx_link)

            activities_links.append(gpx_link)
            activities_absolute_links.append(self.baseurl + link)
            activities_images.append(activity_images)
            activities_titles.append(title)
            activities_texts.append(activity_text)
            activities_dates.append(date)
            activities_months.append(year_and_month)
            activities_years.append(year)


        activities_dates, activities_links, activities_absolute_links, activities_images, activities_titles, activities_texts, activities_months, activities_years = zip(
                *sorted(zip(activities_dates, activities_links,
                    activities_absolute_links, activities_images, activities_titles,
                    activities_texts,
                    activities_months, activities_years))
        )

        activities_dates = list(reversed(list(activities_dates)))
        activities_links = list(reversed(list(activities_links)))
        activities_absolute_links = list(reversed(list(activities_absolute_links)))
        activities_images = list(reversed(list(activities_images)))
        activities_titles = list(reversed(list(activities_titles)))
        activities_texts = list(reversed(list(activities_texts)))
        activities_months = list(reversed(list(activities_months)))
        activities_years = list(reversed(list(activities_years)))

        self.blog_dates, self.blog_titles, self.blog_links, self.blog_contents, self.blog_rfcdates, self.blog_image_links = zip(
                *sorted(zip(self.blog_dates, self.blog_titles, self.blog_links,
                    self.blog_contents, self.blog_rfcdates,
                    self.blog_image_links))
        )


        self.blog_dates = list(reversed(list(self.blog_dates)))
        self.blog_links = list(reversed(list(self.blog_links)))
        self.blog_titles = list(reversed(list(self.blog_titles)))
        self.blog_contents = list(reversed(list(self.blog_contents)))
        self.blog_rfcdates = list(reversed(list(self.blog_rfcdates)))
        self.blog_image_links = list(reversed(list(self.blog_image_links)))

        activities_pages = []

        month_set = sorted(list(set(activities_months)))[::-1]
        year_set = sorted(list(set(activities_years)))[::-1]

        period_set = year_set
        activities_periods = activities_years

        for i, period in enumerate(period_set):

            body = "<article>"
            body += """
<link rel="stylesheet" href="js/leaflet/leaflet.css" />
<script src="js/leaflet/leaflet.js"></script>
<script src="js/gpx.js"></script>
            """
            body += f"<h2>Activities</h2>"
            body += "\n"
            # Add links to other years
            body += "<ul>"
            for period2 in period_set:
                if period2 == period:
                    continue
                body += f"<li><a href='activities-{period2}.html'>{period2}</a></li>"
            body += "</ul>"
            body += "<br/>"
            body += "\n"
            body += f"<h3>{period}</h3>"
            body += "\n"
            body += "\n"
            body += "<section class=gallerymasonry>"
            body += "\n"

            count = 0
            for l, a, im, t, e, d, p in zip(activities_links,
                    activities_absolute_links, activities_images, activities_titles,
                    activities_texts,
                    activities_dates, activities_periods):

                print(l)
                # If image not in current period (month or year), skip it
                if p != period:
                    continue

                # Make section in overview page
                body += """<section class="galleryitem activity">"""
                body += f"<h4>{d}: {t} "
                body += f"<a href=\"{a}\" class=\"shareButton\">(shareable link)</a>"
                body += "</h4>"
                body += "\n"
                body += f"<div id={d}-info>"
                body += f"""<div id="{d}-distance"></div>"""
                body += f"""<div id="{d}-elevationGain"></div>"""
                body += f"""<div id="{d}-duration"></div>"""
                if e is not None:
                    body += "<br />"
                    body += f"""<div id="{d}-text">{e}</div>"""
                body += "</div>"
                body += "<br />"
                body += f"""<div id="{d}" style="height: 400px; width: 100%;">"""
                body += "</div>"

                body += "<script>"
                body += f" var map{count} = L.map('{d}');"
                body += """
        L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
            maxZoom: 17,
            attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'"""
                body += "})" + f".addTo(map{count});"
                body += f"var gpx{count} = '{l}';"
                body += f" new L.GPX(gpx{count}" + ", {"
                body += """
            async: true,
            marker_options: {
                startIconUrl: 'img/pin-icon-start.png',
                endIconUrl:   'img/pin-icon-end.png',
                shadowUrl:    'img/pin-shadow.png',
                //clickable: true,
                //showRouteInfo: true
            },
        }).on('loaded', function(e) {\n"""
                # body += "console.log(e.target);"
                body += f"map{count}.fitBounds(e.target.getBounds());\n"
                body += f"""addText("Distance: " + (e.target.get_distance()/1000).toFixed(2) + " km", "{d}-distance");\n"""
                body += f"""addText("Elevation gain: " + e.target.get_elevation_gain().toFixed(0) + " m", "{d}-elevationGain");\n"""
                body += f"""addText("Duration: " + new Date(e.target.get_moving_time()).toISOString().substr(11, 8), "{d}-duration");\n"""
                body += "})"
                body += f".addTo(map{count});"
                body += "</script>\n"

                # Add images
                for image in im:
                    image_title = os.path.splitext(os.path.basename(image))[0]
                    image_title = image_title.replace("-", " ")
                    body += f"<a href=\"{image}\">"
                    body += f"<img src=\"{image}\" title=\"{image_title}\"/>"
                    body += "</a>"
                    body += "\n"
                    body += f"<figcaption>{image_title}</figcaption>"

                body += "</section>"
                body += "\n"

                count += 1

            body += "</section>"
            body += "\n"
            body += "</article>"
            body += "\n"
            body += """
            <script>
            function addText(text, divId) {
                document.getElementById(divId).innerHTML = text;
            }
            </script>"""

            page = self.combine_layouts(body)
            self.save_page(page, f"activities-{period}.html")

            if i == 0:
                self.save_page(page, f"activities.html")

            activities_pages.append([f"activities-{period}.html", period])
            print(period)

    def generate_rss(self):

        with open("rssfeedtemplate.xml", "r") as f:
            feed = f.read()

        with open("rssitemtemplate.xml", "r") as f:
            item_template = f.read()


        items = ""

        for l, t, d, c, i in zip(self.blog_links, self.blog_titles, self.blog_rfcdates, self.blog_contents, self.blog_image_links):

            c = re.sub(r"<script(.|\n)+?script>", "", c)
            c = re.sub(r"<link(.)+?>", "", c)
            c = c.replace(
                    'src="posts', 'src="' + self.baseurl + 'posts'
            )

            guid =  self.baseurl + l

            if guid.startswith("https://erikjohannes.no/photofeed") or guid.startswith("https://erikjohannes.no/activities"):
                guid = self.baseurl + i
                c = c.replace(
                        'src="', 'src="' + self.baseurl
                )

            c = html.escape(c)

            item = item_template.format(
                    t, self.baseurl + l, d, guid, c
            )


            items += item

        date = datetime.datetime.now()
        date = date - datetime.timedelta(hours=3)
        rfcdate = utils.format_datetime(date)
        feed = feed.format(rfcdate, items)

        self.save_page(feed, "index.xml")



    # def build_galleries(self):

    #     for f in os.listdir(self.photography_folder):
    #         if os.path.isdir(f):

    #             body = "<h1>Erik Johannes Husom's photography</h1>"
    #             body += "\n"
    #             body += "<h2>" + f + "</h2>"
    #             body += "\n"
    #             body += "<section class=gallerymasonry>"

    #             for img in os.listdir(self.photography_folder + "/" + f):
    #                 if os.path.splitext(img)[1].lower() in self.img_exts:
    #                     body += "    <section class=galleryitem>"
    #                     body += 

    #             body += "</section>"

    #             page = self.combine_layouts(body)

    #             self.save_page(page, f + ".html")


if __name__ == '__main__':

    website = Website()
    website.build_pages()
    website.build_blog(exclude_drafts=True)
    website.read_photo_feed("yearly")
    website.create_activity_feed()
    website.generate_rss()

