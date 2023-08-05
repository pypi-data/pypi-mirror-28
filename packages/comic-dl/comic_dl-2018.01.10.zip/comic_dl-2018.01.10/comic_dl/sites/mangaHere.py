#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging


class MangaHere(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)

        url_split = str(manga_url).split("/")

        if len(url_split) is 6:
            self.full_series(comic_url=manga_url, comic_name=self.comic_name, sorting=self.sorting,
                             download_directory=download_directory, chapter_range=chapter_range, conversion=conversion,
                             delete_files=delete_files)
        else:
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                delete_files=delete_files)

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, delete_files):
        # Some chapters have integer values and some have decimal values. We will look for decimal first.
        try:
            chapter_number = re.search(r"c(\d+\.\d+)", str(comic_url)).group(1)
        except:
            chapter_number = re.search(r"c(\d+)", str(comic_url)).group(1)

        source, cookies_main = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        last_page_number = str(re.search(r'total_pages\ \=\ (.*?) \;', str(source)).group(1)).strip()

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"

        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        for chapCount in range(1, int(last_page_number) + 1):

            chapter_url = str(comic_url) + '/%s.html' % chapCount
            logging.debug("Chapter Url : %s" % chapter_url)

            source_new, cookies_new = globalFunctions.GlobalFunctions().page_downloader(manga_url=chapter_url,
                                                                                        cookies=cookies_main)

            image_link_finder = source_new.findAll('section', {'class': 'read_img'})

            for link in image_link_finder:
                x = link.findAll('img')
                for a in x:
                    image_link = a['src']

                    if image_link in ['http://www.mangahere.co/media/images/loading.gif']:
                        pass
                    else:
                        # file_name = "0" + str(chapCount) + ".jpg"
                        if len(str(chapCount)) < len(str(last_page_number)):
                            number_of_zeroes = len(str(last_page_number)) - len(str(chapCount))
                            # If a chapter has only 9 images, we need to avoid 0*0 case.
                            if len(str(number_of_zeroes)) == 0:
                                file_name = str(chapCount) + ".jpg"
                            else:
                                file_name = "0" * int(number_of_zeroes) + str(chapCount) + ".jpg"
                        else:
                            file_name = str(chapCount) + ".jpg"

                        logging.debug("Image Link : %s" % image_link)
                        globalFunctions.GlobalFunctions().downloader(image_link, file_name, chapter_url, directory_path,
                                                                     log_flag=self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[4].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        anime_name = str(safe_name.title()).replace("_", " ")

        return anime_name

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        all_links = re.findall(r"class=\"color_0077\" href=\"(.*?)\"", str(source))

        chapter_links = []

        for link in all_links:
            if 'mangahere.co/manga/' in link:
                chapter_links.append(link)
            else:
                pass

        logging.debug("All Links : %s" % all_links)

        # Uh, so the logic is that remove all the unnecessary chapters beforehand
        #  and then pass the list for further operations.
        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1

            if (str(chapter_range).split("-")[1]).decode().isdecimal():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]

            chapter_links = [chapter_links[x] for x in indexes][::-1]
        else:
            chapter_links = chapter_links

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in chapter_links:
                self.single_chapter(comic_url=str(chap_link), comic_name=comic_name,
                                    download_directory=download_directory, conversion=conversion,
                                    delete_files=delete_files)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in chapter_links[::-1]:
                self.single_chapter(comic_url=str(chap_link), comic_name=comic_name,
                                    download_directory=download_directory, conversion=conversion,
                                    delete_files=delete_files)

        print("Finished Downloading")
        return 0
