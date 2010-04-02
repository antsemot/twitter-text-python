# -*- coding: UTF-8 -*-
#  This file is part of twp.
#
#  twp is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  twp is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  twp. If not, see <http://www.gnu.org/licenses/>.


# twp - Unittests --------------------------------------------------------------
# ------------------------------------------------------------------------------
import unittest
import twp


class TWPTests(unittest.TestCase):
    def setUp(self):
        self.parser = twp.Parser()
    
    
    # General Tests ------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_all_not_allow_amp_without_question(self):
        result = self.parser.parse(u'Check out: http://www.github.com/test&@username')
        self.assertEqual(result.html, u'Check out: <a href="http://www.github.com/test">http://www.github.com/test</a>&<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.urls, [u'http://www.github.com/test'])
    
    def test_all_not_break_url_at(self):
        result = self.parser.parse(u'http://www.flickr.com/photos/29674651@N00/4382024406')
        self.assertEqual(result.html, u'<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>')
        self.assertEqual(result.urls, [u'http://www.flickr.com/photos/29674651@N00/4382024406'])
    
    
    # URL tests ----------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_url_mid(self):
        result = self.parser.parse(u'text http://example.com more text')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a> more text')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_unicode(self):
        result = self.parser.parse(u'I enjoy Macintosh Brand computers: http://✪df.ws/ejp')
        self.assertEqual(result.html, u'I enjoy Macintosh Brand computers: <a href="http://✪df.ws/ejp">http://✪df.ws/ejp</a>')
        self.assertEqual(result.urls, [u'http://\u272adf.ws/ejp'])
    
    def test_url_parentheses(self):
        result = self.parser.parse(u'text (http://example.com)')
        self.assertEqual(result.html, u'text (<a href="http://example.com">http://example.com</a>)')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_amp_lang_equals(self):
        result = self.parser.parse(u'Check out http://search.twitter.com/search?q=avro&lang=en')
        self.assertEqual(result.html, u'Check out <a href="http://search.twitter.com/search?q=avro&amp;lang=en">http://search.twitter.com/s...</a>')
        self.assertEqual(result.urls, [u'http://search.twitter.com/search?q=avro&lang=en'])
        
    def test_url_amp_break(self):
        result = self.parser.parse(u'Check out http://twitter.com/te?foo&invalid=True')
        self.assertEqual(result.html, u'Check out <a href="http://twitter.com/te?foo&amp;invalid=True">http://twitter.com/te?foo...</a>')
        self.assertEqual(result.urls, [u'http://twitter.com/te?foo&invalid=True'])
    
    def test_url_dash(self):
        result = self.parser.parse(u'Is www.foo-bar.com a valid URL?')
        self.assertEqual(result.html, u'Is <a href="http://www.foo-bar.com">www.foo-bar.com</a> a valid URL?')
        self.assertEqual(result.urls, [u'www.foo-bar.com'])
    
    def test_url_multiple(self):
        result = self.parser.parse(u'http://example.com https://sslexample.com http://sub.example.com')
        self.assertEqual(result.html, u'<a href="http://example.com">http://example.com</a> <a href="https://sslexample.com">https://sslexample.com</a> <a href="http://sub.example.com">http://sub.example.com</a>')
        self.assertEqual(result.urls, [u'http://example.com', u'https://sslexample.com', u'http://sub.example.com'])
    
    def test_url_raw_domain(self):
        result = self.parser.parse(u'See http://example.com example.com')
        self.assertEqual(result.html, u'See <a href="http://example.com">http://example.com</a> example.com')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_embed_link(self):
        result = self.parser.parse(u'<link rel=\'true\'>http://example.com</link>')
        self.assertEqual(result.html, u'<link rel=\'true\'><a href="http://example.com">http://example.com</a></link>')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_trailing(self):
        result = self.parser.parse(u'text http://example.com')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_japanese(self):
        result = self.parser.parse(u'いまなにしてるhttp://example.comいまなにしてる')
        self.assertEqual(result.html, u'いまなにしてる<a href="http://example.com">http://example.com</a>いまなにしてる')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    
    # URL followed Tests -------------------------------------------------------
    def test_url_followed_question(self):
        result = self.parser.parse(u'text http://example.com?')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>?')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_colon(self):
        result = self.parser.parse(u'text http://example.com:')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>:')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_curly_brace(self):
        result = self.parser.parse(u'text http://example.com}')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>}')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_single_quote(self):
        result = self.parser.parse(u'text http://example.com')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_dot(self):
        result = self.parser.parse(u'text http://example.com.')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>.')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_exclamation(self):
        result = self.parser.parse(u'text http://example.com!')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>!')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_comma(self):
        result = self.parser.parse(u'text http://example.com,')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>,')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_brace(self):
        result = self.parser.parse(u'text http://example.com)')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>)')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_big_brace(self):
        result = self.parser.parse(u'text http://example.com]')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>]')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_equals(self):
        result = self.parser.parse(u'text http://example.com=')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>=')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    def test_url_followed_semicolon(self):
        result = self.parser.parse(u'text http://example.com;')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>;')
        self.assertEqual(result.urls, [u'http://example.com'])
    
    
    # URL preceeded Tests -------------------------------------------------------
    def test_url_preceeded_colon(self):
        result = self.parser.parse(u'text:http://example.com')
        self.assertEqual(result.html, u'text:<a href="http://example.com">http://example.com</a>')
        self.assertEqual(result.urls, [u'http://example.com'])
            
    def test_not_url_preceeded_equals(self):
        result = self.parser.parse(u'text =http://example.com')
        self.assertEqual(result.html, u'text =http://example.com')
        self.assertEqual(result.urls, [])
    
    # NOT
    def test_not_url_preceeded_forwardslash(self):
        result = self.parser.parse(u'text /http://example.com')
        self.assertEqual(result.html, u'text /http://example.com')
        self.assertEqual(result.urls, [])
    
    def test_not_url_preceeded_exclamation(self):
        result = self.parser.parse(u'text !http://example.com')
        self.assertEqual(result.html, u'text !http://example.com')
        self.assertEqual(result.urls, [])

    
    # URL not tests ------------------------------------------------------------
    def test_not_url_dotdotdot(self):
        result = self.parser.parse(u'Is www...foo a valid URL?')
        self.assertEqual(result.html, u'Is www...foo a valid URL?')
        self.assertEqual(result.urls, [])
        
    def test_not_url_dash(self):
        result = self.parser.parse(u'Is www.-foo.com a valid URL?')
        self.assertEqual(result.html, u'Is www.-foo.com a valid URL?')
        self.assertEqual(result.urls, [])
        
    def test_all_not_break_url_at(self):
        result = self.parser.parse(u'http://www.flickr.com/photos/29674651@N00/4382024406')
        self.assertEqual(result.html, u'<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>')
        self.assertEqual(result.urls, [u'http://www.flickr.com/photos/29674651@N00/4382024406'])
    
    
    # URL numeric tests --------------------------------------------------------
    def test_url_at_numeric(self):
        result = self.parser.parse(u'http://www.flickr.com/photos/29674651@N00/4382024406')
        self.assertEqual(result.html, u'<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>')
        self.assertEqual(result.urls, [u'http://www.flickr.com/photos/29674651@N00/4382024406'])
        
    def test_url_at_non_numeric(self):
        result = self.parser.parse(u'http://www.flickr.com/photos/29674651@N00/foobar')
        self.assertEqual(result.html, u'<a href="http://www.flickr.com/photos/29674651@N00/foobar">http://www.flickr.com/photo...</a>')
        self.assertEqual(result.urls, [u'http://www.flickr.com/photos/29674651@N00/foobar'])
    
    
    # URL domain tests ---------------------------------------------------------
    def test_url_WWW(self):
        result = self.parser.parse(u'WWW.EXAMPLE.COM')
        self.assertEqual(result.html, u'<a href="http://WWW.EXAMPLE.COM">WWW.EXAMPLE.COM</a>')
        self.assertEqual(result.urls, [u'WWW.EXAMPLE.COM'])
    
    def test_url_www(self):
        result = self.parser.parse(u'www.example.com')
        self.assertEqual(result.html, u'<a href="http://www.example.com">www.example.com</a>')
        self.assertEqual(result.urls, [u'www.example.com'])
    
    def test_url_only_domain_query_followed_period(self):
        result = self.parser.parse(u'I think it\'s proper to end sentences with a period http://tell.me/why?=because.i.want.it. Even when they contain a URL.')
        self.assertEqual(result.html, u'I think it\'s proper to end sentences with a period <a href="http://tell.me/why?=because.i.want.it">http://tell.me/why?=because...</a>. Even when they contain a URL.')
        self.assertEqual(result.urls, [u'http://tell.me/why?=because.i.want.it'])
    
    def test_url_only_domain_followed_period(self):
        result = self.parser.parse(u'I think it\'s proper to end sentences with a period http://tell.me. Even when they contain a URL.')
        self.assertEqual(result.html, u'I think it\'s proper to end sentences with a period <a href="http://tell.me">http://tell.me</a>. Even when they contain a URL.')
        self.assertEqual(result.urls, [u'http://tell.me'])
    
    def test_url_only_domain_path_followed_period(self):
        result = self.parser.parse(u'I think it\'s proper to end sentences with a period http://tell.me/why. Even when they contain a URL.')
        self.assertEqual(result.html, u'I think it\'s proper to end sentences with a period <a href="http://tell.me/why">http://tell.me/why</a>. Even when they contain a URL.')
        self.assertEqual(result.urls, [u'http://tell.me/why'])
    
    def test_url_long_tld(self):
        result = self.parser.parse(u'http://example.mobi/path')
        self.assertEqual(result.html, u'<a href="http://example.mobi/path">http://example.mobi/path</a>')
        self.assertEqual(result.urls, [u'http://example.mobi/path'])
    
    def test_url_multiple_protocols(self):
        result = self.parser.parse(u'http://foo.com AND https://bar.com AND www.foobar.com')
        self.assertEqual(result.html, u'<a href="http://foo.com">http://foo.com</a> AND <a href="https://bar.com">https://bar.com</a> AND <a href="http://www.foobar.com">www.foobar.com</a>')
        self.assertEqual(result.urls, [u'http://foo.com', u'https://bar.com', u'www.foobar.com'])
    
    # NOT
    def test_not_url_exclamation_domain(self):
        result = self.parser.parse(u'badly formatted http://foo!bar.com')
        self.assertEqual(result.html, u'badly formatted http://foo!bar.com')
        self.assertEqual(result.urls, [])
    
    def test_not_url_under_domain(self):
        result = self.parser.parse(u'badly formatted http://foo_bar.com')
        self.assertEqual(result.html, u'badly formatted http://foo_bar.com')
        self.assertEqual(result.urls, [])
    

    # Hashtag tests ------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_hashtag_followed_full_whitespace(self):
        result = self.parser.parse(u'#hashtag　text')
        self.assertEqual(result.html, u'<a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>　text')
        self.assertEqual(result.tags, [u'hashtag'])
    
    def test_hashtag_followed_full_hash(self):
        result = self.parser.parse(u'＃hashtag')
        self.assertEqual(result.html, u'<a href="http://search.twitter.com/search?q=%23hashtag">＃hashtag</a>')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_hashtag_preceeded_full_whitespace(self):
        result = self.parser.parse(u'text　#hashtag')
        self.assertEqual(result.html, u'text　<a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_hashtag_number(self):
        result = self.parser.parse(u'text #1tag')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%231tag">#1tag</a>')
        self.assertEqual(result.tags, [u'1tag'])
    
    def test_not_hashtag_escape(self):
        result = self.parser.parse(u'&#nbsp;')
        self.assertEqual(result.html, u'&#nbsp;')
        self.assertEqual(result.tags, [])
    
    def test_hashtag_japanese(self):
        result = self.parser.parse(u'text #hashtagの')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>の')
        self.assertEqual(result.tags, [u'hashtag'])
    
    def test_hashtag_period(self):
        result = self.parser.parse(u'text.#hashtag')
        self.assertEqual(result.html, u'text.<a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_hashtag_trailing(self):
        result = self.parser.parse(u'text #hashtag')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>')
        self.assertEqual(result.tags, [u'hashtag'])
    
    def test_not_hashtag_exclamation(self):
        result = self.parser.parse(u'text #hashtag!')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>!')
        self.assertEqual(result.tags, [u'hashtag'])
    
    def test_hashtag_multiple(self):
        result = self.parser.parse(u'text #hashtag1 #hashtag2')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hashtag1">#hashtag1</a> <a href="http://search.twitter.com/search?q=%23hashtag2">#hashtag2</a>')
        self.assertEqual(result.tags, [u'hashtag1', u'hashtag2'])
    
    def test_not_hashtag_number(self):
        result = self.parser.parse(u'text #1234')
        self.assertEqual(result.html, u'text #1234')
        self.assertEqual(result.tags, [])
    
    def test_not_hashtag_text(self):
        result = self.parser.parse(u'text#hashtag')
        self.assertEqual(result.html, u'text#hashtag')
        self.assertEqual(result.tags, [])
    
    def test_hashtag_umlaut(self):
        result = self.parser.parse(u'text #hash_tagüäö')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hash_tag%C3%BC%C3%A4%C3%B6">#hash_tagüäö</a>')
        self.assertEqual(result.tags, [u'hash_tag\xfc\xe4\xf6'])
    
    def test_hashtag_alpha(self):
        result = self.parser.parse(u'text #hash0tag')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hash0tag">#hash0tag</a>')
        self.assertEqual(result.tags, [u'hash0tag'])
    
    def test_hashtag_under(self):
        result = self.parser.parse(u'text #hash_tag')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hash_tag">#hash_tag</a>')
        self.assertEqual(result.tags, [u'hash_tag'])

    
    # Username tests -----------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_not_username_preceded_letter(self):
        result = self.parser.parse(u'meet@the beach')
        self.assertEqual(result.html, u'meet@the beach')
        self.assertEqual(result.users, [])
    
    def test_username_preceded_punctuation(self):
        result = self.parser.parse(u'.@username')
        self.assertEqual(result.html, u'.<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
    
    def test_username_preceded_japanese(self):
        result = self.parser.parse(u'あ@username')
        self.assertEqual(result.html, u'あ<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
    
    def test_username_followed_japanese(self):
        result = self.parser.parse(u'@usernameの')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a>の')
        self.assertEqual(result.users, [u'username'])
        
    def test_username_surrounded_japanese(self):
        result = self.parser.parse(u'あ@usernameの')
        self.assertEqual(result.html, u'あ<a href="http://twitter.com/username">@username</a>の')
        self.assertEqual(result.users, [u'username'])    
    
    def test_username_followed_punctuation(self):
        result = self.parser.parse(u'@username&^$%^')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a>&^$%^')
        self.assertEqual(result.users, [u'username'])
    
    def test_not_username_spaced(self):
        result = self.parser.parse(u'@ username')
        self.assertEqual(result.html, u'@ username')
        self.assertEqual(result.users, [])
    
    def test_username_beginning(self):
        result = self.parser.parse(u'@username text')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a> text')
        self.assertEqual(result.users, [u'username'])
    
    def test_username_to_long(self):
        result = self.parser.parse(u'@username9012345678901')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username901234567890">@username901234567890</a>1')
        self.assertEqual(result.users, [u'username901234567890'])
    
    def test_username_full_at_sign(self):
        result = self.parser.parse(u'＠username')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">＠username</a>')
        self.assertEqual(result.users, [u'username'])
    
    def test_username_trailing(self):
        result = self.parser.parse(u'text @username')
        self.assertEqual(result.html, u'text <a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
    
    # Replies
    def test_username_reply_simple(self):
        result = self.parser.parse(u'@username')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.reply, u'username')
    
    def test_username_reply_whitespace(self):
        result = self.parser.parse(u'   @username')
        self.assertEqual(result.html, u'   <a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.reply, u'username')
    
    def test_username_reply_full(self):
        result = self.parser.parse(u'　@username')
        self.assertEqual(result.html, u'　<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.reply, u'username')

    def test_username_non_reply(self):
        result = self.parser.parse(u'test @username')
        self.assertEqual(result.html, u'test <a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.reply, None)
    
    
    # List tests ---------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_list_preceeded(self):
        result = self.parser.parse(u'text @username/list')
        self.assertEqual(result.html, u'text <a href="http://twitter.com/username/list">@username/list</a>')
        self.assertEqual(result.lists, [(u'username', u'list')])
    
    def test_list_beginning(self):
        result = self.parser.parse(u'@username/list')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username/list">@username/list</a>')
        self.assertEqual(result.lists, [(u'username', u'list')])
    
    def test_list_preceeded_punctuation(self):
        result = self.parser.parse(u'.@username/list')
        self.assertEqual(result.html, u'.<a href="http://twitter.com/username/list">@username/list</a>')
        self.assertEqual(result.lists, [(u'username', u'list')])
    
    def test_list_followed_punctuation(self):
        result = self.parser.parse(u'@username/list&^$%^')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username/list">@username/list</a>&^$%^')
        self.assertEqual(result.lists, [(u'username', u'list')])
    
    def test_list_not_slash_space(self):
        result = self.parser.parse(u'@username/ list')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a>/ list')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.lists, [])
    
    def test_list_beginning(self):
        result = self.parser.parse(u'@username/list')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username/list">@username/list</a>')
        self.assertEqual(result.lists, [(u'username', u'list')])
        
    def test_list_not_empty_username(self):
        result = self.parser.parse(u'text @/list')
        self.assertEqual(result.html, u'text @/list')
        self.assertEqual(result.lists, [])
  
    def test_list_not_preceeded_letter(self):
        result = self.parser.parse(u'meet@the/beach')
        self.assertEqual(result.html, u'meet@the/beach')
        self.assertEqual(result.lists, [])
  
    def test_list_long_truncate(self):
        result = self.parser.parse(u'@username/list5678901234567890123456789012345678901234567890123456789012345678901234567890A')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username/list5678901234567890123456789012345678901234567890123456789012345678901234567890">@username/list5678901234567890123456789012345678901234567890123456789012345678901234567890</a>A')
        self.assertEqual(result.lists, [(u'username', u'list5678901234567890123456789012345678901234567890123456789012345678901234567890')])
    
    def test_list_with_dash(self):
        result = self.parser.parse(u'text @username/list-foo')
        self.assertEqual(result.html, u'text <a href="http://twitter.com/username/list-foo">@username/list-foo</a>')
        self.assertEqual(result.lists, [(u'username', u'list-foo')])


# Test it!
if __name__ == '__main__':
    unittest.main()

