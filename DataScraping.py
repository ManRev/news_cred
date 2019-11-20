import time
from selenium import webdriver
from random import shuffle
from selenium.webdriver.common.keys import Keys
import sys

br = webdriver.Safari()
url = "https://www.cnn.com/2018/10/16/middleeast/khashoggi-saudi-pompeo-intl/index.html"


def ob_unit(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        dest_url = str(e.get_attribute('href'))  ### URL of the destination
        text_elem = e.find_elements_by_xpath(".//span[contains(@class, 'ob-unit ob-rec-source')]")
        source = ()
        caption = ()
        img_url = ()
        for t in text_elem:
            source = str(t.text).strip()  ### Sometimes the name of the destination website is mentioned
        title_elem = e.find_elements_by_xpath(".//span[contains(@class, 'ob-unit ob-rec-text')]")
        for t in title_elem:
            caption = str(t.text).strip()
        # caption = str(title_elem.get_attribute('title'))
        # source = str(text_elem.get_attribute('title'))
        #### Sometimes some caption is given along the ad / recommendation
        img_elem = e.find_elements_by_xpath(
            ".//img[contains(@class, 'ob-rec-image ob-show')]")  ### URL of the CRN image
        for t in img_elem:
            img_url = str(t.get_attribute('src'))
        out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>outbrain<<||>>ob_unit""" % (
            time_stamp, dest_url, source, caption, img_url)
        out_set.add(out)
    return out_set


def ob_unit2(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        dest_url = str(e.get_attribute('href'))  ### URL of the destination
        source = ()
        caption = ()
        img_url = ()
        title_elem = e.find_elements_by_xpath(".//span[contains(@class, 'strip-rec-link-title ob-tcolor')]")
        for t in title_elem:
            caption = str(t.text).strip()
        # caption = str(title_elem.get_attribute('title'))
        # source = str(text_elem.get_attribute('title'))
        #### Sometimes some caption is given along the ad / recommendation
        img_elem = e.find_elements_by_xpath(
            ".//img[contains(@class, 'ob-rec-image ob-show')]")  ### URL of the CRN image
        for t in img_elem:
            img_url = str(t.get_attribute('src'))
        out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>outbrain<<||>>ob_unit2""" % (
            time_stamp, dest_url, source, caption, img_url)
        out_set.add(out)

    return out_set


def ob_dynamic_rec_link(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        img_url = ()
        source = ()
        caption = ()
        dest_url = str(e.get_attribute('href'))  ### URL of the destination
        text_elem = e.find_elements_by_xpath(".//span[contains(@class, 'rec-source')]")
        for t in text_elem:
            source = str(t.text).strip()  ### Sometimes the name of the destination website is mentioned

        title_elem = e.find_elements_by_xpath(".//span[contains(@class, 'rec-text')]")
        for t in title_elem:
            caption = str(t.text).strip()  #### Sometimes some caption is given along the ad / recommendation
        img_elem = e.find_elements_by_xpath(
            ".//img[contains(@class, 'ob-rec-image ob-show')]")  ### URL of the CRN image
        for t in img_elem:
            img_url = str(t.get_attribute('src'))
        out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>outbrain<<||>>dynamic-rec-link""" % (
            time_stamp, dest_url, source, caption, img_url)
        out_set.add(out)
    return out_set


def dual_container(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        row_elems = e.find_elements_by_xpath(".//li")
        for r in row_elems:
            img_url = ()
            a = r.find_element_by_xpath(".//a[contains(@class, 'rec-link')]")
            dest_url = str(a.get_attribute('href'))
            caption = str(a.text).strip()

            text_elem = r.find_element_by_xpath(".//span[contains(@class, 'source')]")
            source = str(text_elem.text).strip()
            img_elem = e.find_elements_by_xpath(
                ".//img[contains(@class, 'ob-rec-image ob-show')]")  ### URL of the CRN image
            for t in img_elem:
                img_url = str(t.get_attribute('src'))
            out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>outbrain<<||>>dual_container""" % (
                time_stamp, dest_url, source, caption, img_url)
            out_set.add(out)
    return out_set


def ob_dual(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for r in elems:
        row_elems = r.find_elements_by_xpath(".//div[contains(@class, 'odb_div')]")
        for e in row_elems:
            img_url = ()
            main_elem = e.find_element_by_xpath(".//div[contains(@class, 'ob-text-content')]")
            link_elem = main_elem.find_element_by_xpath(".//a")
            dest_url = str(link_elem.get_attribute('href'))
            caption = str(link_elem.text).strip()
            text_elem = main_elem.find_element_by_xpath(".//span[contains(@class, 'source')]")
            source = str(text_elem.text).strip()
            img_elem = e.find_elements_by_xpath(
                ".//img[contains(@class, 'ob-rec-image ob-show')]")  ### URL of the CRN image
            for t in img_elem:
                img_url = str(t.get_attribute('src'))
            out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>outbrain<<||>>ob_dual""" % (
                time_stamp, dest_url, source, caption, img_url)
            out_set.add(out)
    return out_set


def recs_wrap(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        row_elems = e.find_elements_by_xpath(".//a")
        for r in row_elems:
            img_url = ()
            dest_url = str(r.get_attribute('href'))
            text_elem = r.find_element_by_xpath(".//span[contains(@class, 'ob-pub')]")
            source = str(text_elem.text).strip()
            caption = str(r.text).strip()
            caption = str(caption.replace(source, ' ')).strip()
            img_elem = e.find_elements_by_xpath(
                ".//img[contains(@class, 'ob-rec-image ob-show')]")  ### URL of the CRN image
            for t in img_elem:
                img_url = str(t.get_attribute('src'))
            out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>outbrain<<||>>recs_wrap""" % (
                time_stamp, dest_url, source, caption, img_url)
            out_set.add(out)
    return out_set


def ob_rec_li(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        img_url = ()
        link = e.find_element_by_xpath(".//a")
        dest_url = str(link.get_attribute('href'))
        caption = str(link.text).strip()
        text_elem = e.find_element_by_xpath(".//span[contains(@class, 'rec-src-link')]")
        source = str(text_elem.text).strip()
        img_elem = e.find_elements_by_xpath(
            ".//img[contains(@class, 'ob-rec-image ob-show')]")  ### URL of the CRN image
        for t in img_elem:
            img_url = str(t.get_attribute('src'))
        out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>outbrain<<||>>ob_rec_li""" % (
            time_stamp, dest_url, source, caption, img_url)
        out_set.add(out)
    return out_set


def link_containers(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        img_url = ()
        dest_url = str(e.get_attribute('href'))
        text_elem = e.find_element_by_xpath(".//span[contains(@class, 'source')]")
        source = str(text_elem.text).strip()
        title_elem = e.find_element_by_xpath(".//div[contains(@class, 'rec-link-title')]")
        caption = str(title_elem.text).strip()
        img_elem = e.find_elements_by_xpath(
            ".//img[contains(@class, 'ob-rec-image ob-show')]")  ### URL of the CRN image
        for t in img_elem:
            img_url = str(t.get_attribute('src'))
        out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>outbrain<<||>>link_container""" % (
            time_stamp, dest_url, source, caption, img_url)
        out_set.add(out)
    return out_set


def link_containers_2(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for r in elems:
        row_elems = r.find_elements_by_xpath(".//a")
        for e in row_elems:
            img_url = ()
            dest_url = str(e.get_attribute('href'))
            text_elem = e.find_element_by_xpath(".//span[contains(@class, 'source')]")
            source = str(text_elem.text).strip()
            title_elem = e.find_element_by_xpath(".//div[contains(@class, 'rec-link-title')]")
            caption = str(title_elem.text).strip()
            img_elem = e.find_elements_by_xpath(
                ".//img[contains(@class, 'ob-rec-image ob-show')]")  ### URL of the CRN image
            for t in img_elem:
                img_url = str(t.get_attribute('src'))
            out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>outbrain<<||>>link_container_2""" % (
                time_stamp, dest_url, source, caption, img_url)
            out_set.add(out)
    return out_set


def trc_container(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        divs = e.find_elements_by_xpath(".//div")
        for d in divs:
            for link in d.find_elements_by_xpath(".//a"):
                dest_url = str(link.get_attribute('href'))
                caption = str(link.get_attribute('title')).strip()
                try:
                    text_elem = e.find_element_by_xpath(".//span[contains(@class,'branding')]")
                    source = str(text_elem.text).strip()
                except:
                    source = str()
                img_elem = e.find_elements_by_xpath(".//span[contains(@class, 'thumbBlock')]")  ### URL of the CRN image
                for t in img_elem:
                    img_url = str(t.get_attribute('style'))
                out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>taboola<<||>>trc-container""" % (time_stamp, dest_url,
                                                                                                  source, caption,
                                                                                                  img_url)
                out_set.add(out)
    return out_set


def revcontent(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        link = e.find_element_by_xpath(".//a")
        dest_url = str(link.get_attribute('data-target'))
        text_elem = e.find_element_by_xpath(".//div[contains(@class, 'rc-headline')]")
        caption = str(text_elem.text).strip()
        text_elem = e.find_element_by_xpath(".//div[contains(@class, 'rc-provider')]")
        source = str(text_elem.text).strip()
        img_elem = e.find_elements_by_xpath(".//div[contains(@class, 'rc-photo')]")  ### URL of the CRN image
        for t in img_elem:
            img_url = str(t.get_attribute('style'))
        out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>revcontent<<||>>rc-item""" % (
        time_stamp, dest_url, source, caption, img_url)
        out_set.add(out)
    return out_set


def gravity(frameElems, br):
    out_set = set()
    for fe in frameElems:
        br.switch_to_frame(fe.find_element_by_xpath("iframe"))
        elems = br.find_elements_by_xpath("//li[contains(@class, 'grv_article')]")
        time_stamp = str(int(time.time()))
        for e in elems:
            title = e.find_element_by_xpath(".//a[contains(@class, 'grv_article_title')]")
            dest_url = str(title.get_attribute('href'))
            caption = str(title.text).strip()
            text_elem = e.find_element_by_xpath(".//a[contains(@class, 'url_domain')]")
            source = str(text_elem.text).strip()
            out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>gravity<<||>>grv_article""" % (
            time_stamp, dest_url, source, caption)
            out_set.add(out)
        br.switch_to_default_content()
    return out_set


def gravity_article(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        link = e.find_element_by_xpath(".//a")
        dest_url = str(link.get_attribute('href'))
        text_elem = e.find_element_by_xpath(".//span[contains(@class, 'title')]")
        caption = str(text_elem.text).strip()
        text_elem = e.find_element_by_xpath(".//span[contains(@class, 'attribution')]")
        source = str(text_elem.text).strip()
        out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>gravity<<||>>grv_below_article""" % (
        time_stamp, dest_url, source, caption)
        out_set.add(out)
    return out_set


def zergnet(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        img_url = ()
        link = e.find_element_by_xpath(".//a")
        dest_url = str(link.get_attribute('href'))
        text_elem = e.find_element_by_xpath(".//div[contains(@class, 'zergheadline')]")
        caption = str(text_elem.text).strip()
        txt_source = e.find_element_by_xpath(".//span[contains(@class, 'zergdestW')]")
        source = str(txt_source.text).strip()
        img_elem = e.find_element_by_xpath(".//img")
        img_url = str(img_elem.get_attribute('src'))
        out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>zergnet<<||>>zergent""" % (
            time_stamp, dest_url, source, caption, img_url)
        out_set.add(out)
    return out_set


def dianomi(elems):
    out_set = set()
    time_stamp = str(int(time.time()))
    for e in elems:
        link = e.find_element_by_xpath(".//a")
        dest_url = str(link.get_attribute('href'))
        text_elem = e.find_element_by_xpath(".//a[contains(@href, dest_url)]")
        caption = str(text_elem.text).strip()
        txt_source = e.find_element_by_xpath(".//div[contains(@class, 'brand')]")
        source = str(txt_source.text).strip()
        img_elem = e.find_element_by_xpath(".//div[contains(@class, 'lazy-image')]")
        img_url = str(img_elem.get_attribute('data-src'))
        out = """%s<<||>>%s<<||>>%s<<||>>%s<<||>>%s<<||>>dianomi<<||>>dianomi""" % (
            time_stamp, dest_url, source, caption, img_url)
        out_set.add(out)
    return out_set


def get_widget_elements(br):
    outputs = set()
    #### ALL the xpath queries here detect the presence of a widget by the 5 CRNs
    ### Once detected, I write further queries to extract desired elements.

    ############ OutBrain - possibilites ####################
    ### Outbrain shows their widets in several ways
    ### I wrote xpaths for all the possible ways I encountered (this list might not be exhaustive)

    # "ob-dynamic-rec-container ob-recIdx-0 ob-o"
    elems = br.find_elements_by_xpath("//li[contains(@class, 'ob-dynamic-rec-container ob-recIdx-')]")
    if len(elems) > 0:  ##### Means some widgets was detected using this query
        outputs = outputs | ob_unit(elems)  ### Here I extract information from that widget

    # elems = br.find_elements_by_xpath("//div[contains(@id, 'outbrain_widget_')]")
    # if len(elems) > 0:  ##### Means some widgets was detected using this query
    #    outputs = outputs | ob_unit(elems)  ### Here I extract information from that widget


    elems = br.find_elements_by_xpath("//div[contains(@class, 'item-container ob-recIdx')]")
    if len(elems) > 0:  ##### Means some widgets was detected using this query
        outputs = outputs | ob_unit2(elems)

    elems = br.find_elements_by_xpath("//div[contains(@class, 'ob_container_recs')]")
    if len(elems) > 0:  ##### Means some widgets was detected using this query
        outputs = outputs | ob_unit2(elems)

    elems = br.find_elements_by_xpath("//a[@class='ob-dynamic-rec-link']")
    if len(elems) > 0:  ##### Means some widgets was detected using this query
        outputs = outputs | ob_dynamic_rec_link(elems)  ### Here I extract information from that widget

    elems = br.find_elements_by_xpath("//div[contains(@class, 'dual_container')]")
    if len(elems) > 0:
        outputs = outputs | dual_container(elems)

    elems = br.find_elements_by_xpath("//div[contains(@class, 'ob_dual_')]")
    if len(elems) > 0:
        outputs = outputs | ob_dual(elems)

    elems = br.find_elements_by_xpath("//a[contains(@class, 'item-link-container')]")
    if len(elems) > 0:
        outputs = outputs | link_containers(elems)

    elems = br.find_elements_by_xpath("//div[contains(@class, 'item-link-container')]")
    if len(elems) > 0:
        outputs = outputs | link_containers_2(elems)

    elems = br.find_elements_by_xpath("//div[@id='outbrain-recs-wrap']")
    if len(elems) > 0:
        outputs = outputs | recs_wrap(elems)

    elems = br.find_elements_by_xpath("//li[contains(@class, 'outbrain_rec_li')]")
    if len(elems) > 0:
        outputs = outputs | ob_rec_li(elems)

    ############ Taboola ####################
    elems = br.find_elements_by_xpath("//div[contains(@id, 'internal_trc')]")
    if len(elems) > 0:
        outputs = outputs | trc_container(elems)

    ############ Revcontent ####################
    elems = br.find_elements_by_xpath("//div[@class='rc-item']")
    if len(elems) > 0:
        outputs = outputs | revcontent(elems)
    """
    ############ Gravity ####################
    elems = br.find_elements_by_xpath("//div[contains(@id, 'grv-personalization')]")    ### This is an iFrame - Special case
    if len(elems) > 0:
        outputs = outputs | gravity(elems,br)

    elems = br.find_elements_by_xpath("//div[contains(@class, 'gravity-below-article')]")
    if len(elems) > 0:
        outputs = outputs | gravity_article(elems)
    """
    ############ Zergnet ####################
    elems = br.find_elements_by_xpath("//div[@class='zergentity']")
    if len(elems) > 0:
        outputs = outputs | zergnet(elems)

    ############ Dianomi ####################
    elems = br.find_elements_by_xpath("//article[@class='partial tile media image-top margin-32-bottom']")
    if len(elems) > 0:
        outputs = outputs | dianomi(elems)
    # partial tile media image-top margin-32-bottom
    return outputs


def do_crawl(br, url):
    br.get(url)
    number_of_scroll = 5
    while number_of_scroll > 0:
        br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        number_of_scroll = number_of_scroll - 1
    ### Do some time.sleep or scroll - as you need
    return get_widget_elements(br)


def open_tabs(url):
    br.get("https://www.cnn.com")
    elems = br.find_elements_by_xpath("//section[contains(@class, 'homepage1')]")
    for e in elems:
        link = e.find_element_by_xpath(".//a")
        url = link.get_attribute('href')
        # link.send_keys(Keys.COMMAND + 't')
        # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        widgets_collected = do_crawl(br, url)
        print(widgets_collected)
        print("----------------------------")


if __name__ == '__main__':
    visited_url = []
    # br is a webdriver instance using selenium
    # url is some URL you want to visit
    """ br.get("https://www.cnn.com")
    elems = br.find_elements_by_xpath("//section[contains(@class, 'homepage1')]//a[@href]")
    #elems = parentElement.find_elements_by_xpath("//a[@href]")
    #elems = br.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        visited_url.append(elem.get_attribute("href"))
    visited_url = list(set(visited_url))
    print(visited_url)
    visited_url = visited_url[:2]
    #elems = br.find_elements_by_xpath("//section[contains(@class, 'homepage1')]")
    for e in visited_url:
        widgets_collected = do_crawl(br, e)
        print(widgets_collected)
        print("----------------------------")
    """
    br.get("https://www.cnn.com")
    elems = br.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        visited_url.append(elem.get_attribute("href"))
    visited_url = list(set(visited_url))
    visited_url = visited_url[:]
    print(visited_url)
    t = min(len(visited_url), 20)
    for e in visited_url:
        if t > 0:
            widgets_collected = do_crawl(br, e)
            if len(widgets_collected) != 0:
                print(widgets_collected)
                print("----------------------------")
                t = t - 1
        else:
            break
    br.close()
