<?php

#余計なHTMLタグなどを取り除く処理
function cleaning($tunes)
{
    $tunes = str_replace("<br>", "", $tunes);
    $tunes = str_replace("<br />", "", $tunes);
    $tunes = preg_replace('|<div id="notes\\d+">|U', '', $tunes);
    $tunes = preg_replace('|</div><!-- /#notes\\d+ -->|U', '', $tunes);
    $tunes = str_replace("\n\n", "\n", $tunes);
    $tunes = html_entity_decode($tunes, ENT_QUOTES, 'UTF-8');
    return $tunes;
}

#ABC譜を摘出するための正規表現
$reg_note = '|<div class="notes">(.+)</div><!-- /.notes -->|sU';

#1万5000曲をスクレイピングする
foreach (range(1, 15000) as $i)
{
    echo "scraping ... ${i}".PHP_EOL;
                        
    $html = file_get_contents("https://thesession.org/tunes/$i", "UTF-8");

    preg_match_all($reg_note, $html, $match, PREG_PATTERN_ORDER);

    $tunes = cleaning(implode("\n\n", $match[1]));

    $tunes = mb_convert_encoding($tunes, "UTF-8", "auto");

    file_put_contents("tunes.abc", $tunes, FILE_APPEND);
        
    sleep(1);
}
