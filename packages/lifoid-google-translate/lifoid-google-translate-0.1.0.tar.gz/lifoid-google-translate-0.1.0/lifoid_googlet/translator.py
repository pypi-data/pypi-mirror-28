# -*- coding: utf8 -*-
"""
Google Translate implementation
Author: Romary Dupuis <romary@me.com>
"""
import json
import urllib
import httplib2
from lifoid.config import settings
from lifoid.translate import Translator

"""
Language Code
-------- ----
Afrikaans 	af
Albanian 	sq
Arabic 	ar
Belarusian 	be
Bulgarian 	bg
Catalan 	ca
Chinese Simplified 	zh-CN
Chinese Traditional 	zh-TW
Croatian 	hr
Czech 	cs
Danish 	da
Dutch 	nl
English 	en
Estonian 	et
Filipino 	tl
Finnish 	fi
French 	fr
Galician 	gl
German 	de
Greek 	el
Hebrew 	iw
Hindi 	hi
Hungarian 	hu
Icelandic 	is
Indonesian 	id
Irish 	ga
Italian 	it
Japanese 	ja
Korean 	ko
Latvian 	lv
Lithuanian 	lt
Macedonian 	mk
Malay 	ms
Maltese 	mt
Norwegian 	no
Persian 	fa
Polish 	pl
Portuguese 	pt
Romanian 	ro
Russian 	ru
Serbian 	sr
Slovak 	sk
Slovenian 	sl
Spanish 	es
Swahili 	sw
Swedish 	sv
Thai 	th
Turkish 	tr
Ukrainian 	uk
Vietnamese 	vi
Welsh 	cy
Yiddish 	yi
"""

LANGUAGES = ["af", "sq", "ar", "be", "bg", "ca", "zh-CN", "zh-TW", "hr",
             "cs", "da", "nl", "en", "et", "tl", "fi", "fr", "gl", "de",
             "el", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "ko",
             "lv", "lt", "mk", "ms", "mt", "no", "fa", "pl", "pt", "ro",
             "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk",
             "vi", "cy", "yi"]


def _validate_language(lang):
    if lang in LANGUAGES:
        return True
    return False


class GoogleTranslator(Translator):
    """
    Google Translator object.
    """
    def __init__(self):
        # TODO: Implement caching
        self.cache_control = 'max-age=' + str(7 * 24 * 60 * 60)
        self.connection = httplib2.Http()
        self.base_url = "https://www.googleapis.com/language/translate/v2/"

    def _urlencode(self, params):
        """
        Rewrite urllib.urlencode to handle string input verbatim
        """
        params = "&".join(map("=".join, params))
        return params

    def _build_uri(self, extra_url, params):
        params = [('key', settings.google_translate.api_key)] + params
        params = self._urlencode(params)
        url = "%s?%s" % (urllib.parse.urljoin(self.base_url, extra_url), params)
        if len(url) > 2000:  # for GET requests only, POST is 5K
            raise ValueError("Query is too long. URL can only be 2000 "
                             "characters")
        return url

    def _fetch_data(self, url):
        connection = self.connection
        resp, content = connection.request(url, headers={
            'user-agent': settings.google_translate.api_key,
            'cache-control': self.cache_control})
        return content

    def _sanitize_query(self, query):
        if isinstance(query, (list, tuple)):
            query = zip('q' * len(query), map(urllib.parse.quote, query))
        else:
            query = [('q', urllib.parse.quote(query))]
        return query

    def _decode_json(self, response):
        """
        Assumes that response only holds one result
        """
        json_data = json.loads(response)
        try:
            data = json_data["data"]
            if 'translations' in data:
                return data['translations']
            elif 'detections' in data:
                return data['detections']
        except:
            if 'error' in json_data:
                return json_data["error"]

    def translate(self, query, target="en", source="", _dirty=False):
        """
        Translate a query.
        """
        try:
            assert _validate_language(target)
        except:
            raise ValueError("target language %s is not valid" % target)
        newquery = self._sanitize_query(query)
        params = [('key', settings.google_translate.api_key),
                  ('target', target)]
        if source:
            try:
                assert _validate_language(target)
            except:
                raise ValueError("source language %s is not valid" % target)
            params += [("source", source)]
        params += newquery
        url = self._build_uri("", params)
        content = self._fetch_data(url)
        results = self._decode_json(content)

        if "errors" in results and not _dirty:
            if results['message'] == 'Bad language pair: {0}':
                # try to detect language and resubmit query
                source = self.detect(query)
                source = source[0]['language']
                return self.translate(query, target, source, True)

        return results
