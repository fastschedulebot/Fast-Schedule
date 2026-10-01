Rich messages

The following methods and objects allow your bot to handle and send rich messages.
Rich Message Formatting Options

Rich messages support advanced structured formatting options like headings, lists, tables, media, block quotations, collapsible blocks, footnotes, and formulas. Telegram clients will render them accordingly. You can specify rich message content using Markdown-style or HTML-style formatting.

Plain URLs, e-mail addresses, username mentions, hashtags, cashtags, bot commands, phone numbers, and bank card numbers are detected automatically. To disable automatic entity detection, pass True in the skip_entity_detection field. Note that Telegram clients will display an alert to the user before opening an inline link ('Open this link?' together with the full URL).
Rich Message Limits

Rich messages are subject to the following limits:

    Up to 32768 UTF-8 characters in the rich message text, including custom emoji alternative text and formula source.
    Up to 500 blocks, including nested blocks, list items, ordered list items, table rows, quotation blocks, and details blocks.
    Up to 16 levels of nested formatting and blocks.
    Up to 50 media attachments in total, including photos, videos, and audio files.
    Up to 20 columns in a table.

Rich Markdown style

To use this mode, pass rich message content in the markdown field. Use the following syntax in your message:

**bold text**
__bold text__
*italic text*
_italic text_
~~strikethrough text~~
`inline fixed-width code`
==marked text==
||spoiler||

[inline URL](https://t.me/)
[inline e-mail](mailto:user@example.com)
[inline phone number](tel:+123456789)
[inline mention of a user](tg://user?id=123456789)
![👍](tg://emoji?id=5368324170671202286)
![22:45 tomorrow](tg://time?unix=1647531900&format=wDT)
$x^2 + y^2$
\#hashtag $USD +12345678901, card: 4242 4242 4242 4242, https://t.me t.me a@t.me /command @username
all the text above was on the same line

# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

Paragraph text

```python
  print('pre-formatted fixed-width code block written in the Python programming language')
```

---

- unordered list item
* unordered list item
+ unordered list item

1. ordered list item
2. ordered list item

- [ ] task list item
- [x] completed task list item

>Block quotation started
>
>Block quotation continued on the next line
>Block quotation continued on the same line
>
>The last line of the block quotation

![](https://telegram.org/example/photo.jpg)
![](https://telegram.org/example/video.mp4)
![](https://telegram.org/example/audio.mp3)
![](https://telegram.org/example/audio.ogg)
![](https://telegram.org/example/animation.gif)

![](https://telegram.org/example/photo.jpg "Photo caption")
![](https://telegram.org/example/video.mp4 "Video caption")
![](https://telegram.org/example/audio.mp3 "Audio caption")
![](https://telegram.org/example/audio.ogg "Voice note caption")
![](https://telegram.org/example/animation.gif "Animation caption")

| Header 1 | Header 2 |
|:---------|:--------:|
| left     | center   |

Text with a reference[^id1] and another one[^id2].

[^id1]: Definition of the first footnote.
[^id2]: Definition of the second footnote.

$$E = mc^2$$

```math
E = mc^2
```

## Example Nested Syntax Report for _Q1_
Intro with <u>underlined text</u>, ==marked text==, and $x^2 + y^2$.
**Bold _italic <u>underlined italic bold</u> italic_ bold**
<u>In inline tags, nested **markdown** is parsed</u>
>Quote with **bold text, ~~strikethrough, and <tg-spoiler>spoiler</tg-spoiler>~~**, plus [a link](https://t.me/).

- List item with `code`, <sup>superscript</sup>, <sub>subscript</sub>, and a footnote[^note]
- Another item with **bold <tg-spoiler><code>spoiler code</code></tg-spoiler>**
- Another item with ~~strikethrough and <ins>inserted text</ins>~~

| Metric | Value |
|:-------|------:|
| Speed  | **42** <sup>ms</sup> |
| Status | <tg-spoiler>ready</tg-spoiler> |

[^note]: Footnote with _italic text_ and <u>HTML underline</u>.

---

# Details blocks can contain Markdown content:

<details open><summary>Summary with **bold text**</summary>

### Details heading
- List item with _italic text_
- List item with <tg-spoiler>spoiler</tg-spoiler>

</details>

# Collages and slideshows can contain Markdown media blocks:

<tg-collage>

![](https://telegram.org/example/photo.jpg)
![](https://telegram.org/example/video.mp4)

</tg-collage>

<tg-slideshow>

![](https://telegram.org/example/photo.jpg)
![](https://telegram.org/example/video.mp4)

</tg-slideshow>

For formatting features that don't have Markdown syntax, use HTML tags:

<u>underlined text</u>, <ins>underlined text</ins>
<sub>subscript text</sub>
<sup>superscript text</sup>
<a name="chapter-1"></a>
<aside>Pull quote<cite>The Author</cite></aside>
<details open><summary>Title</summary>Content</details>
<tg-map lat="41.9" long="12.5" zoom="14"/>
<tg-collage><img src="https://telegram.org/example/photo.jpg"/><figcaption>Caption<cite>The Author</cite></figcaption></tg-collage>
<tg-slideshow><img src="https://telegram.org/example/photo.jpg"/><video src="https://telegram.org/example/video.mp4"/><figcaption>Slideshow caption<cite>The Author</cite></figcaption></tg-slideshow>

Please note:

    Rich Markdown is compatible with GitHub Flavored Markdown where possible and can contain arbitrary HTML. Supported rich message HTML tags are parsed as described in Rich HTML style.
    Media can be specified only as a separate block.
    Media blocks support only HTTP and HTTPS URLs.
    Media type is determined by the MIME type and the URL of the media.
    In media syntax, the optional title after the URL is used as the caption; for example, displays “Photo caption” under the media.
    Table cells can contain only inline formatting.
    Formula source is treated as raw LaTeX.
    See date-time entity formatting for more details about supported date-time formats.

Rich HTML style

To use this mode, pass rich message content in the html field. The following tags are currently supported:

<a name="chapter-0"></a>
<b>bold text</b>, <strong>bold text</strong>
<i>italic text</i>, <em>italic text</em>
<u>underlined text</u>, <ins>underlined text</ins>
<s>strikethrough text</s>, <strike>strikethrough text</strike>, <del>strikethrough text</del>
<code>inline fixed-width code</code>
<mark>marked text</mark>
<sub>subscript text</sub>
<sup>superscript text</sup>
<tg-spoiler>spoiler</tg-spoiler>

<a href="#note-1">Reference</a>
<a href="https://t.me/">inline URL</a>
<a href="mailto:user@example.com">inline e-mail</a>
<a href="tel:+123456789">inline phone number</a>
<a href="tg://user?id=123456789">inline mention of a user</a>
<a href="#chapter-1">in-document link</a>
<a name="chapter-1"></a>

<tg-reference name="note-1">Referenced text</tg-reference>
<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>
<img src="tg://emoji?id=5368324170671202286" alt="👍"/>
<tg-time unix="1647531900" format="wDT">22:45 tomorrow</tg-time>
<tg-math>x^2 + y^2</tg-math>

#hashtag $USD +12345678901, card: 4242 4242 4242 4242, https://t.me t.me a@t.me /command @username

all the text above was on the same line

<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6</h6>

<a name="chapter-2"></a>

<p>Paragraph text</p>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">  print('pre-formatted fixed-width code block written in the Python programming language')</code></pre>
<footer>Footer text</footer>
<hr/>
<ul><li>unordered list item</li></ul>
<ol><li>ordered list item</li></ol>
<ol start="3" type="a" reversed><li>ordered list item</li></ol>
<ol><li value="7" type="i">ordered list item with explicit number</li></ol>
<ul>
<li><input type="checkbox" checked>Checked checkbox</li>
<li><input type="checkbox">Unchecked checkbox</li>
</ul>

<blockquote>Block quotation started<br>Block quotation continued<br>The last line of the block quotation<cite>The Author</cite></blockquote>
<aside>Pull quote<cite>The Author</cite></aside>

<img src="https://telegram.org/example/photo.jpg"/>
<video src="https://telegram.org/example/video.mp4"></video>
<audio src="https://telegram.org/example/audio.mp3"></audio>
<audio src="https://telegram.org/example/audio.ogg"></audio>
<video src="https://telegram.org/example/animation.gif"></video>

<figure><img src="https://telegram.org/example/photo.jpg" tg-spoiler/><figcaption>Photo caption<cite>Photo credit</cite></figcaption></figure>
<figure><video src="https://telegram.org/example/video.mp4" tg-spoiler></video><figcaption>Video caption</figcaption></figure>
<figure><audio src="https://telegram.org/example/audio.mp3"></audio><figcaption>Audio caption</figcaption></figure>
<figure><audio src="https://telegram.org/example/audio.ogg"></audio><figcaption>Voice note caption</figcaption></figure>
<figure><video src="https://telegram.org/example/animation.gif" tg-spoiler></video><figcaption>Animation caption</figcaption></figure>

<tg-map lat="41.9" long="12.5" zoom="14"/>
<figure><tg-map lat="41.9" long="12.5" zoom="14"/><figcaption>Map caption</figcaption></figure>

<tg-collage><img src="https://telegram.org/example/photo.jpg"/><video src="https://telegram.org/example/video.mp4"/></tg-collage>
<tg-collage><video src="https://telegram.org/example/video.mp4"/><img src="https://telegram.org/example/photo.jpg"/><figcaption>Collage caption</figcaption></tg-collage>
<tg-slideshow><img src="https://telegram.org/example/photo.jpg"/><video src="https://telegram.org/example/video.mp4"/></tg-slideshow>
<tg-slideshow><video src="https://telegram.org/example/video.mp4"/><img src="https://telegram.org/example/photo.jpg"/><figcaption>Slideshow caption</figcaption></tg-slideshow>

<table><tr><th>Header 1</th><th>Header 2</th></tr><tr><td>Value 1</td><td>Value 2</td></tr></table>
<table bordered striped><caption>Table caption</caption>
<tr><td colspan="2" rowspan="2" align="left">Value</td><td align="center">Value2</td><td align="right">Value3</td></tr>
<tr><td valign="top">Value4</td><td valign="middle">Value5</td><td valign="bottom">Value6</td></tr>
<tr><td>Value7</td></tr></table>

<details><summary>Title</summary>Content</details>
<details open><summary>Title</summary>Content</details>
<tg-math-block>E = mc^2</tg-math-block>

Please note:

    Only the tags mentioned above are currently supported.
    All numerical HTML entities are supported.
    The API currently supports only the following named HTML entities: &lt;, &gt;, &amp;, &quot;, &apos;, &nbsp;, &hellip;, &mdash;, &ndash;, &lsquo;, &rsquo;, &ldquo; and &rdquo;.
    Use nested pre and code tags to define the programming language for a pre-formatted block.
    Programming language can't be specified for standalone code tags.
    Links mailto:..., tel:..., and tg://user?id=... are rendered as e-mail links, phone links, and inline mentions respectively. Other supported links are rendered as regular inline links.
    Images, videos, and audio files can be specified only as separate media blocks.
    Media blocks support only HTTP and HTTPS URLs.
    An empty <a name="..."></a> on its own creates an anchor that can be linked to with <a href="#...">...</a>.
    In <figcaption>, you can use <cite> tags to specify caption credit.
    Use <tg-reference name="...">...</tg-reference> to define referenced text that can be linked to with <a href="#...">...</a>.
    The body of a <details> tag can contain rich message content. If the open attribute is specified, the block is expanded by default.
    Formula source is treated as raw LaTeX.
    See date-time entity formatting for more details about supported date-time formats.

RichMessage

Rich formatted message.
Field 	Type 	Description
blocks 	Array of RichBlock 	Content of the message
is_rtl 	Boolean 	Optional. True, if the rich message must be shown right-to-left
InputRichMessage

Describes a rich message to be sent. Exactly one of the fields html or markdown must be used.
Field 	Type 	Description
html 	String 	Optional. Content of the rich message to send described using HTML formatting. See rich message formatting options for more details.
markdown 	String 	Optional. Content of the rich message to send described using Markdown formatting. See rich message formatting options for more details.
is_rtl 	Boolean 	Optional. Pass True if the rich message must be shown right-to-left
skip_entity_detection 	Boolean 	Optional. Pass True to skip automatic detection of entities (e.g., URLs, email addresses, username mentions, hashtags, cashtags, bot commands, or phone numbers) in the text
sendRichMessage

Use this method to send rich messages. If the message contains a block with a media element, then the bot must have the right to send the media to the chat. On success, the sent Message is returned.
Parameter 	Type 	Required 	Description
business_connection_id 	String 	Optional 	Unique identifier of the business connection on behalf of which the message will be sent
chat_id 	Integer or String 	Yes 	Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
message_thread_id 	Integer 	Optional 	Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
direct_messages_topic_id 	Integer 	Optional 	Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
rich_message 	InputRichMessage 	Yes 	The message to be sent
disable_notification 	Boolean 	Optional 	Sends the message silently. Users will receive a notification with no sound.
protect_content 	Boolean 	Optional 	Protects the contents of the sent message from forwarding and saving
allow_paid_broadcast 	Boolean 	Optional 	Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
message_effect_id 	String 	Optional 	Unique identifier of the message effect to be added to the message; for private chats only
suggested_post_parameters 	SuggestedPostParameters 	Optional 	A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
reply_parameters 	ReplyParameters 	Optional 	Description of the message to reply to
reply_markup 	InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply 	Optional 	Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
sendRichMessageDraft

Use this method to stream a partial rich message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendRichMessage with the complete message to persist it in the user's chat. Returns True on success.
Parameter 	Type 	Required 	Description
chat_id 	Integer 	Yes 	Unique identifier for the target private chat
message_thread_id 	Integer 	Optional 	Unique identifier for the target message thread
draft_id 	Integer 	Yes 	Unique identifier of the message draft; must be non-zero. Changes to drafts with the same identifier are animated.
rich_message 	InputRichMessage 	Yes 	The partial message to be streamed
RichText

This object represents a rich formatted text. Currently, it can be either a String for plain text, an Array of RichText, or any of the following types:

    RichTextBold
    RichTextItalic
    RichTextUnderline
    RichTextStrikethrough
    RichTextSpoiler
    RichTextDateTime
    RichTextTextMention
    RichTextSubscript
    RichTextSuperscript
    RichTextMarked
    RichTextCode
    RichTextCustomEmoji
    RichTextMathematicalExpression
    RichTextUrl
    RichTextEmailAddress
    RichTextPhoneNumber
    RichTextBankCardNumber
    RichTextMention
    RichTextHashtag
    RichTextCashtag
    RichTextBotCommand
    RichTextAnchor
    RichTextAnchorLink
    RichTextReference
    RichTextReferenceLink

RichTextBold

A bold text.
Field 	Type 	Description
type 	String 	Type of the rich text, always “bold”
text 	RichText 	The text
RichTextItalic

An italicized text.
Field 	Type 	Description
type 	String 	Type of the rich text, always “italic”
text 	RichText 	The text
RichTextUnderline

An underlined text.
Field 	Type 	Description
type 	String 	Type of the rich text, always “underline”
text 	RichText 	The text
RichTextStrikethrough

A strikethrough text.
Field 	Type 	Description
type 	String 	Type of the rich text, always “strikethrough”
text 	RichText 	The text
RichTextSpoiler

A text covered by a spoiler.
Field 	Type 	Description
type 	String 	Type of the rich text, always “spoiler”
text 	RichText 	The text
RichTextDateTime

Formatted date and time.
Field 	Type 	Description
type 	String 	Type of the rich text, always “date_time”
text 	RichText 	The text
unix_time 	Integer 	The Unix time associated with the entity
date_time_format 	String 	The string that defines the formatting of the date and time. See date-time entity formatting for more details.
RichTextTextMention

A mention of a Telegram user by their identifier.
Field 	Type 	Description
type 	String 	Type of the rich text, always “text_mention”
text 	RichText 	The text
user 	User 	The mentioned user
RichTextSubscript

A subscript text.
Field 	Type 	Description
type 	String 	Type of the rich text, always “subscript”
text 	RichText 	The text
RichTextSuperscript

A superscript text.
Field 	Type 	Description
type 	String 	Type of the rich text, always “superscript”
text 	RichText 	The text
RichTextMarked

A marked text.
Field 	Type 	Description
type 	String 	Type of the rich text, always “marked”
text 	RichText 	The text
RichTextCode

A monowidth text.
Field 	Type 	Description
type 	String 	Type of the rich text, always “code”
text 	RichText 	The text
RichTextCustomEmoji

A custom emoji.
Field 	Type 	Description
type 	String 	Type of the rich text, always “custom_emoji”
custom_emoji_id 	String 	Unique identifier of the custom emoji. Use getCustomEmojiStickers to get full information about the sticker.
alternative_text 	String 	Alternative emoji for the custom emoji
RichTextMathematicalExpression

A mathematical expression.
Field 	Type 	Description
type 	String 	Type of the rich text, always “mathematical_expression”
expression 	String 	The expression in LaTeX format
RichTextUrl

A text with a link.
Field 	Type 	Description
type 	String 	Type of the rich text, always “url”
text 	RichText 	The text
url 	String 	URL of the link
RichTextEmailAddress

A text with an email address.
Field 	Type 	Description
type 	String 	Type of the rich text, always “email_address”
text 	RichText 	The text
email_address 	String 	The email address
RichTextPhoneNumber

A text with a phone number.
Field 	Type 	Description
type 	String 	Type of the rich text, always “phone_number”
text 	RichText 	The text
phone_number 	String 	The phone number
RichTextBankCardNumber

A text with a bank card number.
Field 	Type 	Description
type 	String 	Type of the rich text, always “bank_card_number”
text 	RichText 	The text
bank_card_number 	String 	The bank card number
RichTextMention

A mention by a username.
Field 	Type 	Description
type 	String 	Type of the rich text, always “mention”
text 	RichText 	The text
username 	String 	The username
RichTextHashtag

A hashtag.
Field 	Type 	Description
type 	String 	Type of the rich text, always “hashtag”
text 	RichText 	The text
hashtag 	String 	The hashtag
RichTextCashtag

A cashtag.
Field 	Type 	Description
type 	String 	Type of the rich text, always “cashtag”
text 	RichText 	The text
cashtag 	String 	The cashtag
RichTextBotCommand

A bot command.
Field 	Type 	Description
type 	String 	Type of the rich text, always “bot_command”
text 	RichText 	The text
bot_command 	String 	The bot command
RichTextAnchor

An anchor.
Field 	Type 	Description
type 	String 	Type of the rich text, always “anchor”
name 	String 	The name of the anchor
RichTextAnchorLink

A link to an anchor.
Field 	Type 	Description
type 	String 	Type of the rich text, always “anchor_link”
text 	RichText 	The link text
anchor_name 	String 	The name of the anchor. If the name is empty, then the link brings back to the top of the message.
RichTextReference

A reference.
Field 	Type 	Description
type 	String 	Type of the rich text, always “reference”
text 	RichText 	Text of the reference
name 	String 	The name of the reference
RichTextReferenceLink

A link to a reference.
Field 	Type 	Description
type 	String 	Type of the rich text, always “reference_link”
text 	RichText 	The link text
reference_name 	String 	The name of the reference
RichBlockCaption

Caption of a rich formatted block.
Field 	Type 	Description
text 	RichText 	Block caption
credit 	RichText 	Optional. Block credit which corresponds to the HTML tag <cite>
RichBlockTableCell

Cell in a table.
Field 	Type 	Description
text 	RichText 	Optional. Text in the cell. If omitted, then the cell is invisible.
is_header 	True 	Optional. True, if the cell is a header cell
colspan 	Integer 	Optional. The number of columns the cell spans if it is bigger than 1
rowspan 	Integer 	Optional. The number of rows the cell spans if it is bigger than 1
align 	String 	Horizontal cell content alignment. Currently, must be one of “left”, “center”, or “right”.
valign 	String 	Vertical cell content alignment. Currently, must be one of “top”, “middle”, or “bottom”.
RichBlockListItem

An item of a list.
Field 	Type 	Description
label 	String 	Label of the item
blocks 	Array of RichBlock 	The content of the item
has_checkbox 	True 	Optional. True, if the item has a checkbox
is_checked 	True 	Optional. True, if the item has a checked checkbox
value 	Integer 	Optional. For ordered lists, the numeric value of the item label
type 	String 	Optional. For ordered lists, the type of the item label; must be one of “a” for lowercase letters, “A” for uppercase letters, “i” for lowercase Roman numerals, “I” for uppercase Roman numerals, or “1” for decimal numbers
RichBlock

This object represents a block in a rich formatted message. Currently, it can be any of the following types:

    RichBlockParagraph
    RichBlockSectionHeading
    RichBlockPreformatted
    RichBlockFooter
    RichBlockDivider
    RichBlockMathematicalExpression
    RichBlockAnchor
    RichBlockList
    RichBlockBlockQuotation
    RichBlockPullQuotation
    RichBlockCollage
    RichBlockSlideshow
    RichBlockTable
    RichBlockDetails
    RichBlockMap
    RichBlockAnimation
    RichBlockAudio
    RichBlockPhoto
    RichBlockVideo
    RichBlockVoiceNote
    RichBlockThinking

RichBlockParagraph

A text paragraph, corresponding to the HTML tag <p>.
Field 	Type 	Description
type 	String 	Type of the block, always “paragraph”
text 	RichText 	Text of the block
RichBlockSectionHeading

A section heading, corresponding to the HTML tags <h1>, <h2>, <h3>, <h4>, <h5>, or <h6>.
Field 	Type 	Description
type 	String 	Type of the block, always “heading”
text 	RichText 	Text of the block
size 	Integer 	Relative size of the text font; 1-6, 1 is the largest, 6 is the smallest
RichBlockPreformatted

A preformatted text block, corresponding to the nested HTML tags <pre> and <code>.
Field 	Type 	Description
type 	String 	Type of the block, always “pre”
text 	RichText 	Text of the block
language 	String 	Optional. The programming language of the text
RichBlockFooter

A footer, corresponding to the HTML tag <footer>.
Field 	Type 	Description
type 	String 	Type of the block, always “footer”
text 	RichText 	Text of the block
RichBlockDivider

A divider, corresponding to the HTML tag <hr/>.
Field 	Type 	Description
type 	String 	Type of the block, always “divider”
RichBlockMathematicalExpression

A block with a mathematical expression in LaTeX format, corresponding to the custom HTML tag <tg-math-block>.
Field 	Type 	Description
type 	String 	Type of the block, always “mathematical_expression”
expression 	String 	The mathematical expression in LaTeX format
RichBlockAnchor

A block with an anchor, corresponding to the HTML tag <a> with the attribute name.
Field 	Type 	Description
type 	String 	Type of the block, always “anchor”
name 	String 	The name of the anchor
RichBlockList

A list of blocks, corresponding to the HTML tag <ul> or <ol> with multiple nested tags <li>.
Field 	Type 	Description
type 	String 	Type of the block, always “list”
items 	Array of RichBlockListItem 	Items of the list
RichBlockBlockQuotation

A block quotation, corresponding to the HTML tag <blockquote>.
Field 	Type 	Description
type 	String 	Type of the block, always “blockquote”
blocks 	Array of RichBlock 	Content of the block
credit 	RichText 	Optional. Credit of the block
RichBlockPullQuotation

A quotation with centered text, loosely corresponding to the HTML tag <aside>.
Field 	Type 	Description
type 	String 	Type of the block, always “pullquote”
text 	RichText 	Text of the block
credit 	RichText 	Optional. Credit of the block
RichBlockCollage

A collage, corresponding to the custom HTML tag <tg-collage>.
Field 	Type 	Description
type 	String 	Type of the block, always “collage”
blocks 	Array of RichBlock 	Elements of the collage
caption 	RichBlockCaption 	Optional. Caption of the block
RichBlockSlideshow

A slideshow, corresponding to the custom HTML tag <tg-slideshow>.
Field 	Type 	Description
type 	String 	Type of the block, always “slideshow”
blocks 	Array of RichBlock 	Elements of the slideshow
caption 	RichBlockCaption 	Optional. Caption of the block
RichBlockTable

A table, corresponding to the HTML tag <table>.
Field 	Type 	Description
type 	String 	Type of the block, always “table”
cells 	Array of Array of RichBlockTableCell 	Cells of the table
is_bordered 	True 	Optional. True, if the table has borders
is_striped 	True 	Optional. True, if the table is striped
caption 	RichText 	Optional. Caption of the table
RichBlockDetails

An expandable block for details disclosure, corresponding to the HTML tag <details>.
Field 	Type 	Description
type 	String 	Type of the block, always “details”
summary 	RichText 	Always shown summary of the block
blocks 	Array of RichBlock 	Content of the block
is_open 	True 	Optional. True, if the content of the block is visible by default
RichBlockMap

A block with a map, corresponding to the custom HTML tag <tg-map>.
Field 	Type 	Description
type 	String 	Type of the block, always “map”
location 	Location 	Location of the center of the map
zoom 	Integer 	Map zoom level; 13-20
width 	Integer 	Expected width of the map
height 	Integer 	Expected height of the map
caption 	RichBlockCaption 	Optional. Caption of the block
RichBlockAnimation

A block with an animation, corresponding to the HTML tag <video>.
Field 	Type 	Description
type 	String 	Type of the block, always “animation”
animation 	Animation 	The animation
has_spoiler 	True 	Optional. True, if the media preview is covered by a spoiler animation
caption 	RichBlockCaption 	Optional. Caption of the block
RichBlockAudio

A block with a music file, corresponding to the HTML tag <audio>.
Field 	Type 	Description
type 	String 	Type of the block, always “audio”
audio 	Audio 	The audio
caption 	RichBlockCaption 	Optional. Caption of the block
RichBlockPhoto

A block with a photo, corresponding to the HTML tag <photo>.
Field 	Type 	Description
type 	String 	Type of the block, always “photo”
photo 	Array of PhotoSize 	Available sizes of the photo
has_spoiler 	True 	Optional. True, if the media preview is covered by a spoiler animation
caption 	RichBlockCaption 	Optional. Caption of the block
RichBlockVideo

A block with a video, corresponding to the HTML tag <video>.
Field 	Type 	Description
type 	String 	Type of the block, always “video”
video 	Video 	The video
has_spoiler 	True 	Optional. True, if the media preview is covered by a spoiler animation
caption 	RichBlockCaption 	Optional. Caption of the block
RichBlockVoiceNote

A block with a voice note, corresponding to the HTML tag <audio>.
Field 	Type 	Description
type 	String 	Type of the block, always “voice_note”
voice_note 	Voice 	The voice note
caption 	RichBlockCaption 	Optional. Caption of the block
RichBlockThinking

A block with a “Thinking…” placeholder, corresponding to the custom HTML tag <tg-thinking>. The block may be used only in sendRichMessageDraft, therefore it can't be received in messages. See https://t.me/addemoji/AIActions for examples of custom emoji, which are recommended for usage in the block.
Field 	Type 	Description
type 	String 	Type of the block, always “thinking”
text 	RichText 	Text of the block. See https://t.me/addemoji/AIActions for examples of custom emoji, which are recommended for usage in the block.