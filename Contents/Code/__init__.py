PLUGIN_PREFIX   = "/photos/JessicaClaire"
ROOT_URL        = "http://www.jessicaclaire.net"
RSS_FEED        = ROOT_URL + "/rss/"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "Jessica Claire", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup("Pictures", viewMode="Pictures", mediaType="photos")
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.art = "art-default.jpg"
  DirectoryItem.thumb = "icon-default.png"

####################################################################################################  

def MainMenu():
    dir = MediaContainer(title1="Jessica Claire")
    for item in XML.ElementFromURL(RSS_FEED).xpath("//item"):
      
      title = item.xpath('.//title')[0].text
      url = item.xpath('.//guid')[0].text
      raw_summary = HTML.StringFromElement(item.xpath('.//description')[0]).replace(']]','').replace('<![CDATA[','').replace('&gt;','>').replace('&lt;','<').replace('&nbsp;','')#.text
      summary = HTML.ElementFromString(raw_summary).text_content()[:400]+"..."
      try:
        thumb = HTML.ElementFromString(raw_summary).xpath('.//img')[0].get('src')
      except:
        thumb = None
        
      dir.Append(Function(DirectoryItem(PictureMenu, title=title, thumb=thumb, summary=summary), url=url))

    return dir

def PictureMenu(sender, url,title = ''):
  dir = MediaContainer(viewGroup="Pictures", title1="Jessica Claire", title2=title)
  count = 1
  for img in HTML.ElementFromURL(url).xpath('//img'):
    if img.get('src').find('/images/content') != -1:
      url = ROOT_URL + img.get('src')
      dir.Append(PhotoItem(url, 'Photo %d' % count, '', url))
      count += 1
    
  return dir
